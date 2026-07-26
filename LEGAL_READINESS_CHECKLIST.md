# Legal Readiness Checklist — CardScanR

Strict owner checklist. Tick only when done.

## Required before publishing the website

- [ ] O1 Public legal/trading name confirmed  
- [ ] O2 Public support email confirmed and monitored  
- [ ] O3 Address decision confirmed (publish or omit knowingly)  
- [ ] O4 GitHub username confirmed  
- [ ] O5 Governing law confirmed  
- [ ] O6/O7 Age / children posture confirmed  
- [ ] O15/O16 Retention + deletion timeframe confirmed  
- [ ] O19 Hosting region wording confirmed if mentioned publicly  
- [ ] O21 Privacy effective date set  
- [ ] Replace every `OWNER_ACTION_REQUIRED` token in `docs/**/*.html`  
- [ ] Prefill mailto links use the real support email  
- [ ] Run `python scripts/validate_legal_site.py` — **must pass**  
- [ ] Commit only after validation passes (or clearly mark draft; do not call it production-ready)  
- [ ] Create public GitHub repo `cardscanr-legal` and enable Pages from `/docs`  
- [ ] Verify HTTPS URLs load on mobile and desktop  

## Required before uploading the AAB

- [ ] `applicationId` is `com.cardscanr.app`  
- [ ] Release signing configured (not debug)  
- [ ] Privacy URL live in Play Console  
- [ ] Account deletion URL live  
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
- [ ] External deletion email process staffed within published timeframe  
- [ ] Ads/analytics/subscriptions declarations match the binary (O9–O11)  
- [ ] Content rating questionnaire completed  
- [ ] Target audience declarations completed  
- [ ] Feature graphic / screenshots use approved brand assets only  
- [ ] Final legal HTML re-validated and redeployed if wording changed  
- [ ] Confirm CardScanR app repository was not modified by the legal packaging task (separate PR for app work)
