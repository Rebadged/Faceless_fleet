"""Stage 2 — deterministic assembly with ffmpeg.

Turns the raw assets (scene.png / scene.mp4 / bed.wav / narration.wav) into a
finished long-form video in output/pending_review/<slug>/.

Key ffmpeg techniques (from the research playbook):
  - stream_loop   : loop a short clip to N hours with NO re-encode (fast, lossless)
  - zoompan       : Ken Burns slow-zoom to give a single still gentle motion
  - acrossfade    : seamless audio loop seam
  - amix + volume : duck a music bed under narration

This module is pure ffmpeg, runs anywhere (VPS, Actions, locally), needs no
credits, and is independently testable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
from pathlib import Path

from .config import ROOT, load_channel, output_dirs

HOURS = {"1h": 3600, "3h": 10800, "8h": 28800, "12h": 43200}


def _run(cmd: list[str]) -> None:
    print("[ffmpeg]", " ".join(str(c) for c in cmd[:6]), "...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _probe_duration(path: Path) -> float:
    for entries in ("format=duration", "stream=duration"):
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", entries,
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True).stdout.strip().splitlines()
        for line in out:
            try:
                return float(line)
            except ValueError:
                continue
    raise ValueError(f"could not probe duration of {path}")


def make_seamless_video(clip: Path, out: Path, xfade: float, fps: int) -> Path:
    """Crossfade the clip's end-wrap into its start so a stream_loop has NO visible
    seam. Technique: with D=duration, X=xfade, take tail=clip[X:D] and head=clip[0:X]
    and xfade(tail, head, offset=D-2X). The result starts AND ends on the same frame
    (clip @ time X), so looping it is seamless; the true end->start wrap is hidden in
    the mid-clip crossfade. Output length = D - X."""
    d = _probe_duration(clip)
    if xfade <= 0 or d <= 2 * xfade + 0.1:   # too short to wrap-fade; leave as-is
        _run(["ffmpeg", "-y", "-i", str(clip), "-c", "copy", str(out)])
        return out
    fc = (f"[0:v]trim=0:{xfade},setpts=PTS-STARTPTS[head];"
          f"[0:v]trim={xfade}:{d},setpts=PTS-STARTPTS[tail];"
          f"[tail][head]xfade=transition=fade:duration={xfade}:offset={d - 2*xfade}[v]")
    _run(["ffmpeg", "-y", "-i", str(clip), "-filter_complex", fc, "-map", "[v]",
          "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(out)])
    return out


def apply_particle_overlay(base: Path, overlay: Path, out: Path,
                           opacity: float, blend: str, fps: int) -> Path:
    """Composite a looping particle element (rain / snow / sparks) over the base clip so
    no two videos are pixel-identical — the chosen material-variation lever now that the
    camera stays locked (see research/CROSS_REFERENCE_2026.md). The overlay is a white-
    particles-on-black clip; a `screen`/`lighten` blend makes the black read as transparent.
    It is stream-looped to the base length and scaled to match, then blended at `opacity`.

    Applied to the SHORT unit before the seamless wrap + lossless loop, so it's encoded
    once and stays cheap. If the overlay file is missing the caller skips this step."""
    d = _probe_duration(base)
    fc = (f"[1:v][0:v]scale2ref[ov][bse];"
          f"[bse][ov]blend=all_mode={blend}:all_opacity={opacity},format=yuv420p[v]")
    _run(["ffmpeg", "-y", "-i", str(base), "-stream_loop", "-1", "-i", str(overlay),
          "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}",
          "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(out)])
    return out


def _find_overlay(cfg: dict, scene: dict) -> Path | None:
    """Resolve the particle-overlay file for a scene, if overlays are enabled and present.
    Looks up scene['overlay'] (explicit) else the scene's weather, in the overlays dir,
    extension-tolerant. Returns None (skip the step) when nothing is configured/found."""
    a = cfg["assembly"].get("particle_overlay", {})
    if not a.get("enabled"):
        return None
    name = scene.get("overlay") or scene.get("weather")
    if not name:
        return None
    odir = ROOT / a.get("dir", "assets/overlays")
    for ext in (".mov", ".webm", ".mp4", ".mkv"):
        p = odir / f"{name}{ext}"
        if p.exists():
            return p
    return None


def build_sfx_bed(layers: list[dict], library: dict, sfx_dir: Path, out: Path,
                  unit_seconds: int = 480) -> Path:
    """Mix reusable SFX elements (rain/thunder/fire/wind) into one bed at per-scene
    levels. Each layer = {el, gain}; el maps to a file via `library`. Every element
    is looped to a common unit length, gain-staged, mixed, and limited to avoid
    clipping. The result (a ~90s wav) feeds the normal seamless-loop audio path, so
    you grab ~5 element files ONCE and the pipeline builds every video's bed.

    sleep-safe gains live in the scene config (e.g. thunder 0.5, fire 0.25)."""
    def _resolve(name: str):
        p = sfx_dir / name
        if p.exists():
            return p
        stem = Path(name).stem                       # tolerate .mp3 vs .wav etc.
        for ext in (".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"):
            c = sfx_dir / (stem + ext)
            if c.exists():
                return c
        return None

    present = [(l, _resolve(library.get(l["el"], ""))) for l in layers]
    present = [(l, f) for l, f in present if f]
    if not present:
        raise FileNotFoundError(
            f"No SFX element files found in {sfx_dir} for layers {[l['el'] for l in layers]}. "
            f"Download them (see LAUNCH_PLAN.md) or drop a ready bed.wav in the raw dir.")
    inputs, filt = [], []
    for i, (layer, f) in enumerate(present):
        inputs += ["-stream_loop", "-1", "-i", str(f)]
        # Normalize each ELEMENT to a common loudness first (-20 LUFS, TP -3) so the
        # config gains mean what they say regardless of how the source file was
        # mastered (Freesound files vary wildly: quiet wind beds vs near-full-scale
        # crackle transients). Without this the mix lands ~30 dB crest and the final
        # loudness stage has to crush it. aformat pins rate/layout (loudnorm
        # internally upsamples to 192k, which breaks graph negotiation otherwise).
        filt.append(f"[{i}:a]loudnorm=I=-20:TP=-3:LRA=8,"
                    f"aformat=sample_rates=48000:channel_layouts=stereo,"
                    f"volume={layer.get('gain', 1.0)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(present)))
    fc = (";".join(filt) +
          f";{mix}amix=inputs={len(present)}:normalize=0:duration=shortest,"
          f"alimiter=limit=0.95[out]")
    _run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
          "-t", str(unit_seconds), "-c:a", "pcm_s16le", str(out)])
    return out


def merge_audio_layers(cfg: dict, scene: dict) -> list[dict]:
    """A scene's bed = its FOCAL sound(s) + its SEASON's ambient palette.
    Season comes from weather_map[weather].season; palette from cfg.season_audio.
    e.g. a summer campfire = fire (focal) + crickets/frogs/lake (summer palette).
    Channels without season_audio just use the scene's explicit audio_layers."""
    layers = list(scene.get("audio_layers") or [])
    weather = scene.get("weather")
    season = (cfg.get("weather_map", {}).get(weather, {}) or {}).get("season")
    palette = (cfg.get("season_audio", {}) or {}).get(season, [])
    have = {l["el"] for l in layers}
    for p in palette:
        if p["el"] not in have:
            layers.append(p)
    return layers


