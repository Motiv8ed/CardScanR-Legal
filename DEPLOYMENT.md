# Deployment — cardscanr-legal (GitHub Pages)

Do **not** push from the agent session that prepared this draft unless the owner explicitly asks. Steps below are for the owner.

## Expected public URLs

Replace `GITHUB_USERNAME` with the confirmed GitHub username or org:

- https://GITHUB_USERNAME.github.io/cardscanr-legal/
- https://GITHUB_USERNAME.github.io/cardscanr-legal/privacy/
- https://GITHUB_USERNAME.github.io/cardscanr-legal/delete-account/
- https://GITHUB_USERNAME.github.io/cardscanr-legal/data-deletion/
- https://GITHUB_USERNAME.github.io/cardscanr-legal/support/
- https://GITHUB_USERNAME.github.io/cardscanr-legal/terms/

## Steps

### 1. Resolve owner inputs and validate

1. Replace all `OWNER_ACTION_REQUIRED` tokens in `docs/` HTML.  
2. Run:

```bash
python scripts/validate_legal_site.py
```

3. Ensure the script exits **0** and update `VALIDATION_REPORT.md`.

### 2. Create the public GitHub repository

1. On GitHub, create a new **public** repository named exactly `cardscanr-legal`.  
2. Do not initialise with a conflicting README if you will push this folder as the root.  
3. Locally (from this folder), after validation:

```bash
git init
git add .
git commit -m "Publish CardScanR legal and support site."
git branch -M main
git remote add origin https://github.com/GITHUB_USERNAME/cardscanr-legal.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Repo **Settings → Pages**  
2. Source: **Deploy from a branch**  
3. Branch: **main**  
4. Folder: **/docs**  
5. Save  

### 4. Confirm HTTPS

1. Wait for the Pages build to finish (Actions / Pages status).  
2. Open the home URL with `https://`.  
3. Confirm the certificate is valid and GitHub does not show a setup error.

### 5. Test all public URLs

Visit and check mobile layout + keyboard focus:

- Home, Privacy, Delete Account, Data Deletion (should land on deletion content), Support, Terms  
- Footer links on each page  
- 404 behaviour for a nonsense path  
- mailto links open with the real support address  

### 6. Play Console — Privacy Policy URL

Paste:

`https://GITHUB_USERNAME.github.io/cardscanr-legal/privacy/`

### 7. Play Console — Data Safety / account deletion URL

Paste:

`https://GITHUB_USERNAME.github.io/cardscanr-legal/delete-account/`

(Optional alias: `.../data-deletion/`.)

## Safety reminders

- Never commit Supabase service role keys, OAuth client secrets, or reviewer passwords.  
- Do not point Pages at anything outside `docs/`.  
- Re-run validation after every public HTML edit.
