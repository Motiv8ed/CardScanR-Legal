# App Access Review Instructions — CardScanR

**For Google Play app access / reviewer instructions.**  
**Never place real passwords in this public repository.**

## Reviewer login requirements

| Item | Instruction |
|---|---|
| Account required? | Yes — Google Sign-In and/or email auth via Supabase |
| Special hardware | Android device/emulator with camera recommended; gallery import available for some flows |
| Geographic restriction | None known in source |
| Paid content gate | None in audited dependencies (confirm O9) |

## Test account requirements (owner action)

Provide in Play Console **only** (not in this public repo):

1. A dedicated reviewer Google account **or** email/password test account on the production Supabase project  
2. Password / magic credentials stored only in Play Console’s secure app access form  
3. Confirm the account completes onboarding (country/currency) so Home / Collection / Scanner are reachable  

If Google OAuth blocking reviewers: provide email/password fallback instructions.

## Google Sign-In considerations

- Flow: Supabase OAuth → `cardscanr://login-callback`  
- Reviewers must be able to complete OAuth on the review device  
- If OAuth fails in review environment, email auth is the fallback (`Continue with Email`)  
- Ensure production redirect URLs and Supabase Google provider settings are live for the release package name (`com.cardscanr.app` after rename)

## Steps to reach scanner and major features

1. Install build / open app  
2. Sign in (Google or Email)  
3. Complete onboarding if prompted (country, currency, interests)  
4. Land in app shell (Home)  
5. Open **Scan** / scanner entry from bottom navigation or scan CTA  
6. Grant **Camera** when prompted  
7. Capture or import a card; review OCR/match screens; save to collection  
8. Open **Collection** to view saved cards  
9. Open a card detail to view pricing sections (estimates; providers may be partially configured)  
10. Open **Settings** → Account, Privacy and trust, About  

## Subscription / paywall

None identified in audited source. If added later, update this document with unlock steps or reviewer promo codes (**codes only in Play Console, not here**).

## Anything the reviewer must know

- Pricing values are estimates, not live brokerage quotes  
- eBay sold-comps path may show as not configured  
- Cloud Vision “better OCR” is stubbed  
- In-app account deletion is not available; deletion is via website/email  
  (`https://motiv8ed.github.io/CardScanR-Legal/delete-account/` or cardscanr.dev@gmail.com)  
- Package rename from `com.example.card_scanner_app` must be completed for production AAB  
- Do not instruct reviewers to enable developer diagnostics unless needed for a specific bug  
- Public privacy policy: `https://motiv8ed.github.io/CardScanR-Legal/privacy/`  
- Public support: `https://motiv8ed.github.io/CardScanR-Legal/support/`  

## Placeholder for Console paste (fill privately)

```
CardScanR reviewer access
- Sign-in: [Google test account OR email]
- Email: [PROVIDE IN PLAY CONSOLE ONLY]
- Password: [PROVIDE IN PLAY CONSOLE ONLY]
- After login: complete onboarding → Scan → allow camera → save a card → Collection
- No paid subscription gate at launch: [Yes/No per owner]
```
