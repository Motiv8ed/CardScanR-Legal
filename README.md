# CardScanR Legal — cardscanr-legal

Static legal/support site and Google Play readiness package for **CardScanR: TCG Card Scanner** (`com.cardscanr.app`).

## Status

**READY_TO_PUBLISH** — public HTML validated; owner inputs applied. Do not push until you explicitly choose to create the remote and enable GitHub Pages.

## Source audit

| Item | Value |
|---|---|
| App path | `D:\Card Scanner App` (junction `D:\CardScanR`) |
| HEAD | `bcb22f613d2301cccacd05f1bf3079d50ff737f8` |
| Branch | `main` |

## Layout

- `docs/` — GitHub Pages site  
- `audit/` — data, permissions, third-party, owner inputs  
- `play-console/` — Data Safety, store listing, access, content notes  
- `scripts/validate_legal_site.py` — publication gate  
- `APP_CHANGES_REQUIRED.md`, `LEGAL_READINESS_CHECKLIST.md`, `DEPLOYMENT.md`

## Validate

```bash
python scripts/validate_legal_site.py
```

## Safety

No remotes are configured by the packaging task. Do not push until owner inputs are resolved and validation passes.
