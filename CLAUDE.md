# CLAUDE.md — Faceless_fleet

Context for any Claude instance in this repo. **Read `faceless_fleet/WHATS_WHERE.md` next**
(live map + changelog — it outranks this file when they disagree), and load the
**`faceless-fleet` skill** if installed (distilled playbooks; source in `skill/`).

## What this is

A review-gated, config-driven pipeline producing faceless AI ambient/relaxation videos for
independent YouTube channels, monetized by ad/watch revenue. Operator **CK** (solo,
Vancouver Island BC) is the **human quality gate** — AI generates, code assembles and
schedules, CK approves what publishes. No merch, no character IP, no shared brand.

**Active fleet ("Comforts"):** Cabin Comforts (`rain_cabin`, LIVE: `UCbayo4s0nrP0-n2iagNDBQw`
@CabinComforts — lead, prove first) · Campfire Comforts (`campfire`) · Tent Comforts
(`camping_tent`). Legacy configs (`sleep_ambient`, `pet_calming_dogs`) are not the active
slate. Launch staging: brand all now; Cabin uploads first; others trickle after Gate A.

## Locked constraints (do NOT relitigate)

- **Stack:** Higgsfield via MCP (`soul_2` stills ~0.1 cr; `kling3_0_turbo` 5s/720p ~7.5-9 cr,
  ~3× iteration) + **pure CC0 SFX beds (NO Suno** — decision 2026-06) + ffmpeg seamless
  loops at **−16 LUFS / TP −1.5 / LRA 6** (measured two-pass chain in `assemble.py`) +
  YouTube Data API (private + jittered `publishAt`) + VPS runtime + human review gate.
- **Budget:** ~$100 CAD/mo. **Clips ≠ videos:** credits buy clip-library breadth; videos
  assemble ~free (lossless stream-copy loops).
- **Upload cap:** ≤5/day per Cloud project (hidden 2026 "Video Uploads" bucket 429s
  unverified projects at ~7-11/day; verification lifts to 100). Never shard projects (ToS).
  Never call `search.list` at runtime.
- **Platforms:** YouTube-first; Facebook Reels secondary; TikTok/IG reach-only (TikTok
  Creator Rewards excludes Canada). **Growth:** organic only. **Camera:** locked; motion
  lives in the scene elements + particle overlays. **Look:** stylized painterly "handcrafted"
  brand framing (see BRANDING.md).

## The rule that governs everything

YouTube's **July 15, 2025 "inauthentic content" policy** demonetizes templated, low-variation
mass content **channel-wide**. Material variation per video (scene/location × audio bed ×
title/metadata + particle overlays) is enforced by `review.py`. AI is allowed and
monetizable — the line is sameness, not AI.

## Validated production lessons (2026-07 — follow, don't rediscover)

- `soul_2` has **no negative-prompt channel**: inline "no X" lists inject X. Positive-only
  prompts; `identity.negative` is the review checklist.
- "like a fire dancing inside" → literal flames. "windows glowing with soft warm amber
  light from deep inside."
- Kling under-animates timid wording → explicit multi-element motion prompts ("heavy rain
  in clearly visible streaks… reflections rippling… smoke drifting"); serene water scenes
  need heavy-rain energy or they render static.
- Audio: normalize each element to −20/−3 before mixing; leave 1.5-4 dB codec headroom
  (AAC overshoots true peak on crackle/cricket transients).
- **Fall-first launch** (CK): rain + distant thunder + fire crackle beds; wind-heavy mixes
  rejected; winter later.

## Environment / runtime

Cowork desktop sessions CAN download Higgsfield media + run ffmpeg (proven). Claude Code
WEB sandboxes get 403 on the CDN — drive generation only. Unattended loop = VPS cron
(`weekly`). Clone the repo into the sandbox HOME, not the mounted folder (git locks fail
on the mount). GitHub PAT: `Projects\Youtube\gh_token.txt.txt` on CK's machine.

## Commands

```bash
python -m faceless_fleet.pipeline.run channels | generate | assemble | review | approve |
  upload | auto | weekly | batch-plan | restock-record | restock-fetch | restock-run | fetch-sfx
```

Flow: generate → assets → assemble (ffmpeg) → `output/pending_review/` → CK approves →
`approved/` → upload (private + `publishAt`). Secrets: env vars / local `.env` only —
never chat, never git (§8 of COWORK_HANDOFF.md).

## Verify before stating as fact (fast-moving)

Ambient RPM ranges · Higgsfield pricing/models · Spotify functional-noise + 1,000-stream
rules · SOCAN AI-eligibility · 12h live-archive limit (18h+ = archive deleted) · Facebook
Content Monetization eligibility · Canadian tax (W-8BEN Article XII 0%, GST/HST $30k
incl. zero-rated exports — accountant for specifics).

## Working with CK

Direct, realistic, downside-surfaced. No hype. Ranges over false precision. Check before
anything that publishes or spends real credits. Batch questions; don't over-ask.
