# STATUS — one-screen coordination summary (both agents keep current)
Updated: 2026-07-12 by fable

## Objective (CK): all 3 channels reach verified scheduled uploads
| Workstream | Owner | State | Next |
|---|---|---|---|
| OAuth refresh tokens | Relay | pending (2 of 3 possible) | mint Campfire+Tent; Cabin blocked on channel decision |
| Channel ID verification | Relay -> fable | 2 verified; Cabin terminated/stale | write Campfire/Tent IDs; CK resolves Cabin |
| Consent screens "In production" | Relay | unknown | confirm x3 |
| Phone verification (Campfire, Tent) | Relay | unknown | check in Studio |
| Audio element picks (a/b x7) | CK/fable | done: calm-first canon | 7 MP3s present; fix Tent key + strict missing-layer preflight |
| Clip library on locked look | fable | seed only: 2/channel | need >=3 approved/channel for 3/week; credits = CK gate |
| Long renders 1h/8h/12h | fable | blocked | after library + audio |
| First scheduled upload (Cabin) | both | blocked: old channel terminated | CK identifies replacement/appeal path, then token + render + approval |
| Upload-path audit | Relay -> fable | spacing/cap/UTF-8 pass; retry/human gate pending | fix phantom ledger, clip-aware selection, strict SFX + CK gate |

## Done (recent)
- Runtime media integrity: 6 seed clips + 7 canonical SFX readable; ffmpeg/ffprobe 8.1.1 available (2026-07-12)
- The Look locked + 6 approved scenes in configs (2026-07-03)
- Per-channel OAuth secrets support + youtube.readonly scope + CK.env auto-load (2026-07-12)
- comms protocol + onboarding live (2026-07-06/12)