def _measure_loudness(src: Path, lufs: float, tp: float, lra: float) -> dict:
    """loudnorm analysis pass: returns the measured input_* values as a dict.
    (Single-pass loudnorm guesses; feeding these back in pass 2 makes it exact.)"""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src),
         "-af", f"loudnorm=I={lufs}:TP={tp}:LRA={lra}:print_format=json",
         "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[\s\S]*\}", proc.stderr[-2500:])
    if not m:
        raise RuntimeError(f"loudnorm measurement failed for {src}")
    return json.loads(m.group(0))


def make_seamless_audio(bed: Path, out: Path, xfade: float, lufs: float,
                        tp: float = -1.5, lra: float = 6) -> Path:
    """Seamless audio loop unit + ACCURATE loudness normalization. Wraps the bed's
    end into its start so a stream_loop has no audible seam (see make_seamless_video
    for the technique), then hits the LUFS target with a measured TWO-PASS loudnorm.

    Why two passes + pre-gain (2026-07 fix): the SFX bed is mixed at sleep-safe
    layer gains, so it lands VERY quiet (≈ -30 LUFS). Single-pass loudnorm lifting
    +14 dB both undershoots the target and lets true peaks through. Fix: (a) if the
    gap to target is large, pre-gain with a true-peak limiter to restore headroom;
    (b) run loudnorm with measured_* values + linear=true so the result is exact
    (±0.5 LU) with dynamics intact and TP hard-capped.

    NOTE: acrossfade starves if both inputs are atrim branches of the same source,
    so head/tail are extracted to temp WAVs first (crossfading two files is robust)."""
    d = _probe_duration(bed)

    # --- 1) build the seamless unit (uncompressed; normalize AFTER the fade) ---
    unit = out.with_name("_aunit.wav")
    if xfade <= 0 or d <= 2 * xfade + 0.1:
        _run(["ffmpeg", "-y", "-i", str(bed), "-c:a", "pcm_s16le", str(unit)])
    else:
        head = out.with_name("_ahead.wav")
        tail = out.with_name("_atail.wav")
        _run(["ffmpeg", "-y", "-i", str(bed), "-t", str(xfade), "-c:a", "pcm_s16le", str(head)])
        _run(["ffmpeg", "-y", "-ss", str(xfade), "-i", str(bed), "-c:a", "pcm_s16le", str(tail)])
        _run(["ffmpeg", "-y", "-i", str(tail), "-i", str(head),
              "-filter_complex", f"[0:a][1:a]acrossfade=d={xfade}:c1=tri:c2=tri[a]",
              "-map", "[a]", "-c:a", "pcm_s16le", str(unit)])

    # --- 2) condition: tame crest just enough that a LINEAR lift fits the TP cap ---
    # The bed mixes at sleep-safe layer gains -> very quiet loudness (~ -30 LUFS) but
    # near-full-scale crackle transients. Lifting to target would smash the TP ceiling,
    # so: compress ONLY the top transients (peak mode, adaptive threshold), apply the
    # lift, and catch strays with an OVERSAMPLED limiter (192k ~= true-peak-aware).
    # For sleep content this transient taming is a feature: no crackle may startle.
    m = _measure_loudness(unit, lufs, tp, lra)
    staged = unit
    needed = lufs - float(m["input_i"])          # dB of loudness lift required
    if needed > 1.0:
        headroom = (tp - 1.0) - float(m["input_tp"])   # safe gain before the cap
        excess = needed - headroom                     # transient dB to tame
        chain = []
        if excess > 0:
            # Backstop only (elements are pre-normalized in build_sfx_bed, so the
            # crest should already be sane): compress transients sitting >14 dB
            # above program loudness, gently.
            thr = 10 ** ((float(m["input_i"]) + 14.0) / 20)
            chain.append(f"acompressor=threshold={max(min(thr, 0.9), 0.001):.6f}"
                         f":ratio=4:attack=3:release=200:knee=6")
        ceiling = 10 ** ((tp - 0.5) / 20)
        chain += [f"volume={needed - 0.5:.2f}dB",
                  "aresample=192000",
                  f"alimiter=limit={ceiling:.6f}:attack=2:release=120:level=false",
                  "aresample=48000"]
        pre = out.with_name("_apre.wav")
        _run(["ffmpeg", "-y", "-i", str(unit), "-af", ",".join(chain),
              "-c:a", "pcm_s16le", str(pre)])
        staged = pre
        m = _measure_loudness(staged, lufs, tp, lra)

    # --- 3) exact loudnorm: measured two-pass, verify-and-correct (max 3 passes) ---
    # linear=true is transparent but clamps gain at the TP ceiling, which can leave
    # the result short of target; each extra pass closes the remaining gap on the
    # already-TP-capped signal, so this converges in 1-2 passes in practice.
    cur = staged
    for i in range(3):
        m = _measure_loudness(cur, lufs, tp, lra)
        if abs(float(m["input_i"]) - lufs) <= 0.7 and float(m["input_tp"]) <= tp + 0.1:
            break
        # Aim 0.7 dB under the TP cap inside the pass: loudnorm limits at its
        # internal 192k rate, and the resample back to 48k overshoots ~0.5-1 dB.
        norm = (f"loudnorm=I={lufs}:TP={tp - 0.7}:LRA={lra}:linear=true"
                f":measured_I={m['input_i']}:measured_TP={min(float(m['input_tp']), 0.0)}"
                f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
                f":offset={m['target_offset']}")
        nxt = out.with_name(f"_anorm{i}.wav")
        _run(["ffmpeg", "-y", "-i", str(cur), "-af", norm, "-ar", "48000",
              "-c:a", "pcm_s16le", str(nxt)])
        cur = nxt
    # --- 4) encode with codec headroom, verify the ENCODED file ---
    # AAC reconstruction overshoots true peak on crackle-like transients (+1..2 dB),
    # so limit the WAV ~1.5 dB below the cap first, then check the actual .m4a;
    # if the codec still overshot, tighten the ceiling 1 dB and re-encode once.
    for margin in (1.5, 2.5):
        ceiling = 10 ** ((tp - margin) / 20)
        lim = out.with_name("_alim.wav")
        _run(["ffmpeg", "-y", "-i", str(cur), "-af",
              f"aresample=192000,alimiter=limit={ceiling:.6f}:attack=2:release=120:level=false",
              "-ar", "48000", "-c:a", "pcm_s16le", str(lim)])
        _run(["ffmpeg", "-y", "-i", str(lim), "-c:a", "aac", "-b:a", "256k", str(out)])
        if float(_measure_loudness(out, lufs, tp, lra)["input_tp"]) <= tp + 0.1:
            break
    return out


