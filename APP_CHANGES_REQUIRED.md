# App Changes Required — CardScanR (production app)

Required or strongly recommended work in the **CardScanR application repository** before Play production.  
This legal repo must not modify the app. Items below are for the app team.

## Blockers for Play policy / Data Safety honesty

### 1. In-app account deletion — **Required**

| Status | Missing in audited build |
|---|---|
| Evidence | `PrivacyTrustScreen`: “In-app account deletion is not available”; `AccountScreen` only offers Sign out |
| Need | End-to-end delete: Auth user + `user_profiles` + `user_collections` + `user_cards` + `scan_sessions` (+ storage objects if any); irreversible confirmation UX; link to web deletion page as backup |
| Play | Account deletion must be reasonably available; web URL alone may be insufficient long-term depending on current Play rules — implement in-app |

### 2. Application ID rename — **Required**

| Current | `com.example.card_scanner_app` |
|---|---|
| Target | `com.cardscanr.app` |
| Also | Update namespace, Google OAuth client IDs, Supabase redirect allow-list, signing, deep link testing |

### 3. In-app Privacy Policy / Terms / Support links — **Required**

| Status | PrivacyTrustScreen is static copy only; no `url_launcher` to public policy URLs found in settings audit |
|---|---|
| Need | Settings links to published HTTPS privacy, terms, support, and delete-account pages |

### 4. Release signing — **Required**

| Status | Release `signingConfig` still uses debug signing in audited `build.gradle.kts` |
|---|---|
| Need | Upload key / Play App Signing ready keystore (secrets stay out of git) |

## Strongly recommended before closed testing

### 5. Deletion of residual scan artifacts

Clarify and implement retention/cleanup for captured stills and diagnostic bundles; align PrivacyTrustScreen claims with sync of `local_image_path` / `raw_ocr_text`.

### 6. Export

`ExportService` CSV path throws `UnimplementedError`. Implement export before promising backups in store copy.

### 7. Permission / photo-picker disclosure

If Android 13+ media permissions appear in merged manifest, add runtime disclosure UX as required by Play.

### 8. Consent / first-run notices

Camera purpose disclosure before first scan; account/sync disclosure before first cloud save if required by policy.

### 9. Reviewer access

Create dedicated test account on production backend; verify Google OAuth on release package name; document in Play Console (not in public git).

### 10. Production configuration

- Supabase production project with RLS verified for user-scoped tables  
- Publishable key only in client  
- Confirm which pricing providers are live; disable or hide dead eBay/Pokewallet paths if not configured  
- Remove or gate QA assets / developer tools from production builds  
- Confirm `CARD_SCANR_IMAGE_BASE_URL` / pricing backend URLs for release  

### 11. Optional analytics / ads / billing

If enabling later: update privacy policy, Data Safety, and this checklist **before** shipping.

## Not required solely for legal site publish

Completing app deletion can proceed in parallel with owner filling website contact tokens, but Play production should not ship without deletion + policy links + correct package id.
