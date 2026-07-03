# Audio — Sourcing, Licensing, Mastering, Royalty Stacking

> **DECISIONS IN FORCE (2026-07):** fleet audio = **pure CC0 ambience** (Freesound), NO Suno.
> Target **−16 LUFS / TP −1.5 / LRA ≤6** via the pipeline's measured chain: per-element
> loudnorm to −20/−3 before mixing → adaptive transient conditioning → measured two-pass
> loudnorm (verify-and-correct) → oversampled limit with 1.5–4 dB codec headroom (AAC
> overshoots on crackle/cricket transients). Fall palette first: rain_heavy, rain_light,
> thunder_distant, fireplace, crickets — NO wind-forward mixes (CK rejected). Suno/SOCAN/
> Spotify notes below are for the parked music-channel idea, not the active fleet.


Audio is the star of these channels. The core principle: **make it genuinely original, not scraped.** Original/self-generated audio is both higher-quality and the best shield against Content ID claims. "Fetch CC0 rain from Freesound and layer it" is the placeholder to move past.

## Sourcing per channel

**Nature/ambience (Rainy Cabin):**
- **Recommended core method:** design original soundscapes in a DAW from 4–8 licensed/AI stems (rain bed + thunder + fire + wind + room tone). Audacity (free) or Reaper (~$60 one-time).
- **Paid subscription libraries (the workhorse layer):** Epidemic Sound (~$15 personal/$19 commercial; pre-cleared, Content-ID-safe, channel whitelisting; videos cleared during an active sub stay cleared forever). Artlist (~$40 Max; lifetime rights on downloads, Clearlist auto-clears claims). Storyblocks (~$15; unique $20k indemnification on individual tier, but assets are NOT perpetual after cancellation — keep the sub active). Boom Library (one-time packs, hundreds of dollars — the quality ceiling; buy ONE to anchor the channel).
- **AI-generated SFX (highest-ROI originality lever):** ElevenLabs Sound Effects (paid from $5/mo; all paid tiers grant commercial/royalty-free use; ~22–30s clips — loop/layer them). Stable Audio Open (local, unlimited, ~47s cap).
- **Free (Freesound) — fallback only, never the core:** only **CC0** is monetization-safe; CC-BY needs attribution; CC-BY-NC forbids monetized use (avoid). CC0 risks mislabeled rips + sameness + third-party Content ID on similar recordings.

