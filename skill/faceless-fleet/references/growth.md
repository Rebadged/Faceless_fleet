# Growth & Cold-Start (Live Loops + Shorts Funnel)

**Lead with a 24/7 live-stream loop as the watch-hour engine and a daily Shorts funnel as the subscriber engine — but focus everything on ONE channel (Rainy Cabin) for the first 90 days.** The classic YPP path (1,000 subs + 4,000 public watch hours/12 months) is the realistic one; the Shorts path (10M Shorts views/90 days ≈ 111k/day) is a viral threshold, not a plan.

## Cold-start reality

- Every upload seeds to ~10–100 viewers within minutes; scored on engagement (CTR + watch time), satisfaction (surveys/returns), relevance. Reach expands over 24–48h and 7–14 days.
- **Ambient flips the math:** search/intent-driven (low CTR is normal), but average view duration runs in *hours*, so one 10-hour video banks huge watch-hours from few viewers. The lever is search-intent match + maximum retention (seamless loops, ~-16 to -18 LUFS), not clicks.
- **The binding constraint is usually subscribers (1,000), not watch hours** — which is exactly why the Shorts funnel matters. Realistic timeline to YPP: **4–9 months** for a disciplined single channel, not weeks.

## 24/7 live-stream loops

- **Why:** always-on discoverability (Live tab/badge, search, all time zones); **public live watch hours count toward the 4,000-hour threshold**; new-audience injection.
- **How (ffmpeg + VPS):** render a long seamless loop (hours, not a short clip) at ~-16 to -18 LUFS; push to YouTube RTMP:
  `ffmpeg -re -stream_loop -1 -i loop.mp4 -c:v libx264 -preset veryfast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/STREAM_KEY`
  (`-g` = 2×fps; 1080p ~3,000–6,000 kbps / 720p ~2,500 kbps). **Run from the VPS** (a home PC 24/7 is unreliable + costs more in electricity).
- **Archive so the hours count:** restart the ffmpeg process + broadcast every **~11.5 hours** so each segment stays under the 12-hour auto-archive ceiling and converts to a public VOD (VERIFY the 12h limit + that public live hours still count). Start streams via the **scheduler**, not "Go Live" (an operator found >90% of failed streams were started via "Go Live"). Add monitoring/auto-restart.
- **Cost/bandwidth:** ~2 Mbps ≈ ~650 GB/mo; ~6 Mbps ≈ ~2 TB/mo — pick unmetered/high-cap bandwidth. A 1–2 vCPU VPS runs one stream ~$5–12/mo.
- **Requirements/risk:** verified channel (phone) + 24h activation + no live restrictions/90 days. **No subscriber minimum for encoder/RTMP streaming** (the 50-sub rule is mobile-app only — so a 0-sub channel CAN go 24/7 live via ffmpeg). Looping pre-recorded as "live" is allowed (standard for lofi radio) — BUT looping a single un-varied short clip trips inauthentic-content/quality flags; use a long varied loop of your own assets.
- **Honest read:** a watch-hour + always-on-presence engine, NOT a discovery rocket. New streams sit at 0–3 concurrent for weeks; early value is banked hours + always-live presence while Shorts + catalog do the subscriber/discovery lifting.

## Shorts funnel

- **How Shorts work:** separate ranking model; seeds to ~50–500 (~70% non-subscribers); the gate to wider reach is average % viewed/retention + replays + shares; swipe-away in the first 1–2s is the killer; can resurface weeks later. 2026 weights Short→long-form click-through heavily.
- **Hard conversion reality:** Shorts-feed watch time does **NOT** count toward 4,000 hours; Shorts→subscriber ~0.5% (≈5 subs/1,000 views; >1% is strong); Short→long-form viewer even lower. **Shorts' job is to drive the 1,000 subscribers (the bottleneck) + feed discovery — NOT watch hours or direct revenue.**
- **Funnel mechanics (use the 50+ hook library — curiosity-gap/POV/bold-statement/FOMO/comment-bait):** hook in the first 1–1.5s; burn-in captions (muted viewing); design the end to loop seamlessly for replay credit; original audio; drive conversion via a pinned comment linking the full long-form/live stream + an end-of-Short CTA + a Shorts-specific channel trailer (2–4x better conversion for Shorts visitors).
- **Ambient Shorts ideas (cheap repurposing):** crop Higgsfield loops to 9:16, cut 20–45s clips (rain-on-window, fireplace, storm); "POV: it's raining and you're in a cozy cabin"; satisfying/sensory micro-loops; dog: "play this when your dog is anxious" + before/after; sleep: 30s "fall asleep in 2 minutes" tips. Each materially varied.
- **Cadence:** ~1–2 Shorts/day at a consistent time (below ~1/day the algorithm deprioritizes; above ~3/day reach dilutes). Solo-sustainable = 1/day per active channel, batch-produced. Consistency beats bursts.

## Other cold-start levers

Fixed publishing schedule ("program" the channel — consistency is a signal). First 10–20 videos = test bed; by ~50–100 identify the ~20% of formats driving ~80% of results, double down, **unlist (never delete)** duds. External traffic (high ROI, low risk if genuine): Pinterest ("cozy rain ambience"/"cozy cabin" visual search), Reddit (r/CozyPlaces + sleep/study/ASMR — contribute genuinely, no blatant promo), sleep/study playlists + embeds (count as valid external watch time). Cross-promotion between your own channels + cross-posted Shorts is free leverage. Facebook Reels (Canada-eligible — Content Monetization + Creator Fast Track: 15 reels/month across ≥10 days; ~US$100–$450/mo for 20k–99,999 followers up to ~$3,000/mo for 1M+). TikTok/IG reach-only.

**Avoid:** engagement pods, sub4sub, bought views/hours, botting (detected, stripped, suspension risk); looping a single short clip; templated uploads; TikTok-watermarked cross-posts (demoted).

## 0-to-monetization plan

- **Days 0–14:** verify + enable live (24h wait); VPS + ffmpeg stream script with ~11.5h auto-cycle; publish 8–12 long varied loops (review-gated); stand up the 24/7 stream; build the Shorts trailer.
- **Days 15–45:** 2–3 long-form/week (fixed schedule); 1 Short/day (hook library, pinned-comment + end-CTA funnel); verify VOD archiving; Pinterest + tasteful Reddit/playlist seeding; cross-post to Facebook Reels (monetizable), TikTok/IG reach-only.
- **Days 46–90:** double down on best formats/hooks; you'll likely hit 4,000 hours (stream + catalog) before 1,000 subs — weight effort to Shorts/subscriber conversion; decide Channel 2 once Channel 1 self-runs.
- **Add Channel 2** when Channel 1 is automated AND ≥600 subs or ≥3,000 watch hours. Effort split ~70% Channel 1 / ~20% reusable systems / ~10% Channel 2 seeding.

**Benchmarks:** <300 subs after 90 days despite consistent Shorts → re-examine hooks/trailer before adding channels. Watch hours stall → verify VOD archiving + add stream hours/longer videos. Short breakout (>100k) → immediately publish 3–5 varied versions of that hook.

## Caveats

- New-stream concurrent viewers are low (0–3) for weeks; early payoff is banked hours + presence, not a spike. The 12-hour archive limit is a real risk to watch-hour counting — verify VOD archiving + hours in Studio. Shorts conversion (~0.5%) is an industry aggregate — recalibrate from analytics. Facebook/Meta eligibility changes often and is per-page — verify in the Meta Professional Dashboard. The inauthentic-content rule has terminated/demonetized AI faceless channels — originality/variation is the highest existential risk.
