# Legal Readiness Checklist — CardScanR

Strict owner checklist.

## Required before publishing the website

- [x] O1 Public operator name confirmed — Andrew Gore  
- [x] O2 Public support email confirmed — cardscanr.dev@gmail.com  
- [x] O3 Address omitted from public pages  
- [x] O4 GitHub Pages host confirmed — Motiv8ed / CardScanR-Legal  
- [x] O5 Governing law — Queensland, Australia  
- [x] Children posture — not directed to children; legal capacity required  
- [x] Deletion timeframe — normally within 30 days  
- [x] Privacy effective / last updated — 27 July 2026  
- [x] All `OWNER_ACTION_REQUIRED` tokens removed from `docs/**/*.html`  
- [x] Mailto links use cardscanr.dev@gmail.com  
- [x] `python scripts/validate_legal_site.py` passes  
- [x] Public GitHub repo `Motiv8ed/CardScanR-Legal` with Pages from `master` `/docs`  
- [x] HTTPS URLs live at https://motiv8ed.github.io/CardScanR-Legal/  

## Required before uploading the AAB

- [ ] `applicationId` is `com.cardscanr.app`  
- [ ] Release signing configured (not debug)  
- [ ] Privacy URL in Play Console: `https://motiv8ed.github.io/CardScanR-Legal/privacy/`  
- [ ] Account deletion URL in Play Console: `https://motiv8ed.github.io/CardScanR-Legal/delete-account/`  
- [ ] Data Safety answers match `play-console/DATA_SAFETY_WORKSHEET.md` after owner review  
- [ ] Store listing text matches honest limitations  
- [ ] Production Supabase + OAuth clients match package name  
- [ ] Merged manifest permissions reviewed  
- [ ] No secrets in the AAB beyond publishable client config  

## Required before closed testing

- [ ] In-app links to Privacy / Terms / Support / Delete  
- [ ] Reviewer test account prepared (credentials only in Play Console)  
- [ ] Camera and scan path smoke-tested on release build  
- [ ] Cloud sync smoke-tested for test account  
- [ ] Deletion runbook tested at least once on a throwaway account  
- [ ] App access instructions pasted into Play Console  

## Required before production application

- [ ] In-app account deletion implemented and verified  
- [ ] External deletion email process staffed within the published 30-day window  
- [ ] Ads/analytics/subscriptions declarations match the binary  
- [ ] Content rating questionnaire completed  
- [ ] Target audience declarations completed  
- [ ] Feature graphic / screenshots use approved brand assets only  
- [ ] Final legal HTML re-validated and redeployed if wording changed  