**Ambient music (sleep channel) — Suno:** Pro ($10/mo) grants a commercial-use license; you keep rights to songs made while subscribed even after cancelling. **VERIFY current terms** — post-Warner deal (Nov 2025) Suno changed to "even with granted commercial use rights, you generally are not considered the owner" (raw AI output isn't copyrightable in US/Canada → can't defend against copying, can't register in Content ID); current models to be deprecated when licensed models launch; free-tier downloads removed; paid tiers get monthly download caps. Suno music is **monetizable on YouTube** (must clear the inauthentic-content bar; NOT Content-ID-eligible) **and distributable to Spotify/Apple** via DistroKid (AI allowed if you own rights + disclose via the DDEX synthetic flag; **CD Baby and TuneCore reject 100%-AI music**).

**Pet (dog):** Suno soft piano/ambient (proven by RelaxMyDog/Calm Your Dog), optional gentle nature beds; same mastering/looping.

## Seamless mastering

- Cut loop boundaries at **zero-crossings**; choose similar-amplitude start/end points; crossfade to mask residual mismatch (loop a 30s+ section for ambient).
- **Defeat the obvious loop:** layer stems of mutually-prime lengths (e.g., 47s + 2m11s + 3m37s) so the combined texture doesn't repeat until their LCM; add sparse random one-shots.
- **LUFS — the -14 target is likely too loud for sleep.** Aim **~-16 to -20 LUFS integrated** (ambient commonly ~-18), true peak ≤ -1 dBTP. Quieter preserves dynamics, avoids fatigue, and prevents "loud ambience" for a cranked-volume sleeper. Verify with a free meter (Youlean) in the review gate.
- Keep WAV through the pipeline; compress only at final upload. See ffmpeg/pydub commands in `references/pipeline.md`.

## Content ID & copyright safety

- Content ID fingerprints audio and auto-claims matches; it does NOT read your license. **Nature sounds, white noise, ambient beds, sleep/meditation music, production loops, and fully AI-generated audio are all INELIGIBLE to be registered as Content ID references** (too common/non-distinct).
- **Do NOT enroll any fleet audio in Content ID** (e.g., DistroKid's add-on) — it'd be rejected for ambient/AI anyway, and registering risks false claims against innocent creators + penalties.
- Genuinely original/self-generated audio is the best shield; the only realistic claims are third-party false positives — dispute in Studio with documentation. A claim ≠ a strike; you keep held revenue once resolved. Whitelist your channels with your paid library.
- Keep a license/receipt file per video (library PDFs, Suno receipts + dates, ElevenLabs plan) as proof of original creation.

## Spotify/Apple + SOCAN royalty stacking (real but modest secondary line)

- Repurpose the long-form audio into tracks/albums; distribute via DistroKid (~$23–25/yr, AI-friendly, 0% commission) for streaming royalties ON TOP of AdSense.
- **Sober earnings:** ~$0.003–0.005/stream Spotify, ~$0.005–0.01 Apple. A brand-new small catalog likely earns **tens to low-hundreds of dollars in the first 6–18 months** — not a jackpot. Gated by:
  - **Spotify 1,000-stream/12-month minimum** (per track) + a non-public minimum-listener count — below it, ZERO master royalties. (VERIFY current figures.)
  - **Functional-noise rules:** rain/white-noise/nature need a **2-minute minimum** AND are reportedly valued at ~one-fifth of a music stream. Composed sleep *music* counts as full-value music.
  - **Anti-spam/anti-mass-AI filtering** — release deliberately, distinct tracks, clean metadata.
- **Canadian SOCAN advantage:** SOCAN collects composition/publishing royalties **separate from master royalties and NOT subject to the 1,000-stream threshold** — register with SOCAN (free for Canadians). Per the ASCAP/BMI/SOCAN alignment (Oct 28, 2025), works "partially generated using AI" (AI + human authorship) are eligible while "entirely AI" works are not — so **document human input** (arrangement/editing/curation). (VERIFY the human-authorship line.)
- **Naming trap:** do NOT keyword-stuff artist/track names ("Sleep Music," "Rain Listener") — distributors/platforms reject SEO-stuffed generic names. Use a real, distinct artist name + clean metadata. Tracks ≥2 min (ideally 3–10), bundled into themed albums.
- **No Content ID conflict:** ambient/nature/AI is Content-ID-ineligible and you won't register it, so the same masters go on YouTube + Spotify without fingerprint conflict.

## Budget-fit stack (~$50–75 CAD/mo + one-time DAW)

Epidemic Sound commercial (~$26 CAD) + Suno Pro (~$14 CAD) + ElevenLabs Starter/Creator (~$7–30 CAD) + DistroKid (~$2.50 CAD/mo) + SOCAN (free) + Audacity (free) or Reaper (~$60 one-time) + Youlean meter (free). Optional one-time Boom Library nature pack.

**Highest-ROI:** replace scraped CC0 with paid + AI-generated + DAW-layered original audio; prime-length multi-stem layering; master sleep quieter (~-18); register SOCAN; keep the review gate + per-video variation. **Avoid:** raw CC0 as core; enrolling ambient/AI in Content ID; CD Baby/TuneCore for 100%-AI; keyword-stuffed streaming names; mastering sleep at full -14; treating Spotify as primary income early.

## Caveats

- Suno's ownership/legal status is unsettled (license but not copyright; label litigation active mid-2026; terms changing under Warner). Keep dated receipts and verify before external licensing.
- AI-music platform policies move fast and can apply retroactively — disclose honestly everywhere.
- The "one-fifth" functional-noise valuation and the exact Spotify listener minimum are reported, not officially fixed — verify.
- LUFS targets are guidance (platforms normalize) — adjust by ear.
