# App Data Inventory — CardScanR

**Audit date:** 27 July 2026  
**Source repository:** `D:\Card Scanner App` (junction: `D:\CardScanR`)  
**Git HEAD inspected:** `bcb22f613d2301cccacd05f1bf3079d50ff737f8` (`main`, “Branding update ?”, 2026-07-26)  
**Package target (Play):** `com.cardscanr.app`  
**Package in audited build.gradle.kts:** `com.example.card_scanner_app` (change required)

Confidence legend used below:

1. Confirmed by source/configuration  
2. Confirmed by owner-provided project documentation  
3. Owner confirmation required  
4. App implementation still required  

Do not copy secrets, API keys, tokens, or user records into this legal repository.

---

## Brand assets copied for the legal site

| File in CardScanR-Legal | Original path | SHA-256 |
|---|---|---|
| `docs/assets/images/cardscanr_mark.png` | `card_scanner_app/assets/brand/cardscanr_mark_transparent.png` | `27E87B85B216CD7E1A820B573352D064392D6B50036301A11C4230ABF6D11589` |
| `docs/assets/images/cardscanr_logo.png` | `card_scanner_app/assets/brand/cardscanr_logo_transparent.png` | `DAC4F021C1D204861F51BBB15C24D242592BECA8182503FA7989E62FC5783D07` |
| `docs/assets/images/cardscanr_app_icon.png` | `card_scanner_app/assets/brand/cardscanr_app_icon_1024.png` | `789A3B77B6711A7EEE25B2866538D963ACB30EB7287B5AA781B791CC331FF284` |
| `docs/assets/images/play_store_icon.png` | `card_scanner_app/assets/brand/play_store_icon_1024.png` | `789A3B77B6711A7EEE25B2866538D963ACB30EB7287B5AA781B791CC331FF284` |

Brand colours from `cardscanr_brand_tokens.json`: gold `#D6A84B`, dark navy `#070B16`, ivory `#F5F1E8`. UI tokens also use charcoal `#0D1117` and action gold `#D4AF37`.

---

## Data types

### 1. Account identifiers (email, user id, auth metadata)

| Field | Detail |
|---|---|
| Evidence | `lib/services/auth_service.dart`, `lib/services/supabase_service.dart`, `lib/screens/settings/account_screen.dart` |
| Collection method | Google OAuth via Supabase; email/password via Supabase Auth |
| Purpose | Sign-in, account display, sync authorisation |
| Destination | Cloud — Supabase Auth (and session on device via supabase_flutter) |
| Third party | Supabase; Google (for Google sign-in) |
| Retention evidence | Not encoded in app (3) |
| Deletion behaviour | No in-app delete; sign-out only (1). External request process required (4) |
| Play Data Safety | Personal info → Email address; Device or other IDs → User IDs |
| Confidence | 1 |

### 2. Display name / profile name

| Field | Detail |
|---|---|
| Evidence | `user_profiles.display_name`; auth `userMetadata` `display_name` / `full_name` |
| Collection method | Onboarding/profile create; Google/email metadata |
| Purpose | Personalisation, account UI |
| Destination | Cloud `user_profiles`; may appear in auth metadata |
| Third party | Supabase |
| Retention | (3) |
| Deletion | Tied to account deletion (4) |
| Play Data Safety | Personal info → Name |
| Confidence | 1 |

### 3. Country, currency, pricing market, onboarding preferences

| Field | Detail |
|---|---|
| Evidence | `lib/models/user_profile.dart`, `lib/services/user_profile_service.dart`, onboarding screens |
| Collection method | User selection during onboarding / settings; defaults include AU market helpers |
| Purpose | Localise pricing display and market preferences |
| Destination | Cloud `user_profiles`; local preference caches |
| Third party | Supabase |
| Retention | (3) |
| Deletion | With profile (4) |
| Play Data Safety | Personal info → Address (approximate: country only — declare carefully as Other personal info / App activity preferences if preferred) |
| Confidence | 1 for collection; 3 for Play category labelling nuance |

### 4. Local inventory / collection cards

| Field | Detail |
|---|---|
| Evidence | `lib/services/inventory_database.dart`, `lib/models/inventory_card.dart` |
| Collection method | Scan save, manual add, edits |
| Purpose | Core collection management |
| Destination | Local SQLite |
| Third party | None for local store |
| Retention | Until uninstall / clear storage / user delete of rows (1) |
| Deletion | Local row delete exists for inventory operations; full account wipe (4) |
| Play Data Safety | App info and performance / App activity (user-generated collection content); Photos if user photos attached — see image notes |
| Confidence | 1 |

### 5. Cloud-synced cards and collections

| Field | Detail |
|---|---|
| Evidence | `user_card_service.dart` upserts `user_cards`; `collection_service.dart` uses `user_collections` |
| Collection method | Background/cloud sync when signed in |
| Purpose | Cross-device / backup sync of inventory |
| Destination | Supabase tables `user_cards`, `user_collections` |
| Fields of note | Card identity, condition, qty, purchase/estimate fields, notes, tags, `image_url`, `local_image_path` |
| Third party | Supabase |
| Retention | (3) |
| Deletion | (4) — no automated user delete-all |
| Play Data Safety | App activity; Photos and videos **only if** user photos are uploaded — audited sync sends URLs/path strings; binary photo upload of captures not confirmed as a dedicated storage upload path (1 for metadata sync; 3 for whether path strings ever contain sensitive local paths) |
| Confidence | 1 |