def kenburns_from_still(still: Path, out: Path, cfg: dict, seconds: int) -> Path:
    """Make a gently zooming clip from a single still (fallback when there's no motion clip)."""
    a = cfg["assembly"]
    frames = seconds * a["fps"]
    zoom = f"zoompan=z='min(zoom+{a['kenburns_zoom_per_frame']},{a['kenburns_max_zoom']})'" \
           f":d={frames}:s={a['width']}x{a['height']}:fps={a['fps']}"
    _run(["ffmpeg", "-y", "-loop", "1", "-i", str(still),
          "-vf", zoom, "-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    return out


def loop_video_with_black_tail(unit: Path, out: Path, seconds: int, cfg: dict) -> Path:
    """CK format decision (2026-07-12): the visual plays for the first N minutes, then a
    gentle fade to black; the rest of the video is a black screen while the audio
    continues. Serves sleepers: no glare, battery-friendly, matches the niche convention.
    Composition (all segments share codec params so concat is stream-copy):
      [visual: unit stream-looped to N min] + [fade: unit re-encoded with fade-out]
      + [black: 60s black unit stream-looped for the remainder].
    The seamless unit ends on its own start frame, so the fade segment (which starts at
    the unit's start) continues the motion without a jump. Falls back to a plain loop
    when disabled or when the target is shorter than visual+fade."""
    a = cfg["assembly"]
    bt = a.get("black_tail") or {}
    vis_s = int(bt.get("visual_minutes", 15)) * 60
    fade_s = float(bt.get("fade_seconds", 4))
    if not bt.get("enabled") or seconds <= vis_s + fade_s + 60:
        return loop_to_length(unit, out, seconds)

    work = out.parent
    fps = a.get("fps", 30)
    # 1) visual head (lossless loop)
    head = work / "_bt_head.mp4"
    loop_to_length(unit, head, vis_s)
    # 2) fade segment: first fade_s of the unit, fading to black (same encode params
    #    as make_seamless_video so concat -c copy accepts it)
    fade = work / "_bt_fade.mp4"
    _run(["ffmpeg", "-y", "-i", str(unit), "-t", str(fade_s),
          "-vf", f"fade=t=out:st=0:d={fade_s}",
          "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
          "-an", str(fade)])
    # 3) black unit (60s, encoded once) -> looped to the remainder
    width, height = a.get("width", 1920), a.get("height", 1080)
    black_unit = work / "_bt_black_unit.mp4"
    _run(["ffmpeg", "-y", "-f", "lavfi", "-i",
          f"color=c=black:s={width}x{height}:r={fps}", "-t", "60",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(black_unit)])
    black = work / "_bt_black.mp4"
    remainder = max(1, int(seconds - vis_s - fade_s))
    loop_to_length(black_unit, black, remainder)
    # 4) concat all three, stream copy
    lst = work / "_bt_concat.txt"
    lst.write_text("".join(f"file '{f.name}'\n" for f in (head, fade, black)))
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
          "-c", "copy", str(out)])
    return out


