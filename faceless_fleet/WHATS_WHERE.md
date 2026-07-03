# What changed & where everything lives

A map of the whole `faceless_fleet/` project + a changelog of this session, so any new
session (Cowork especially) can orient fast. Repo: **`Rebadged/Faceless_fleet`**, default
branch **`main`**, with the `faceless_fleet/` package at the repo root (so commands run as
`python -m faceless_fleet.pipeline.run …`). *(Migrated 2026-07 out of a feature branch of
`polymarket-alpha`, where it was easy to lose — see note at the bottom.)*

## Read in this order
1. **`COWORK_HANDOFF.md`** — mission, what Cowork unblocks, accounts/assets, the ordered playbook.
2. **`START_HERE.md`** — master runbook (two-loop model → launch a channel → cron).
3. **`research/CROSS_REFERENCE_2026.md`** — the resolved decisions + corrected credit math + economics. READ before generating/uploading.
4. **`BRANDING.md`** — the brand/thumbnail system + compliance checklist.

---

## This session — what changed (newest first)

### 2026-07-01 (Instance 2 — channels 2 & 3)
- **Campfire/Tent branding regenerated:** all four 2026-06-26 assets were defective on
  zoom inspection (both banners: baked-in YouTube player UI / play-button logo, from
  "YouTube banner" phrasing + inline "no X" lists; both avatars: scene-inside-a-circle
  vignette, tent avatar also had gibberish canvas text). Regenerated with positive-only
  prompts per the validated 2026-07-01 lessons. **Final job IDs** — Campfire avatar
  `559ef24e-70e3-4b7c-a06d-d09f653e1bc0`, Campfire banner `7f473e86-db00-4353-8015-2fa05b400495`,
  Tent avatar `a8c5eafc-8845-4e42-8fe0-65b2966d0892`, Tent banner
  `90514c64-a9e0-4b41-9c7a-0803b3d49c48`. ~1.4 cr total (14 stills, no video). Finals
  downloaded to CK's machine (banners upscaled to 2560×1440); alternates kept in the
  Higgsfield library.
- **Channels:** creation pack (names, handles, verbatim bios, step list) handed to CK —
  he creates the Brand Accounts; handles + `youtube_channel_id` will be written back into
  `campfire.yaml` / `camping_tent.yaml` once created.

### 2026-07-03 (Fable session — look lock)
- **The Look locked by CK** after a reference-driven lookdev round (his 6 refs + 8 generated
  stills + 8 clips): fire-light-only, casual fires, opaque tents, wind-alive motion,
  wilderness-only audio. Rules in `BRANDING.md` §The Look; 6 approved scenes added across
  all three channel configs with validated prompts + Higgsfield job IDs.
- Sample verdicts: Fall 4-min sample approved earlier; of the 5-video batch CK kept the
  original Fall one and retired the rest as look-drift. Long renders wait until the first
  library is rebuilt on the locked look.
- Next: audio sourcing pass (wilderness-only, per-element listening previews), then rebuild
  the clip library on approved scenes, then 1h/8h/12h renders -> OAuth -> first upload.

### 2026-07-01 (Fable session)
- **Fall launch pivot (CK):** start with autumn/rain, not winter — richer audio palette
  (rain + distant thunder + fire crackle; wind was too dominant). New hero scene
  `rainy_cabin_autumn` in `rain_cabin.yaml`; validated still + 5s clip generated; 4-min
  sample approved by CK.
- **Loudness chain rebuilt** (`assemble.py`): per-element loudnorm before mixing,
  adaptive transient conditioning, measured two-pass loudnorm (verify-and-correct loop),
  oversampled limiting + codec-headroom AAC encode. Verified: −16.6 LUFS / TP −3.0 /
  LRA 1.4 (was −21.7 with true-peak clipping). Cabin `loudness_lufs: -16` (CK decision).
- **Prompt lessons (validated on renders):** soul_2 has NO negative channel — inline
  "no X" lists inject X (foreground trunks); "like a fire dancing inside" renders literal
  flames; timid motion prompts ("gentle/subtle") make Kling near-static (0.0% pixel
  change). Scene prompts now positive-only with explicit multi-element motion;
  `generate.py` no longer appends `identity.negative` to prompts.
- **Brand framing (CK):** the painterly look is owned as "handcrafted" in bios + video
  descriptions (all 3 channels + BRANDING.md policy note). Live @CabinComforts bio updated.
- **State:** Cabin Comforts channel is live + branded (`UCbayo4s0nrP0-n2iagNDBQw`);
  SFX fetched (5 cabin elements); OAuth client creds in CK's local `CK.env` (no refresh
  token yet); next: 8h render → OAuth → first scheduled upload.

