# Third-Party Services — CardScanR

**Source HEAD:** `bcb22f613d2301cccacd05f1bf3079d50ff737f8`  
Processor/controller notes are engineering assessments, not legal advice.

| Provider | Feature in app | Data transmitted (evidence) | Assessment | Public privacy policy (verify later) |
|---|---|---|---|---|
| **Supabase** | Auth (email + Google OAuth), Postgres tables (`user_profiles`, `user_collections`, `user_cards`, `scan_sessions`, `card_image_manifests_current`), client init via `SUPABASE_URL` + publishable/anon key | Email/password or OAuth tokens; profile; collection rows; scan session metadata; catalogue manifest lookups | Processor for operator-controlled project; Auth user store | https://supabase.com/privacy |
| **Google Identity / OAuth** | “Continue with Google” via Supabase `signInWithOAuth(OAuthProvider.google)` | Google account auth assertions; email/name per Google/Supabase config | Independent controller for Google Account; supplies identity to Supabase | https://policies.google.com/privacy |
| **Google ML Kit Text Recognition** | On-device OCR (Latin + Japanese libs) | Card images processed on device via ML Kit APIs | On-device SDK; review Google ML Kit terms for any residual telemetry | https://developers.google.com/ml-kit/terms + Google Privacy Policy |
| **OpenCV (Android AAR)** | Native CV assist | Local image processing | Local library | N/A (library); Apache/licence review separate |
| **TCGdex** | Catalogue search / pricing (`api.tcgdex.net`) | Card name/number/set/language queries | Independent provider | https://tcgdex.dev/ (confirm privacy/terms pages on site) |
| **Pokémon TCG API** | Catalogue search (`api.pokemontcg.io`) | Card search queries | Independent provider | https://docs.pokemontcg.io/ (confirm privacy/terms) |
| **PokeWallet** | Pricing (`https://api.pokewallet.io`) when configured | Card identity / pricing requests | Independent provider | Verify on pokewallet.io (owner to confirm production use) |
| **CardScanR pricing backend** | Optional `CARDSCANR_PRICING_BACKEND_URL` `/pricing/card` | Card identity payload JSON | Operator backend if enabled — controller/processor depends on hosting | Operator policy |
| **Card image CDN / base URL** | `CARD_SCANR_IMAGE_BASE_URL` + manifests | Downloads of catalogue artwork | Operator or CDN processor | Operator / host policy |
| **eBay** | Sold-comps service scaffold | **Not transmitting in audited mobile config** (`isConfigured` false; no mobile secrets) | N/A until enabled via safe backend | https://www.ebay.com/help/policies/member-behaviour-policies/user-privacy-notice-privacy-policy |
| **Firebase / AdMob / Sentry** | — | Not in audited dependencies | N/A | — |

## Non-affiliation reminder (for public copy)

Pokémon / Nintendo / Creatures / Game Freak, eBay, TCGdex, and other catalogue providers are independent. CardScanR should continue using non-affiliation language in store and legal copy.

## Secrets policy for this legal repo

Build-time defines (`SUPABASE_URL`, keys, backend URLs) must **not** be committed here. Only the fact that they exist as configuration is recorded.