def loop_to_length(clip: Path, out: Path, seconds: int) -> Path:
    """stream_loop the source clip up to `seconds` with no re-encode."""
    _run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clip),
          "-t", str(seconds), "-c", "copy", str(out)])
    return out


def mix_narration_over_bed(narration: Path, bed: Path, out: Path, bed_gain: float) -> Path:
    fc = (f"[0:a]volume=1.0[n];[1:a]volume={bed_gain}[b];"
          f"[n][b]amix=inputs=2:duration=longest[out]")
    _run(["ffmpeg", "-y", "-i", str(narration), "-i", str(bed),
          "-filter_complex", fc, "-map", "[out]", "-c:a", "aac", "-b:a", "192k", str(out)])
    return out


def mux(video: Path, audio: Path, out: Path) -> Path:
    """Combine looped video + looped audio, ending at the shorter stream.
    Both inputs are already encoded, so copy both streams = near-instant mux."""
    _run(["ffmpeg", "-y", "-i", str(video), "-i", str(audio),
          "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
          "-shortest", "-movflags", "+faststart", str(out)])
    return out


def _resolve_seconds(slug: str, cfg: dict, variant: str) -> int:
    """Fixed HOURS variant, or an ORGANIC length from config (target_seconds +/- jitter).
    Jitter is seeded per-slug so a given channel's length is stable across re-runs but
    never an exactly-round number (avoids the 'suspiciously exact 3:00:00' tell)."""
    if variant in HOURS:
        return HOURS[variant]
    lf = cfg.get("longform", {})
    base = int(lf.get("target_seconds", HOURS["3h"]))
    jitter = int(lf.get("jitter_seconds", 0))
    if jitter:
        rng = random.Random(hashlib.sha256(f"{slug}:{variant}".encode()).hexdigest())
        base += rng.randint(-jitter, jitter)
    return base


