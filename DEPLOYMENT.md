# Deployment — CardScanR-Legal (GitHub Pages)

## Live public URLs

- https://motiv8ed.github.io/CardScanR-Legal/
- https://motiv8ed.github.io/CardScanR-Legal/privacy/
- https://motiv8ed.github.io/CardScanR-Legal/delete-account/
- https://motiv8ed.github.io/CardScanR-Legal/data-deletion/
- https://motiv8ed.github.io/CardScanR-Legal/support/
- https://motiv8ed.github.io/CardScanR-Legal/terms/

Repository: `Motiv8ed/CardScanR-Legal`  
Default branch: `master`  
Pages source: `master` / `/docs`  
Custom domain: **none** (do not add `docs/CNAME` or DNS for an unowned domain)

## Play Console URLs

Privacy Policy:

`https://motiv8ed.github.io/CardScanR-Legal/privacy/`

Account deletion:

`https://motiv8ed.github.io/CardScanR-Legal/delete-account/`

Optional alias:

`https://motiv8ed.github.io/CardScanR-Legal/data-deletion/`

## Maintain / redeploy

1. Edit files under `docs/` (or supporting markdown) in this repository only.  
2. Run:

```bash
python scripts/validate_legal_site.py
```

3. Ensure exit code **0**.  
4. Commit on `master` and push to `origin`.  
5. Wait for GitHub Pages to refresh, then re-check the live URLs above over HTTPS.

### Pages settings (already configured)

1. Repo **Settings → Pages**  
2. Source: **Deploy from a branch**  
3. Branch: **master**  
4. Folder: **/docs**  
5. Custom domain: leave empty  

## Safety reminders

- Never commit Supabase service role keys, OAuth client secrets, or reviewer passwords.  
- Do not point Pages at anything outside `docs/`.  
- Do not create `docs/CNAME` unless a domain you own is deliberately configured later.  
- Re-run validation after every public HTML edit.
