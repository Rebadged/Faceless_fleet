# STATUS — one-screen coordination summary (both agents keep current)
Updated: 2026-07-12 by fable

## Objective (CK): all 3 channels reach verified scheduled uploads
| Workstream | Owner | State | Next |
|---|---|---|---|
| OAuth refresh tokens | Relay | 0 minted; Campfire sign-in open (2 of 3 possible) | CK signs in; mint Campfire+Tent; Cabin waits |
| Channel ID verification | Relay -> fable | 2 public IDs verified; Cabin terminated/stale | token-bound readonly identity check; CK resolves Cabin |
| Consent screens "In production" | Relay | unknown | confirm x3 |
| Phone verification (Campfire, Tent) | Relay | unknown | check in Studio |
| Audio element picks (a/b x7) | CK/fable | done: calm-first canon | 7 MP3s present; fix Tent key + strict missing-layer preflight |
| Clip library on locked look | fable | seed only: 2/channel | need >=3 approved/channel for 3/week; credits = CK gate |
| Long renders 1h/8h/12h | fable | Campfire 1h smoke rendered; launch QA failed | fix geometry + audio ceiling + thumbnail, rerender |
| First scheduled upload (Cabin) | both | blocked: old channel terminated | CK identifies replacement/appeal path, then token + render + approval |
| Upload-path audit | Relay -> fable | spacing/cap/UTF-8 pass; retry/human/thumbnail gates pending | fix phantom ledger, clip-aware selection, strict SFX, CK gate + thumbnail build/upload |

## Done (recent)
- Campfire 1h local smoke render completed; candidate rejected for geometry switch, -1.04 dBTP ceiling miss, and missing thumbnail (2026-07-12)
- Runtime media integrity: 6 seed clips + 7 canonical SFX readable; ffmpeg/ffprobe 8.1.1 available (2026-07-12)
- The Look locked + 6 approved scenes in configs (2026-07-03)
- Per-channel OAuth secrets support + youtube.readonly scope + CK.env auto-load (2026-07-12)
- comms protocol + onboarding live (2026-07-06/12)
