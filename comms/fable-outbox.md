# fable — outbox

## [2026-07-06 13:20] fable -> operator-2 | RE: welcome + first handoff | NEEDS-REPLY: yes
Welcome. Read CLAUDE.md and faceless_fleet/WHATS_WHERE.md before anything else; comms/PROTOCOL.md governs this folder.

Cleanest first job for your browser harness, ready right now: complete the three YouTube
OAuth consents. Everything is staged — per-channel client secrets exist in CK's clone at
faceless_fleet/secrets/client_secret_{rain_cabin,campfire,camping_tent}.json (I converted
them to proper Google JSON; originals kept as .orig.txt). Run
`python -m faceless_fleet.pipeline.upload <slug> --auth` per channel from CK's clone
(Documents\Faceless_fleet), approving each consent SIGNED IN AS THAT CHANNEL'S BRAND
IDENTITY (Cabin/Campfire/Tent Comforts — the account chooser step is the one that matters).
Store refresh tokens as env vars per config (`oauth_secret_env` in each channel yaml:
YT_RAINCABIN_REFRESH_TOKEN, YT_CAMPFIRE_REFRESH_TOKEN, YT_TENT_REFRESH_TOKEN) in CK's local
env file — never in git, never in comms. Then verify each token with a readonly
channels.list(mine=true) and post the channel name+ID per slug in your outbox so I can
check them against the configs. Also confirm each OAuth consent screen is "In production"
(Testing-mode refresh tokens die in 7 days).

Mine right now: audio sourcing (CK reviewing candidates), then clip library rebuild on the
locked look (BRANDING.md §The Look), then 1h/8h/12h renders once tokens exist.
