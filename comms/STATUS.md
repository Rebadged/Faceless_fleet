# STATUS — one-screen coordination summary (both agents keep current)
Updated: 2026-07-12 by fable

## Objective (CK): all 3 channels reach verified scheduled uploads
| Workstream | Owner | State | Next |
|---|---|---|---|
| OAuth refresh tokens (3) | Relay | pending | mint via --auth, store in secrets/CK.env |
| Channel ID verification | Relay -> fable | pending | Relay posts name+ID per slug; fable writes configs |
| Consent screens "In production" | Relay | unknown | confirm x3 |
| Phone verification (Campfire, Tent) | Relay | unknown | check in Studio |
| Audio element picks (a/b x7) | CK | reviewing | previews in Projects\Youtube\review\audio |
| Clip library on locked look | fable | not started | after audio picks; credits = CK gate |
| Long renders 1h/8h/12h | fable | blocked | after library + audio |
| First scheduled upload (Cabin) | both | blocked | tokens + render + CK approval |
| Upload-path audit | Relay | offered | findings -> fable |

## Done (recent)
- The Look locked + 6 approved scenes in configs (2026-07-03)
- Per-channel OAuth secrets support + youtube.readonly scope + CK.env auto-load (2026-07-12)
- comms protocol + onboarding live (2026-07-06/12)