### 6. Scan session metadata (including raw OCR text)

| Field | Detail |
|---|---|
| Evidence | `lib/models/scan_session.dart`, `lib/services/scan_session_service.dart` → `scan_sessions` |
| Collection method | Cloud save when signed in |
| Purpose | Session history / diagnostics of scan activity |
| Destination | Supabase `scan_sessions` |
| Third party | Supabase |
| Retention | (3) |
| Deletion | (4) |
| Play Data Safety | App activity; may include Other user-generated content (OCR text) |
| Confidence | 1 |

### 7. Camera frames and gallery photographs

| Field | Detail |
|---|---|
| Evidence | `AndroidManifest` CAMERA; `camera` + `image_picker` usage in scanner screens; PrivacyTrustScreen copy |
| Collection method | Live camera / still capture / gallery pick |
| Purpose | OCR and card matching |
| Destination | Processed on device via ML Kit / OpenCV; in-app copy says images stay on device unless diagnostics export or explicit sending workflow |
| Cloud Vision | Stub only — returns null (`cloud_vision_ocr_service.dart`) (1) |
| Retention of captures | Not a fixed encoded TTL found (3) |
| Deletion | Not a dedicated user control for all residual scan files (4/3) |
| Play Data Safety | Photos and videos — collected for app functionality; ephemeral processing may apply for live frames but still/gallery files may persist locally — **do not claim ephemeral-only without owner+QA confirmation** (3) |
| Confidence | 1 for collection purpose; 3 for retention/ephemeral Play answers |

### 8. Catalogue artwork downloads

| Field | Detail |
|---|---|
| Evidence | `card_image_cloud/*`, `cached_network_image`, `card_image_manifests_current` |
| Collection method | HTTPS download of provider/CDN artwork referenced by card id |
| Purpose | Display official catalogue images |
| Destination | Local cache on device; manifests via Supabase |
| Third party | Supabase / configured image base URL (`CARD_SCANR_IMAGE_BASE_URL`) |
| Note | These are catalogue assets, not the user’s private photos |
| Play Data Safety | Generally not user personal data; network access only |
| Confidence | 1 |

### 9. Pricing / catalogue query payloads

| Field | Detail |
|---|---|
| Evidence | `tcgdex_service.dart`, `pokemon_tcg_api.dart`, `pokewallet_pricing_service.dart`, `card_pricing_backend_service.dart`, `ebay_sold_pricing_service.dart` |
| Collection method | HTTPS GET/POST with card name/set/number/language/etc. |
| Purpose | Match cards and estimate values |
| Destination | Third-party APIs / optional backend |
| eBay | Module present; `isConfigured == false` in audited mobile code (1) |
| Retention | Provider-side unknown (3) |
| Play Data Safety | App activity (search/query data). Not financial info unless purchase prices entered by user — purchase price fields exist on cards (1) |
| Confidence | 1 |

### 10. User-entered purchase prices / sale flags / notes

| Field | Detail |
|---|---|
| Evidence | `UserCard` / `InventoryCard` purchase and notes fields |
| Collection method | User input |
| Purpose | Collection valuation personalisation |
| Destination | Local DB; cloud sync when signed in |
| Play Data Safety | Financial info → User payment info is **not** collected via Play Billing in audit; purchase price on a card is user-entered collection metadata — declare as Other financial info or App activity carefully (3 for exact Play checkbox) |
| Confidence | 1 for existence; 3 for Play categorisation |

### 11. Device preferences and settings

| Field | Detail |
|---|---|
| Evidence | `shared_preferences` across settings, scanner, welcome, cache settings |
| Purpose | UX preferences, developer unlock flags, market prefs |
| Destination | Local |
| Play Data Safety | App info and performance → Other app performance data (optional) |
| Confidence | 1 |

### 12. Diagnostic / crash log exports

| Field | Detail |
|---|---|
| Evidence | `privacy_trust_screen.dart`; `diagnostics/*`; scanner diagnostics export services |
| Collection method | User-initiated export / developer diagnostics |
| Purpose | Troubleshooting |
| Destination | Local files; shared only if user shares them |
| Third party | None automatic in audited deps (no Crashlytics/Sentry) |
| Play Data Safety | App info and performance → Crash logs / Diagnostics — only if collected. Currently optional/local (1). Launch analytics plan (3) |
| Confidence | 1 |

### 13. Advertising identifiers / ads

| Field | Detail |
|---|---|
| Evidence | No AdMob or ads SDK in `pubspec.yaml` |
| Status | Not collected by audited dependencies (1). Launch intent (3) |
| Play Data Safety | Declare no advertising ID collection unless added later |
| Confidence | 1 for current source; 3 for store declaration at launch |

### 14. Approximate location

| Field | Detail |
|---|---|
| Evidence | No location permission in manifest; country is user-selected profile field |
| Status | No device location permission found (1) |
| Confidence | 1 |

---

## Summary for policy authors

- **Do claim:** Supabase auth (Google + email), profile/onboarding fields, local SQLite inventory, optional cloud sync of cards/collections/scan sessions, on-device ML Kit OCR, catalogue/pricing HTTPS queries, optional local diagnostics.  
- **Do not claim:** Immediate deletion of scan photos; encryption-at-rest guarantees; fixed retention days; GDPR/CCPA “compliance”; working in-app account deletion; active eBay API comps; active Cloud Vision; Firebase Analytics; ads; Play Billing subscriptions — unless later confirmed.