**Decisions baked in** (`e074c30`):
- **5s master clips** (`clip_seconds: 5`, `est_credits_per_clip: 9`) — video isn't the star; halves credit cost, loops just as invisibly.
- **Camera essentially locked** (barely-perceptible drift max) across all 3 channels; motion lives in the scenery.
- **No Suno** — pure ambience now; audio deep-dive re-scoped to *safe audio now + custom/original audio long-term*.

**Build fixes & new capabilities:**
- **Particle-overlay step** (`a98995d`) — `assemble.apply_particle_overlay()` composites a looping rain/snow/spark element over the clip for per-video variation (the inauthentic-policy lever now that the camera's locked). Drop CC0 overlays in `assets/overlays/<weather>.mov` to activate; skips silently if absent. ffmpeg filter verified.
- **Credit math corrected** (`f4db6b4`) — was `est: 8`, reality ≈ 9 cr/5s + ~3× iteration. `batch_plan` now plans on raw cost and reports worst-case.
- **Hidden YouTube upload cap** (`f4db6b4`) — `upload.max_uploads_per_day: 5` (unverified projects get silent 429 at ~7–11/day; verify the project to lift to 100).
- **Credit & cadence economics** (`e553e61`) — the **clips ≠ videos** reframe (videos are ~free to assemble; credits only buy library breadth; `batch_plan` self-limits to missing clips). In `CROSS_REFERENCE_2026.md`.

**Automation built earlier this session:**
- **Weekly orchestrator** (`01a6ac7`, `5049c7f`) — `weekly.py` publishes every connected channel; restock runs as a weekly Claude scheduled session + a git URL bridge (`restock.py`).
- **Unattended Cloud-API restock** (`fff88c2`, `9fe94e0`) — `rest.py` + `restock-run`; needs the 2 Cloud-API model slugs confirmed (use `deploy/probe_slugs.py`, see `deploy/REST_SMOKE_TEST.md`).

**Research ingested:**
- **Branding** (`efb02b8`) — `research/BRANDING_PLAYBOOK.md` + distilled into `BRANDING.md` (thumbnail system, fonts, material-variation compliance checklist).
- **2026 strategic validation** (`f4db6b4`) — `research/2026_*` sources + `CROSS_REFERENCE_2026.md`.
- **Research backlog** (`c09a4ec`) — `research/RESEARCH_BACKLOG.md` (open deep-dives) + the **2am-deweighting rule**.

---

## Repo map (every file, one line)

### Top-level docs
| File | What |
|---|---|
| `COWORK_HANDOFF.md` | **The brief for Cowork** — mission, playbook, gotchas, security. |
| `START_HERE.md` | Master runbook: launch a channel, go live, cron. |
| `WHATS_WHERE.md` | This file. |
| `BRANDING.md` | Brand/thumbnail system + avatar/banner specs + compliance checklist. |
| `README.md` | Project overview. |
| `ROADMAP.md`, `FLEET.md`, `AUTONOMY.md`, `LAUNCH_PLAN.md`, `LAUNCH_SLATE.md`, `HANDOFF_REPORT.md` | Strategy/background (some predate the Comforts pivot). |
| `RESEARCH_BRIEF_geography.md` | Location research (cabin/forest geography). |

### `config/`
| File | What |
|---|---|
| `global.yaml` | Fleet defaults: generation (5s/credits), assembly (loudness, loop, **particle_overlay**), upload (cap), auto, policy. |
| `channels/rain_cabin.yaml` | **Cabin Comforts** (ACTIVE) — look, scenes, seasonal audio, bio, metadata, handle. |
| `channels/campfire.yaml` | **Campfire Comforts** (ACTIVE). |
| `channels/camping_tent.yaml` | **Tent Comforts** (ACTIVE). |
| `channels/sleep_ambient.yaml`, `pet_calming_dogs.yaml` | Legacy/alternate-slate configs — **not the active fleet**. |
| `channels/_archive/*` | Archived experiments (2am, meditation). |

### `pipeline/` (the code; CLI is `python -m faceless_fleet.pipeline.run <cmd>`)
| File | What |
|---|---|
| `run.py` | CLI orchestrator: generate / assemble / review / approve / upload / auto / weekly / batch-plan / restock-record / restock-fetch / restock-run / fetch-sfx / channels. |
| `config.py` | Load + deep-merge global + per-channel YAML. |
| `generate.py` | Build Higgsfield job specs (still/motion prompts) + titles. |
| `assemble.py` | **ffmpeg core**: seamless video loop, SFX bed, loudnorm, **particle overlay**, mux. |
| `auto.py` | Zero-touch single run: pick clip → bed → assemble → approve → upload. |
| `weekly.py` | Weekly orchestrator (every connected channel; fetches new clips first). |
| `batch_plan.py` | Budgeted "what clips are missing" manifest (self-limiting). |
| `restock.py` | Clip transport: record URLs → `restock/<slug>.json`; `fetch_pending` downloads. |
| `rest.py` | Unattended Cloud-API restock (`restock-run`, needs `HIGGSFIELD_API_KEY` + slugs). |
| `sfx_fetch.py` | Freesound CC0 SFX downloader (`fetch-sfx`). |
| `review.py` | Human review gate + policy/material-variation checks. |
| `upload.py` | YouTube OAuth (`--auth`) + scheduled (private + publishAt) upload. |
| `schedule.py`, `state.py` | Publish-time scheduling helpers + per-channel rotation state. |
| `higgsfield_client.py` | Earlier Higgsfield API helper (the Cloud-API path now lives in `rest.py`). |

### `deploy/`
| File | What |
|---|---|
| `crontab.example` | The VPS cron — one `weekly` line (git-pulls first). |
| `RESTOCK_SCHEDULE.md` | Weekly restock: scheduled session + git URL bridge + budgets. |
| `COWORK_RESTOCK.md` | Paste-able Cowork prompt to fulfil a clip manifest. |
| `REST_SMOKE_TEST.md` | Confirm the Cloud-API model slugs on a real-internet box + 1-clip test. |
| `probe_slugs.py` | Auto-discover the slugs + generate the first clip (`--write`). |
| `GOOGLE_CLOUD_OAUTH_SETUP.md`, `YOUTUBE_AUTH_PHONE.md` | YouTube OAuth setup (desktop + phone). |
| `run_channel.sh`, `fetch_and_assemble.sh`, `stock_clips.py` | Helper scripts. |

### `research/`
| File | What |
|---|---|
| `2026_fleet_research_dossier.pdf` | The original research dossier (source). |
| `2026_strategic_validation_canada.md` | Second-model 2026 validation (source). |
| `CROSS_REFERENCE_2026.md` | **Reconciliation vs our build**: resolved decisions, corrected credit math, clips≠videos economics, action table. |
| `BRANDING_PLAYBOOK.md` | Branding/visual-identity research (full). |
| `RESEARCH_BACKLOG.md` | Open deep-dives (audio, SEO, growth/live/Shorts, monetization+tax). |

### `restock/`
| File | What |
|---|---|
| `README.md` + `<slug>.json` (generated) | Clip-URL manifests written by the scheduled session, pulled by the VPS. |

### Not in git (gitignored, machine-local)
`output/` (renders), `assets/` (clips, sfx, **overlays**), `secrets/`, `client_secret*.json`, `token*.json`, env vars (API keys, refresh tokens).

---

## The two research files
Both are committed under `research/` (`2026_fleet_research_dossier.pdf`,
`2026_strategic_validation_canada.md`), and reconciled in `CROSS_REFERENCE_2026.md`. When
handing off to Cowork you can also attach the originals directly — but they're already in
the repo, so a clone has them.

## Current state (what's done / pending)
- ✅ Pipeline, branding system, compliance checklist, weekly + REST restock, probe, particle overlay.
- ✅ Decisions resolved: 5s clips, locked camera + overlays, no Suno. Credit math corrected.
- ⏳ **Pending (needs Cowork/PC/VPS):** create + brand the 3 channels; add SFX (`assets/sfx/`) + overlay (`assets/overlays/`) assets; generate the first clip library; YouTube OAuth + first upload; confirm the 2 Cloud-API slugs (`probe_slugs.py`); set up the VPS for unattended scheduling.
- ⏳ **Open deep-dives** (`research/RESEARCH_BACKLOG.md`): audio (safe + custom), SEO, growth/live/Shorts, monetization + CA tax.

## Repo migration note (2026-07)
This project was moved from a feature branch of `Rebadged/polymarket-alpha` (a wallet-tracker
repo — where an agent once thought the fleet was "lost") into its own repo
**`Rebadged/Faceless_fleet`** (default branch `main`). The `faceless_fleet/` package is kept
at the repo root so every `python -m faceless_fleet.pipeline.run …` command and import still
works unchanged — the only difference is the clone URL. Point Cowork, Fable, and the VPS at
`Rebadged/Faceless_fleet` going forward; the old branch is retired. Live assets (Higgsfield
clips, branding, sample video) and `CK.env` were never in git and don't move with the repo.
