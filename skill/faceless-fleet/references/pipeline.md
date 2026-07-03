# Pipeline — Stack, Where Things Live, Automation

Operational reference for building and running the production pipeline. Division of labor: **Claude Code builds/maintains the deterministic pipeline; deterministic code runs the unattended loop; a human gate sits before publish.** No fully-autonomous "generate → auto-publish" loop — keep publishing behind reviewed, deterministic code.

## Tool stack & where everything lives

| Component | Tool | Cost (verify) | Credential / location |
|---|---|---|---|
| Motion video (the new capability) | **Higgsfield** (Plus ~1,000 credits/mo) | image ~0.12 cr, Kling 3.0 turbo 5s/720p ~7.5 cr → ~8–25 cr/video | Hosted **MCP** (auth by account, billed in credits, no API keys). Ensure the MCP is connected to the UPGRADED workspace (a wrong-workspace connection shows free/0 credits) |
| Stills | **Flux Pro on fal.ai** | ~$0.04/megapixel | `FAL_KEY` env var (fal.ai → Keys) |
| Audio bed | **CC0 SFX (Freesound API)** | free | `FREESOUND_API_KEY` env var; `run fetch-sfx`. NO Suno (CK decision 2026-06) |
| Audio assembly | **Python/pydub** | free | VPS |
| Video assembly + looping | **ffmpeg** | free | VPS (replaced DaVinci Resolve) |
| Upload | **YouTube Data API v3** | free (quota-limited) | Google Cloud project + OAuth 2.0 (Desktop) + stored **refresh token**; scope `youtube.upload` |
| Cross-post (reach) | scheduler (e.g. self-hosted Postiz, or Upload-Post) | free/low | TikTok/IG/FB reach-only for Canada |
| Runtime | **VPS** (open egress) | ~$5–12/mo | Runs downloads + ffmpeg + 24/7 streaming |
| Orchestration | Claude Code + VPS cron / GitHub Actions | free | See below |

**Environment reality:** Claude Code WEB sandboxes block the Higgsfield CDN (403) — they can drive generation but not download. **Cowork desktop sessions CAN download and run ffmpeg** (proven: the whole 2026-07 sample batch). Production runtime is still the VPS for unattended loops. Repo: `Rebadged/Faceless_fleet` (private, main) — clone into the sandbox home, not the mounted folder (git locks fail on the mount); GitHub PAT at `Projects\Youtube\gh_token.txt.txt` on CK's machine.

## Assembly & looping (ffmpeg)

- **Lossless short→long loop:** `ffmpeg -stream_loop -1 -i clip.mp4 -c copy -t 36000 out.mp4` (stream-copy, no re-encode — a 3h build in ~60s). `-stream_loop 9` turns 1h into 10h in seconds.
- **Video crossfade:** `xfade=transition=fade:duration=5:offset=<t>`. **Ken Burns:** `zoompan=z='min(zoom+0.0005,1.5)':d=<frames>:s=1920x1080` — motion is standard (static stills depress average view duration).
- **Audio crossfade/loop:** pydub `combined.append(audio, crossfade=ms)`; ffmpeg `acrossfade=d=<sec>`; `aloop`/`amix` to layer stems. Keep WAV through the pipeline; compress only at final upload. Verify audio file size before muxing.
- **Seamless loops:** cut at zero-crossings; layer stems of mutually-prime lengths so the texture doesn't obviously repeat. Master sleep quieter (~-16 to -18 LUFS, not -14). Detail in `references/audio.md`.
- **Build an "outro plate"** (visual quiet in the right two-thirds for the last ~20s) into the loop so end screens have somewhere to sit (see `references/seo.md`).

## Upload & scheduling

- Upload **Private** first (`privacyStatus="private"`), optionally `publishAt` (ISO-8601) for scheduled release. CK reviews → publish. Channel must be phone-verified. Store and reuse the **refresh token** (access tokens regenerate from it).
- **Anti-spam:** bulk *uploading* is fine; bulk *same-day publishing* is the risk. Drip on a consistent-but-organic cadence; **jitter `publishAt`** by tens of minutes; ≥~20h between a channel's uploads; vary metadata per video.
- **YouTube quota (VERIFY):** `videos.insert` long cited at 1,600 units against 10,000/day (~6 uploads/day); one source reports a Dec 2025 cut to ~100. Check the live Quota Calculator. Failed uploads don't consume quota. **Do NOT shard into many Cloud projects to multiply the free quota — ToS violation, can suspend all projects.** Safer: one project + audited increase, or one project per genuinely-owned Google account.
- **Cross-platform APIs:** TikTok Content Posting API tokens expire every **24h** (refresh proactively; refresh token lasts 365 days), unaudited clients are private-only, ~15 posts/day cap, set `is_aigc=true`. Reach-only for Canada, so native posting usually beats API. IG via Graph API (container publish). 

