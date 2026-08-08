# Deployment — CardScanR-Legal

Zero-cost static site for CardScanR legal, support, feedback, OAuth return, and
Android App Links verification.

## Live custom domain (Cloudflare Pages — primary)

**Project:** `cardscanr-www` (Cloudflare Pages, free tier)

Production URLs (canonical):

- https://cardscanr.com/
- https://cardscanr.com/support/
- https://cardscanr.com/feedback/
- https://cardscanr.com/privacy/
- https://cardscanr.com/terms/
- https://cardscanr.com/delete-account/
- https://cardscanr.com/data-deletion/
- https://cardscanr.com/auth/callback/
- https://cardscanr.com/beta/ (merged from D:\CardScanR\public_website at deploy)
- https://cardscanr.com/.well-known/assetlinks.json

Build and deploy:

```bash
python scripts/validate_legal_site.py
node scripts/deploy_to_cloudflare_pages.mjs          # builds dist/ only
node scripts/deploy_to_cloudflare_pages.mjs --deploy # builds dist/ + wrangler pages deploy
```

The deploy script copies `docs/*` into `dist/`, merges beta assets from
`D:\CardScanR\public_website\beta`
(and `assets/css/beta.css`, `assets/js/beta.js`, `assets/js/config.js`) without
overwriting `site.css` / `site.js`, and writes merged `_headers` / `_redirects`.

**Do not create `docs/CNAME` while Cloudflare Pages owns the apex domain.** Keep
`docs/CNAME.pending` in the repository for documentation; GitHub Pages fallback
continues to work without a CNAME file.

## GitHub Pages fallback

Relative links throughout `docs/` keep the site working on the project path:

- https://motiv8ed.github.io/CardScanR-Legal/
- https://motiv8ed.github.io/CardScanR-Legal/support/
- https://motiv8ed.github.io/CardScanR-Legal/feedback/
- https://motiv8ed.github.io/CardScanR-Legal/privacy/
- https://motiv8ed.github.io/CardScanR-Legal/terms/
- https://motiv8ed.github.io/CardScanR-Legal/delete-account/
- https://motiv8ed.github.io/CardScanR-Legal/auth/callback/
- https://motiv8ed.github.io/CardScanR-Legal/.well-known/assetlinks.json

Repository: `Motiv8ed/CardScanR-Legal`  
Default branch: `master`  
Pages source: `master` / `/docs`  
`docs/.nojekyll` is present so GitHub Pages serves `.well-known/` as static files.

The `/beta/` path is not in `docs/`; it appears only after Cloudflare deploy merge
or on the live custom domain.

## Play Console URLs (cardscanr.com)

Use these once the custom domain is verified live:

| Field | URL |
| ----- | --- |
| Website | https://cardscanr.com |
| Privacy policy | https://cardscanr.com/privacy/ |
| Feedback | https://cardscanr.com/feedback/ |
| Support | https://cardscanr.com/support/ |
| Account deletion | https://cardscanr.com/delete-account/ |
| Data deletion alias | https://cardscanr.com/data-deletion/ |
| OAuth return | https://cardscanr.com/auth/callback/ |
| App Links | https://cardscanr.com/.well-known/assetlinks.json |

Until DNS cutover is complete, github.io URLs remain valid fallbacks (see list above).

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

1. Edit files under `docs/` (or supporting scripts) in this repository only.
2. Run:

```bash
python scripts/validate_legal_site.py
```

3. Ensure exit code **0**.
4. For Cloudflare production: `node scripts/deploy_to_cloudflare_pages.mjs --deploy`
5. For GitHub Pages fallback: commit on `master` and push to `origin` when intentionally publishing.

### GitHub Pages settings (fallback)

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **master**
4. Folder: **/docs**
5. Custom domain: leave empty while Cloudflare Pages serves `cardscanr.com`

## Safety reminders

- Never commit Supabase service role keys, OAuth client secrets, or Turnstile secret keys.
- Publishable Supabase anon key and Turnstile site key in `feedback-config.js` are intentional.
- Do not point Pages at anything outside `docs/`.
- Do not create `docs/CNAME` until the owner confirms GitHub Pages should own the domain again.
- Re-run validation after every public HTML or Asset Links edit.