def assemble(slug: str, variant: str = "3h") -> Path:
    cfg = load_channel(slug)
    dirs = output_dirs(cfg)
    raw = dirs["raw"]
    plan = json.loads((raw / "plan.json").read_text(encoding="utf-8-sig")) if (raw / "plan.json").exists() else {}

    seconds = _resolve_seconds(slug, cfg, variant)
    a = cfg["assembly"]
    work = raw / "_work"
    work.mkdir(exist_ok=True)

    seamless = cfg.get("longform", {}).get("seamless_loop", False)
    lufs = cfg.get("audio", {}).get("loudness_lufs", a.get("default_loudness_lufs", -14))
    scene = next((s for s in cfg.get("scene_pool", []) if s["id"] == plan.get("scene_id")), {})

    # --- video base: prefer the motion clip, else Ken Burns the still ---
    if (raw / "scene.mp4").exists():
        base_clip = raw / "scene.mp4"
    elif (raw / "scene.png").exists():
        base_clip = kenburns_from_still(raw / "scene.png", work / "kenburns.mp4", cfg, 20)
    else:
        raise FileNotFoundError(
            f"No scene.mp4 or scene.png in {raw}. Fulfill the generation manifest first."
        )
    # Particle overlay (material variation, locked-camera era): composite a looping
    # rain/snow/spark element onto the short unit if one is configured + present.
    ov = _find_overlay(cfg, scene)
    if ov:
        po = cfg["assembly"].get("particle_overlay", {})
        base_clip = apply_particle_overlay(
            base_clip, ov, work / "video_overlaid.mp4",
            po.get("opacity", 0.5), po.get("blend", "screen"), a["fps"])
        print(f"[assemble] particle overlay: {ov.name} @ {po.get('opacity', 0.5)}")
    # Seamless loop unit: crossfade the wrap so the seam is invisible across hours.
    if seamless:
        base_clip = make_seamless_video(
            base_clip, work / "video_unit.mp4", a["loop_video_xfade_seconds"], a["fps"])
    looped_v = loop_video_with_black_tail(base_clip, work / "video_long.mp4", seconds, cfg)

    # --- audio base (seamless unit + loudness-normalized) ---
    # Prefer building the bed from reusable SFX elements at per-scene levels; fall
    # back to a ready-made bed.wav dropped in the raw dir.
    bed = raw / "bed.wav"
    audio_cfg = cfg.get("audio", {})
    layers = merge_audio_layers(cfg, scene)   # `scene` resolved above
    if layers and audio_cfg.get("sfx_library"):
        sfx_dir = ROOT / audio_cfg.get("sfx_dir", "assets/sfx")
        try:
            bed = build_sfx_bed(layers, audio_cfg["sfx_library"], sfx_dir, work / "bed_sfx.wav",
                                unit_seconds=a.get("bed_unit_seconds", 480))
        except FileNotFoundError as e:
            if not bed.exists():
                raise
            print(f"[assemble] SFX layers unavailable ({e}); using bed.wav")
    if not bed.exists():
        raise FileNotFoundError(f"No SFX elements and no bed.wav in {raw}.")
    audio_unit = make_seamless_audio(
        bed, work / "audio_unit.m4a",
        a["loop_audio_xfade_seconds"] if seamless else 0.0, lufs,
        tp=a.get("loudness_true_peak", -1.5), lra=a.get("loudness_range", 6))
    looped_a = loop_to_length(audio_unit, work / "audio_long.m4a", seconds)

    if plan.get("narration_enabled") and (raw / "narration.wav").exists():
        looped_a = mix_narration_over_bed(
            raw / "narration.wav", looped_a, work / "audio_mixed.m4a",
            cfg["audio"].get("bed_gain", a["bed_gain_under_narration"]))

    out = dirs["pending_review"] / f"{slug}__{plan.get('scene_id','scene')}__{variant}.mp4"
    mux(looped_v, looped_a, out)
    print(f"[assemble] -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("channel")
    ap.add_argument("--variant", default="3h", choices=list(HOURS))
    args = ap.parse_args()
    assemble(args.channel, args.variant)
