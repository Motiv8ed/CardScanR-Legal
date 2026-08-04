# Deployment — CardScanR-Legal (GitHub Pages)

Zero-cost static site for CardScanR legal, support, OAuth return, and Android
App Links verification. No paid hosting.

## Live public URLs (GitHub Pages — working now)

Relative links are used throughout `docs/`, so the site works on the project
Pages URL:

- https://motiv8ed.github.io/CardScanR-Legal/
- https://motiv8ed.github.io/CardScanR-Legal/privacy/
- https://motiv8ed.github.io/CardScanR-Legal/terms/
- https://motiv8ed.github.io/CardScanR-Legal/support/
- https://motiv8ed.github.io/CardScanR-Legal/delete-account/
- https://motiv8ed.github.io/CardScanR-Legal/data-deletion/
- https://motiv8ed.github.io/CardScanR-Legal/auth/callback/
- https://motiv8ed.github.io/CardScanR-Legal/.well-known/assetlinks.json

Repository: `Motiv8ed/CardScanR-Legal`  
Default branch: `master`  
Pages source: `master` / `/docs`  
`docs/.nojekyll` is present so GitHub Pages serves `.well-known/` as static files.

## Desired custom domain (OWNER ACTION — do not enable until DNS works)

Desired apex: **cardscanr.com**  
Desired www: **www.cardscanr.com**

### Do not create `docs/CNAME` yet

Creating `docs/CNAME` before DNS is correctly pointed will break
`motiv8ed.github.io/CardScanR-Legal` URLs.

A pending file is ready:

- `docs/CNAME.pending` contains `cardscanr.com`

**When DNS is confirmed working**, rename:

```text
docs/CNAME.pending  →  docs/CNAME
```

Then commit/push and set the custom domain in GitHub → Settings → Pages.

### DNS options (OWNER ACTION)

#### Option A — Apex A records + www CNAME (GitHub Pages)

At your DNS host for `cardscanr.com`, create:

| Type  | Name | Value                 |
| ----- | ---- | --------------------- |
| A     | `@`  | `185.199.108.153`     |
| A     | `@`  | `185.199.109.153`     |
| A     | `@`  | `185.199.110.153`     |
| A     | `@`  | `185.199.111.153`     |
| CNAME | `www`| `motiv8ed.github.io`  |

Then in GitHub Pages settings, set custom domain to `cardscanr.com` and enable
HTTPS once GitHub issues the certificate.

#### Option B — Cloudflare proxy to GitHub Pages

1. Add `cardscanr.com` to Cloudflare (or use an existing zone).
2. Point DNS at GitHub Pages (same A records / www CNAME as above, or a
   Cloudflare CNAME setup that targets `motiv8ed.github.io`).
3. SSL/TLS mode: **Full** (not Flexible) once GitHub HTTPS is ready.
4. Only enable proxy (orange cloud) after you understand cache/HTTPS behaviour
   for `.well-known` and OAuth return paths.
5. Still rename `docs/CNAME.pending` → `docs/CNAME` only after DNS resolves
   correctly to GitHub Pages.

### Final URLs after custom domain is live

- https://cardscanr.com/
- https://cardscanr.com/privacy/
- https://cardscanr.com/terms/
- https://cardscanr.com/support/
- https://cardscanr.com/delete-account/
- https://cardscanr.com/data-deletion/
- https://cardscanr.com/auth/callback/
- https://cardscanr.com/.well-known/assetlinks.json
- https://www.cardscanr.com/… (same paths, once www is configured)

Play Console and OAuth redirect URIs should be updated to the custom-domain
URLs when DNS is ready. Keep github.io URLs working until then.

## Play Console URLs (current github.io)

Privacy Policy:

`https://motiv8ed.github.io/CardScanR-Legal/privacy/`

Account deletion:

`https://motiv8ed.github.io/CardScanR-Legal/delete-account/`

Optional alias:

`https://motiv8ed.github.io/CardScanR-Legal/data-deletion/`

OAuth / App Links (after domain cutover, prefer cardscanr.com equivalents):

`https://motiv8ed.github.io/CardScanR-Legal/auth/callback/`  
`https://motiv8ed.github.io/CardScanR-Legal/.well-known/assetlinks.json`

## Android Digital Asset Links (`assetlinks.json`)

File: `docs/.well-known/assetlinks.json`

| Field | Value |
| --- | --- |
| `package_name` | `com.cardscanr.app` |
| Fingerprint currently published | **Upload / test** certificate SHA-256 from the CardScanR upload keystore |
| Upload / test SHA-256 | `B8:08:4B:10:C0:B8:7F:AD:34:F2:E9:EC:44:6E:4A:63:D0:44:A4:B1:E6:B8:20:67:5D:33:13:52:C1:EE:40:B6` |

### PLACEHOLDER — Play App Signing certificate (OWNER ACTION)

For Play-distributed installs, Android App Links verification usually requires
the **Google Play App Signing** certificate SHA-256 from Play Console → App
integrity → App signing — **not** only the upload key.

Do **not** invent that value. After first Play App Signing enrollment:

1. Copy the Play App Signing cert SHA-256 from Play Console.
2. Add it to `sha256_cert_fingerprints` in `docs/.well-known/assetlinks.json`
   (keep the upload fingerprint for sideload/test if still useful).
3. Re-validate and redeploy.

Until that fingerprint is added, treat App Links on Play builds as incomplete.

## Maintain / redeploy

1. Edit files under `docs/` (or supporting markdown) in this repository only.
2. Run:

```bash
python scripts/validate_legal_site.py
```

3. Ensure exit code **0**.
4. Commit on `master` and push to `origin` (only when intentionally publishing).
5. Wait for GitHub Pages to refresh, then re-check the live URLs over HTTPS.

### Pages settings

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **master**
4. Folder: **/docs**
5. Custom domain: leave empty until DNS is ready and `docs/CNAME` exists

## Safety reminders

- Never commit Supabase service role keys, OAuth client secrets, or reviewer passwords.
- Do not point Pages at anything outside `docs/`.
- Do not create `docs/CNAME` until the owner confirms DNS for `cardscanr.com`.
- Do not enable paid hosting or paid DNS products for this site.
- Re-run validation after every public HTML or Asset Links edit.
