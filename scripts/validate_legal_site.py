#!/usr/bin/env python3
"""Validate the CardScanR legal site under docs/ (stdlib only).

Fails (exit 1) when the public site is not publication-ready.
Writes VALIDATION_REPORT.md in the repository root.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORT_PATH = ROOT / "VALIDATION_REPORT.md"

REQUIRED_PATHS = [
    "index.html",
    "privacy/index.html",
    "delete-account/index.html",
    "data-deletion/index.html",
    "support/index.html",
    "feedback/index.html",
    "terms/index.html",
    "auth/callback/index.html",
    ".well-known/assetlinks.json",
    "404.html",
    "assets/css/site.css",
    "assets/js/site.js",
    "assets/js/feedback-config.js",
    "assets/js/feedback.js",
    "_headers",
    "_redirects",
    ".nojekyll",
    "robots.txt",
]

# At least one of these must exist (Cloudflare Pages owns domain; GitHub uses pending).
CNAME_OPTIONS = ["CNAME", "CNAME.pending"]

# Merged into dist at Cloudflare deploy — not required in docs/ for link checks.
DEPLOY_MERGED_PREFIXES = ("beta/", "beta")

PLACEHOLDER_PATTERNS = [
    re.compile(r"OWNER_ACTION_REQUIRED", re.I),
    re.compile(r"\bTODO\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"example\.com", re.I),
    re.compile(r"YOUR_[A-Z0-9_]+"),
    re.compile(r"REPLACE_ME", re.I),
    re.compile(r"TBD_EMAIL", re.I),
    re.compile(r"\[insert[^\]]*\]", re.I),
    re.compile(r"lorem ipsum", re.I),
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk_live_[A-Za-z0-9]+\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"service_role", re.I),
    re.compile(r"SUPABASE_SERVICE_ROLE"),
    re.compile(r"-----BEGIN CERTIFICATE-----"),
]

REMOTE_SCRIPT_BLOCK = re.compile(r"<script[^>]+src=['\"]https?://", re.I)
ANALYTICS_BLOCK = re.compile(
    r"googletagmanager|google-analytics|gtag\(|facebook\.net|hotjar|segment\.com|mixpanel|plausible\.io|clarity\.ms",
    re.I,
)
TURNSTILE_ALLOWED = re.compile(r"^https://challenges\.cloudflare\.com/", re.I)
CANONICAL_RE = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']https://cardscanr\.com/[^"\']*["\']',
    re.I,
)
FEEDBACK_NAV_RE = re.compile(r'href=["\'][^"\']*feedback/?["\']', re.I)

WINDOWS_PATH = re.compile(r"[A-Za-z]:\\|/Users/|/home/\w+/")
LOCALHOST = re.compile(r"localhost|127\.0\.0\.1", re.I)

CONTACT_HINT = re.compile(
    r"(mailto:)|(\bemail\b)|(\bsupport\b)|(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    re.I,
)

SHA256_FINGERPRINT = re.compile(
    r"^[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){31}$"
)


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.scripts: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag == "a" and ad.get("href"):
            self.hrefs.append(ad["href"])
        if tag == "link" and ad.get("href"):
            self.hrefs.append(ad["href"])
        if tag == "img" and ad.get("src"):
            self.hrefs.append(ad["src"])
        if tag == "script":
            src = ad.get("src", "")
            if src:
                self.scripts.append(src)
                self.hrefs.append(src)

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.text_chunks.append(data)


def rel_from_docs(path: Path) -> str:
    return path.relative_to(DOCS).as_posix()


def is_deploy_merged_href(href: str) -> bool:
    href = href.strip().rstrip("/")
    for prefix in DEPLOY_MERGED_PREFIXES:
        if href == prefix or href.endswith("/" + prefix) or href.endswith(prefix):
            return True
        if href.startswith(prefix + "/") or href.startswith("../" + prefix):
            return True
    return "beta/" in href or href.endswith("/beta") or href == "beta"


def resolve_href(page: Path, href: str) -> Path | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https", "data", "javascript"}:
        return None
    if parsed.scheme and parsed.scheme not in {"", "file"}:
        return None
    raw = unquote(parsed.path)
    if not raw:
        return None
    base = page.parent
    target = (base / raw).resolve()
    try:
        target.relative_to(DOCS.resolve())
    except ValueError:
        return target
    if target.is_dir():
        index = target / "index.html"
        return index if index.exists() else target
    return target


def validate_assetlinks(failures: list[str], notes: list[str]) -> None:
    path = DOCS / ".well-known" / "assetlinks.json"
    if not path.exists():
        return
    rel = ".well-known/assetlinks.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{rel}: invalid JSON ({exc})")
        return

    if not isinstance(data, list) or not data:
        failures.append(f"{rel}: expected a non-empty JSON array")
        return

    entry = data[0]
    if not isinstance(entry, dict):
        failures.append(f"{rel}: first entry must be an object")
        return

    target = entry.get("target")
    if not isinstance(target, dict):
        failures.append(f"{rel}: missing target object")
        return

    if target.get("namespace") != "android_app":
        failures.append(f"{rel}: target.namespace must be android_app")
    if target.get("package_name") != "com.cardscanr.app":
        failures.append(f"{rel}: package_name must be com.cardscanr.app")

    fps = target.get("sha256_cert_fingerprints")
    if not isinstance(fps, list):
        failures.append(f"{rel}: sha256_cert_fingerprints must be an array")
        return

    for fp in fps:
        if not isinstance(fp, str) or not SHA256_FINGERPRINT.match(fp):
            failures.append(f"{rel}: malformed sha256 fingerprint: {fp!r}")

    if fps:
        notes.append(
            f"{rel}: {len(fps)} sha256_cert_fingerprints present "
            "(upload/test certs only until Play App Signing fingerprint is added — see DEPLOYMENT.md)"
        )
    else:
        notes.append(f"{rel}: sha256_cert_fingerprints is empty — App Links incomplete")


def validate_cname(failures: list[str], notes: list[str]) -> None:
    found = [name for name in CNAME_OPTIONS if (DOCS / name).exists()]
    if not found:
        failures.append(
            "Missing domain marker: docs/CNAME or docs/CNAME.pending required"
        )
        return
    if len(found) > 1:
        notes.append(
            "Both CNAME and CNAME.pending exist — Cloudflare Pages should use CNAME; "
            "remove docs/CNAME from GitHub Pages branch if github.io fallback must stay active"
        )
    for name in found:
        content = (DOCS / name).read_text(encoding="utf-8").strip()
        if content != "cardscanr.com":
            failures.append(f"{name}: expected 'cardscanr.com', found {content!r}")
        else:
            notes.append(f"{name} present with cardscanr.com")


def validate_remote_scripts(rel: str, text: str, failures: list[str]) -> None:
    is_feedback = rel == "feedback/index.html"
    if ANALYTICS_BLOCK.search(text):
        failures.append(f"{rel}: remote script/analytics pattern matched")

    parser = LinkCollector()
    try:
        parser.feed(text)
    except Exception:
        parser.scripts = []

    for src in parser.scripts:
        if not src.startswith(("http://", "https://", "//")):
            continue
        normalised = src if not src.startswith("//") else "https:" + src
        if is_feedback and TURNSTILE_ALLOWED.match(normalised):
            continue
        failures.append(f"{rel}: remote script src '{src}'")

    if not is_feedback and REMOTE_SCRIPT_BLOCK.search(text):
        failures.append(f"{rel}: remote script tag found")


def main() -> int:
    failures: list[str] = []
    notes: list[str] = []
    pages_checked: list[str] = []

    if not DOCS.is_dir():
        failures.append("docs/ directory missing")
        write_report(failures, notes, pages_checked)
        return 1

    for rel in REQUIRED_PATHS:
        if not (DOCS / rel).exists():
            failures.append(f"Required path missing: docs/{rel}")

    validate_assetlinks(failures, notes)
    validate_cname(failures, notes)

    html_files = sorted(DOCS.rglob("*.html"))
    if not html_files:
        failures.append("No HTML files under docs/")

    for page in html_files:
        rel = rel_from_docs(page)
        pages_checked.append(rel)
        text = page.read_text(encoding="utf-8")

        for pat in PLACEHOLDER_PATTERNS:
            if pat.search(text):
                failures.append(f"{rel}: placeholder/token matched /{pat.pattern}/")

        if WINDOWS_PATH.search(text):
            failures.append(f"{rel}: Windows or absolute filesystem path found")

        if LOCALHOST.search(text):
            failures.append(f"{rel}: localhost reference found")

        for pat in SECRET_PATTERNS:
            if pat.search(text):
                failures.append(f"{rel}: secret-like pattern matched /{pat.pattern}/")

        validate_remote_scripts(rel, text, failures)

        if not CANONICAL_RE.search(text):
            failures.append(
                f"{rel}: missing canonical link https://cardscanr.com/..."
            )

        if rel in {"index.html", "support/index.html", "feedback/index.html"}:
            if not FEEDBACK_NAV_RE.search(text):
                failures.append(f"{rel}: Feedback link missing from navigation")

        parser = LinkCollector()
        try:
            parser.feed(text)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{rel}: HTML parse error: {exc}")
            continue

        for href in parser.hrefs:
            if is_deploy_merged_href(href):
                continue
            target = resolve_href(page, href)
            if target is None:
                continue
            if not target.exists():
                failures.append(f"{rel}: broken internal link '{href}' -> {target}")

        body = " ".join(parser.text_chunks) + "\n" + text
        if rel in {
            "privacy/index.html",
            "delete-account/index.html",
            "data-deletion/index.html",
            "auth/callback/index.html",
        }:
            if "CardScanR" not in body:
                failures.append(f"{rel}: does not identify CardScanR")

        if rel in {
            "index.html",
            "privacy/index.html",
            "delete-account/index.html",
            "support/index.html",
            "feedback/index.html",
            "terms/index.html",
            "auth/callback/index.html",
        }:
            if not CONTACT_HINT.search(body):
                failures.append(f"{rel}: contact information appears missing")

        if rel == "auth/callback/index.html":
            if "cardscanr://login-callback" not in text:
                failures.append(f"{rel}: missing cardscanr://login-callback deep-link fallback")

    if any(
        "OWNER_ACTION_REQUIRED" in (DOCS / p).read_text(encoding="utf-8")
        for p in [
            "index.html",
            "privacy/index.html",
            "delete-account/index.html",
            "support/index.html",
            "feedback/index.html",
            "terms/index.html",
            "auth/callback/index.html",
        ]
        if (DOCS / p).exists()
    ):
        notes.append(
            "Public docs are NOT publishable until owner inputs used by public pages are resolved."
        )

    for img in [
        "assets/images/cardscanr_mark.png",
        "assets/images/cardscanr_logo.png",
    ]:
        if not (DOCS / img).exists():
            failures.append(f"Missing brand asset docs/{img}")
        else:
            digest = hashlib.sha256((DOCS / img).read_bytes()).hexdigest().upper()
            notes.append(f"SHA-256 docs/{img} = {digest}")

    write_report(failures, notes, pages_checked)
    if failures:
        print(f"VALIDATION FAILED with {len(failures)} issue(s). See VALIDATION_REPORT.md")
        for item in failures[:30]:
            print(f" - {item}")
        if len(failures) > 30:
            print(f" - … {len(failures) - 30} more")
        return 1

    print("VALIDATION PASSED")
    return 0


def write_report(failures: list[str], notes: list[str], pages: list[str]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    status = "FAILED" if failures else "PASSED"
    lines = [
        "# Validation Report",
        "",
        f"- Generated: {now}",
        f"- Result: **{status}**",
        f"- Docs root: `{DOCS}`",
        f"- Pages checked: {len(pages)}",
        "",
        "## Pages",
        "",
    ]
    for p in pages:
        lines.append(f"- `{p}`")
    lines.extend(["", "## Failures", ""])
    if failures:
        seen: set[str] = set()
        for f in failures:
            if f in seen:
                continue
            seen.add(f)
            lines.append(f"- {f}")
    else:
        lines.append("- None")
    lines.extend(["", "## Notes", ""])
    if notes:
        for n in notes:
            lines.append(f"- {n}")
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Publication gate",
            "",
            (
                "Not publishable."
                if failures
                else "Publishable - owner inputs appear resolved and structural checks passed."
            ),
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
