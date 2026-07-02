# Handoff — Instance 2: launch Campfire Comforts + Tent Comforts

You are a parallel Cowork instance. Instance 1 (Fable) is producing Cabin Comforts
content; **your lane is channels 2 & 3: create + brand "Campfire Comforts"
(`config/channels/campfire.yaml`) and "Tent Comforts" (`config/channels/camping_tent.yaml`)**.
Split rule: you own the two channel setups + their configs; do NOT edit `pipeline/*`,
`config/channels/rain_cabin.yaml`, or `global.yaml` (instance 1's lane). Commit small,
`git pull --rebase` before every push — both instances push to `main`.

## Repo access (the exact working recipe)
- Repo: **`Rebadged/Faceless_fleet`** (private), branch `main`. The `faceless_fleet/`
  package is at repo root.
- GitHub fine-grained PAT (Contents read/write, this repo only) is on CK's machine at
  **`C:\Users\caden\Claude\Projects\Youtube\gh_token.txt.txt`** (mounted in Cowork as
  `mnt/Youtube/gh_token.txt.txt`). Wire it like:
  `git config --global credential.helper store` then write
  `https://Rebadged:<TOKEN>@github.com` to `~/.git-credentials`. Never print the token.
- **Gotcha:** `git clone` into the mounted `Projects\Youtube` folder FAILS ("Operation
  not permitted" on .git lock files). Clone into the sandbox home (`~`) instead; git is
  the persistence layer (sandbox is wiped between sessions — push everything that matters).

## Read these, in order (all in the repo)
1. `WHATS_WHERE.md` — repo map + the 2026-07-01 session changelog (current state).
2. `COWORK_HANDOFF.md` — the master playbook. **§5.B–C is your job description**
   (branding + channel creation steps). §7 gotchas, §8 security rules (non-negotiable:
   no secrets in chat or git).
3. `BRANDING.md` — avatar/banner/thumbnail specs, per-channel prompts, the
   "handcrafted" framing policy (already written into your channels' bios/descriptions
   — use the bio in each config verbatim).
4. `research/CROSS_REFERENCE_2026.md` — resolved decisions + compliance keystones.
   Locked, do not relitigate: 5s clips, locked camera + particle overlays, no Suno,
   −16 LUFS, Fall-first launch.
5. `FABLE_HANDOFF.md` — the locked visual spec for any imagery you generate.

## Accounts & assets
- **YouTube:** Cabin Comforts exists and is the reference: `UCbayo4s0nrP0-n2iagNDBQw`
  (@CabinComforts) — branded, phone-verified, public. Create yours the same way:
  YouTube → Settings → Add/manage channels → **Brand Account**; name + handle from the
  config (`channel.name`, `youtube_handle` — if the handle is taken, pick a variant and
  **write it back into the config + commit**); phone-verify (CK enters the SMS code);
  upload avatar + banner; paste `channel.bio` as description; country = Canada; add
  "Featured channels" cross-links to @CabinComforts and the sister channel.
- **Higgsfield MCP** (shared account, Plus): branding for both channels was generated
  in a past session — Tent banner `150bbf37-932c-442d-98a2-edbdf23e291d`, Tent avatar
  `23c21ead-efec-46d3-9247-1135d870b2bf`, Campfire banner
  `42673481-8378-481b-b532-d092f56be7dc`, Campfire avatar `db810393…` (find via
  `show_generations`/`job_display`, download the rawUrl).
  **⚠ Inspect before publishing:** the Cabin set from that batch had a baked-in
  Higgsfield watermark badge on the avatar and garbled UI chrome on the banners
  (triggered by the literal words "YouTube banner" in the prompt). Zoom the corners.
  Regenerate defective ones with the `BRANDING.md` prompts — but reworded per the
  validated 2026-07-01 prompt lessons below.
- **Credits:** shared pool (~840 as of this handoff; instance 1 has CK's 150-credit
  budget for Cabin videos). Your branding is stills-only ≈ ~0.1 cr each — iterate
  freely, but do NOT generate videos without CK's explicit OK.

## Validated prompt lessons (2026-07-01, from real renders — follow these)
- `soul_2` has **no negative-prompt channel**. Inline "no X" lists INJECT X into the
  image (we grew foreground tree trunks from "no tree trunks"). Use **positive-only**
  wording ("the ground between the camera and the tent completely open and empty").
  `generate.py` no longer appends `identity.negative` — it's the review checklist.
- Phrases like "firelight **like a fire dancing inside**" render LITERAL flames
  (a burning cabin). Say "windows glowing with soft warm amber light from deep inside".
  (Campfire scenes are the exception where visible flames are the subject.)
- Aspect: banner 2048×1152, avatar 2048×2048, **no text baked into any image** (AI
  text = gibberish; thumbnails are a later Pillow/compositing step per BRANDING.md).
- If you animate anything (don't, without CK): motion prompts must be EXPLICIT and
  multi-element or Kling renders a near-static clip.

## Strategy context you must respect
- **Launch staging (ROADMAP / COWORK_HANDOFF §5.C):** create + brand both channels NOW
  so they age, but they do NOT upload at full cadence — Cabin launches first; Campfire/
  Tent get a light trickle only after Cabin is 2–4 weeks clean (Gate A).
- **Fall-first (CK, 2026-07-01):** the fleet launches on autumn/rain scenes — rich audio
  palettes (rain, distant thunder, fire crackle; **wind-heavy mixes were rejected**).
  Tent's signature = rain drumming ON the tent tarp; Campfire = crackle + light drizzle.
- **"Handcrafted" brand framing (CK):** already in your configs' bios + description
  templates — anchor craft claims to curation/mixing, never explicitly deny AI.

## Secrets (§8 — hard rules)
Keys/tokens/passwords NEVER in chat or git. CK's creds live in `CK.env` on his machine;
the GitHub token in the file above; YouTube refresh tokens (later) go in per-channel env
vars (`YT_CAMPFIRE_REFRESH_TOKEN`, `YT_TENT_REFRESH_TOKEN`). If a secret lands in chat,
tell CK to regenerate it.

## When done
Update `WHATS_WHERE.md`'s changelog (channels created, handles, channel IDs, branding
state), write channel IDs into the configs (`youtube_channel_id`), commit + push.
