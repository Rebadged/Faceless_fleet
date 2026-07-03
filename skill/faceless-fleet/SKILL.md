---
name: faceless-fleet
description: "Operating knowledge and playbooks for CK's faceless AI ambient YouTube channel fleet — Cabin Comforts (lead, live), Campfire Comforts, and Tent Comforts — built on Higgsfield motion + CC0 ambient SFX beds + ffmpeg long-form loops + the YouTube Data API + a VPS, with CK as the human review gate. Use this whenever work touches the YouTube/faceless-channel operation: building or automating the video pipeline, audio sourcing and licensing, SEO and titles/metadata, thumbnails and branding, channel growth, cold-start, 24/7 live streams, the Shorts funnel, monetization and RPM, YouTube's July 2025 inauthentic-content policy, or the Canadian tax setup (W-8BEN, GST/HST). Load it before advising on any of these so guidance fits the settled constraints — roughly 100 CAD/month budget, Canada, YouTube-first, Facebook secondary, organic-only — rather than generic advice. Then read the matching file in references/ for the topic at hand."
license: "Proprietary — CK internal use"
---

# Faceless Fleet — Operating Playbook

Working reference for CK's faceless, AI-generated ambient/relaxation YouTube channel fleet. It exists so any Claude instance can pick up the operation already knowing the settled decisions, the stack, where things live, and the rules that govern monetization — instead of re-deriving them or giving generic advice that violates a constraint.

This SKILL.md is the always-loaded overview. Detailed, topic-specific guidance lives in `references/` and should be read on demand (see the routing table). A separate exhaustive research dossier also exists outside this skill for deep cross-referencing; this skill is the distilled working version.

## What the operation is

CK is a technically strong solo creator on Vancouver Island, BC, running a fleet of independent, simply-branded ambient channels monetized purely by ad/watch revenue. AI generates the assets and code assembles and schedules them; **CK is only the human quality-review checkpoint before anything publishes.** No merch, no character IP, no shared brand across channels.

Settled 3-channel launch slate (the "Comforts" fleet — configs in `config/channels/`):
1. **Cabin Comforts** (`rain_cabin`) — rain/storm/snow cozy-cabin. **LIVE + branded:** channel ID `UCbayo4s0nrP0-n2iagNDBQw`, @CabinComforts, phone-verified. The lead: prove it first.
2. **Campfire Comforts** (`campfire`) — crackling fire. Being created/branded (parallel instance).
3. **Tent Comforts** (`camping_tent`) — rain-on-tent. Being created/branded (parallel instance).

(`sleep_ambient` and `pet_calming_dogs` configs are legacy/alternate slate — NOT the active fleet.)
**Launch staging:** brand all three now, but only Cabin uploads at full cadence; Campfire/Tent trickle ~1-2/wk after Cabin is 2–4 weeks clean (Gate A); full cadence after Cabin proves monetization (Gate B / YPP).

## Locked constraints (do NOT relitigate — advise within these)

- **Pipeline:** Higgsfield via MCP (stills `soul_2` ~0.1 cr; motion `kling3_0_turbo` 5s/720p ~7.5-9 cr, ~3× iteration budget) + **pure CC0 ambient SFX beds** (Freesound; **NO Suno** — CK decision 2026-06, music channel ideas parked) + ffmpeg (seamless loops; **-16 LUFS / TP -1.5 / LRA 6**, measured two-pass chain) + YouTube Data API v3 (private + scheduled `publishAt`) + VPS runtime + human review gate.
- **Upload cap:** `max_uploads_per_day: 5` per Cloud project — a hidden 2026 "Video Uploads" bucket 429s unverified projects at ~7-11/day. Verify the Google project to lift to 100/day. Never call `search.list` at runtime (100 units each).
- **Clip economics:** clips ≠ videos. 5s master clips cost credits; videos assemble from the clip library for ~zero credits (lossless stream-copy loops). Credits buy library breadth only.
- **Budget:** ~$100 CAD/month total for all generation credits + tooling.
- **Platforms:** YouTube-first monetization; Facebook Reels / Content Monetization secondary; TikTok and Instagram are **reach-only** (TikTok Creator Rewards excludes Canada — a Canadian earns $0 from it regardless of audience).
- **Location:** Canada (drives monetization eligibility, tax, payment).
- **Growth:** organic only — no botting, sub4sub, engagement pods, or bought views/hours.
- **Division of labor:** Claude Code builds and maintains the deterministic pipeline; deterministic code runs the unattended loop; Claude Code/Cowork does scheduled *review/regeneration*, never scheduled blind publishing. The human gate is non-negotiable.

## The one rule that governs everything

YouTube's **July 15, 2025 "inauthentic content" policy** (renamed from "repetitious content") demonetizes mass-produced/templated content with little variation between videos, and it applies **channel-wide**. This is the single biggest existential risk to an AI faceless fleet. Every video must be **materially varied** (distinct visuals, distinct audio/track, distinct title/metadata), and the human review gate must enforce a material-variation check before publish. AI is explicitly *allowed and monetizable* — the line is templated sameness, not AI itself. The pipeline's originality (own Higgsfield footage + own Suno music) is the core mitigation. Whenever advising on production, scheduling, SEO, or branding, keep guidance on the right side of this rule.