## Orchestration (Claude Code / Cowork)

- **Recommended substrate:** VPS **cron** (most durable) runs generate→assemble nightly + a jittered upload cron + a daily token-refresh job. Free alternatives: GitHub Actions `schedule:` cron (free unlimited on public repos; private has limited free minutes) — but heavy multi-hour ffmpeg renders blow past runner limits, keep them on the VPS. Never commit OAuth tokens to a public repo (use Actions secrets).
- **Claude Code scheduling primitives (know their limits):** `/loop` and `CronCreate` are session-scoped and **expire in 7 days** (die with the session). Desktop scheduled tasks + Cowork scheduled tasks only fire **while the Desktop app is open and the machine awake**. **Routines** (cloud, Pro/Max/Team) run on Anthropic infra even when the laptop is off, but work on a fresh repo clone + connectors (not local files/MCP) — best for "regenerate metadata / draft next batch / open a PR," NOT "run ffmpeg on a 10-hour render." Headless `claude -p "..." --output-format json` is single-shot; wrap in your own cron/CI. The GitHub Action commits to a branch + gives a PR link (doesn't self-merge — an inherent human gate).
- **Reality:** no documented fully-unattended Claude-Code media-gen-plus-auto-upload loop exists. Keep the review gate + deterministic publishing.

## Reference architecture (recommended)

"Free VPS Cron Factory" (~$5–12/mo + credits): Claude Code (interactive) writes `generate.py` (Suno + fal.ai + Higgsfield MCP), `assemble.py` (stream_loop/xfade/acrossfade/zoompan), `upload.py` (private + jittered publishAt), `schedule.json`, and a per-channel context file. Human gate: review `pending_review/` → `approved/`. VPS cron runs generate→assemble + a jittered upload cron + a daily token-refresh. A self-hosted scheduler fans out reach clips to TikTok/IG/FB. A daily Claude Code Routine reads analytics and opens a review note (interpretive, not publishing).

## The validated "2am without her." pipeline (background)

The proof-of-concept that de-risked all of the above. Same DNA, minus the character.

- **Identity:** "2am without her." (trailing period), @2amWithoutHer; ambient/lo-fi for young men who miss someone / can't sleep; purple-blue night, 35mm, a recurring "girl" character; lowercase longing titles, no emojis.
- **Flow:** Suno music → QC → Flux Pro still (16:9) → Flux Kontext purple grade → QC (character consistency, no AI artifacts, **no visible text on any surface**) → pydub crossfade/loop → ffmpeg combine (fade from black) → upload Private → CK reviews → publish.
- **Two lanes:** Sleep/Emotional (~3h, ultra-slow ambient, no drums, loop to 2:50–2:59 so it's not suspiciously exact) and Study With Me (~20 min, lo-fi groove).
- **Proven results:** live in ~48h; organic YouTube search in 48h; `she felt like home` ~11.1% CTR; strong retention. Midjourney was tried and refunded (too polished); clean purple grade beat heavy VHS/scanlines.
- **Decisions carried forward:** batch-produce then drip-schedule; stagger/randomize; add Ken Burns motion; no text in AI images; material variation per video; human review gate; organic only; durations look organic; CK is the checkpoint, the pipeline does the work.

## Do / avoid

- **Do:** run generation from the sandbox but assembly/upload/streaming from the VPS; store the YouTube refresh token; jitter publish times; keep WAV through the pipeline; verify audio size before muxing; build the outro plate into loops; keep one Cloud project per owned account.
- **Avoid:** sharding Cloud projects to dodge quota (ToS); relying on `/loop`/session cron for anything past 7 days; blind scheduled publishing; looping a single un-varied short clip (policy + quality risk); committing tokens to public repos.