## Current state

The pipeline is proven end to end (a 3-hour loop assembles from a short clip in ~60s via ffmpeg stream-copy; Higgsfield produces publishable on-brand motion at ~8 credits/video). The predecessor channel "2am without her." (@2amWithoutHer) validated the whole workflow (concept → live in ~48h; organic search in 48h; 11.1% CTR on its best video) — it used a recurring character, which the new fleet drops. Build lives in a `faceless_fleet/` repo (config-driven, review-gated). See `references/pipeline.md` for the validated pipeline and where every tool/credential/output lives.

## Validated production lessons (2026-07, from real renders — follow these)

- **soul_2 has NO negative-prompt channel.** Inline "no X" lists INJECT X (we grew foreground tree trunks from "no tree trunks"). Positive-only composition wording; `identity.negative` is the review checklist, not prompt text.
- **"like a fire dancing inside" renders literal flames** (a burning cabin). Say "windows glowing with soft warm amber light from deep inside". Campfire/fireplace scenes where fire IS the subject are the exception.
- **Kling under-animates timid prompts.** "gentle/subtle/only-motion-is-X" → near-static clip (0.0% pixel change, twice). Motion prompts must be explicit and multi-element ("heavy rain in clearly visible streaks… reflections rippling… smoke drifting"). Serene water scenes especially need heavy-rain energy or they freeze.
- **Loudness:** normalize each SFX element to −20 LUFS/TP−3 BEFORE mixing (raw Freesound files vary ~30 dB in crest); then measured two-pass loudnorm with verify-and-correct; leave ~1.5-4 dB codec headroom (AAC overshoots true peak on crackle/cricket transients — crickets by ~+4 dB).
- **Brand framing (CK):** the stylized painterly look is owned as "handcrafted" in bios/descriptions ("scenes painted in our signature storybook style, soundscapes mixed by hand"). Anchor craft claims to curation/mixing; never explicitly deny AI.
- **Coordination:** parallel instances split lanes (content vs channel setup); pull-rebase before every push to `main`.

## How to use this skill — routing table

Read the reference file that matches the task. Don't load them all; load what's relevant.

| If the work is about… | Read |
|---|---|
| The tool stack, where things/credentials live, the build + automation architecture, ffmpeg looping, Claude Code orchestration, the validated 2am pipeline | `references/pipeline.md` |
| Which niches/categories to run, the 3-channel slate rationale, job-to-be-done per niche, the geography/Canadian-content verdict, differentiation levers | `references/strategy.md` |
| Audio sourcing + licensing, Suno commercial terms, Content ID safety, seamless mastering/LUFS, Spotify/Apple + SOCAN royalty stacking, the audio tool budget | `references/audio.md` |
| Keyword research, ranking title formulas, metadata for speechless content, playlists/end-screens/chapters, search-vs-suggested sequencing | `references/seo.md` |
| Cold-start to first 1,000 subs / 4,000 hours, 24/7 live-stream loops (how-to + policy), the Shorts funnel, the 0-to-monetization plan | `references/growth.md` |
| YPP path + RPM levers, YouTube Premium revenue, secondary streams ranked, Canadian tax (W-8BEN, T2125, GST/HST, incorporation) | `references/monetization.md` |
| Building channel recognition without a character, per-niche thumbnail formulas, avatar/banner specs, consistency-vs-variation, the clip-channel verdict | `references/branding.md` |

## Verify before quoting (fast-moving facts)

These were flagged as uncertain or fast-changing. Do NOT state them as settled — verify against current sources first, and tell CK you're verifying:

- **YouTube upload quota — RESOLVED (June 2026, in config):** `videos.insert` = 100 general units + 1 from a dedicated hidden "Video Uploads" bucket that caps UNVERIFIED projects at ~7-11/day (silent 429). We stay at 5/day/project; project verification lifts it to 100/day. **Never shard Cloud projects — ToS violation.**
- **Suno commercial/ownership terms** — changed after the Warner deal (Nov 2025): "you generally are not considered the owner," plus model deprecation and download caps. Verify current monetization/distribution rights.
- **Ambient/sleep RPM** — ranges wildly ($0.40–$4 generic music vs ~$10.92 US sleep "soundscapes"). Give ranges; it's a watch-time volume play.
- **Higgsfield pricing/credits**, **Spotify's 1,000-stream + functional-noise rules**, **SOCAN AI-eligibility (Oct 2025)**, the **12-hour live-archive limit**, **Facebook Content Monetization eligibility in Canada**, and **Canadian tax specifics (W-8BEN treaty rate, GST/HST $30k)** — all verify current; tax details need a Canadian accountant (not professional advice).

## Tone with CK

Direct, realistic, downside-surfaced. No hype. Ranges over false precision. Separate verified facts from estimates. Surface the risk, then give the opinionated recommendation.
