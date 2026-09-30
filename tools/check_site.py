#!/usr/bin/env python3
"""Consistency checker for the portfolio site (stdlib-only, no external deps).

Run:  python3 tools/check_site.py
Exits 0 when every invariant holds, 1 otherwise (so it can gate a deploy/CI).

The site has no tests by design (see CLAUDE.md), but it does have invariants
documented as architecture:
  * the header nav and footer are duplicated BY HAND in every page — they
    must stay byte-identical across pages,
  * personal details (email / phone / location / WhatsApp) must live in ONE
    place — siteConfig in assets/js/site.js — never pasted into HTML,
  * the resume exists in three synced forms (resume.html · Resume.pdf via
    make_resume_pdf.py · siteConfig),
  * static fallback stats should match the config they fall back to,
  * the sitemap must cover exactly the served pages.

This script guards all of those so a careless edit can't silently unsync them.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = ["index.html", "resume.html", "products.html", "contact.html", "404.html"]
CONTENT_PAGES = PAGES[:-1]          # 404.html has no footer
SITE_JS = "assets/js/site.js"
MAKE_PDF = "tools/make_resume_pdf.py"

# Contact literals that must never be pasted into HTML (they live in siteConfig).
# The JSON-LD block on index.html is exempt: it deliberately mirrors the email
# for search engines (see check_single_edit_point below).
LITERALS = [
    "pvishva93@gmail.com",
    "+91 92410 93877",
    "919241093877",
]

# A location like "Bengaluru, Karnataka, India" also appears legitimately as a
# *company's* job location, so instead of scanning for it we assert the
# data-location / data-email / data-phone / data-wa hooks exist where expected.
HOOKS = {
    "index.html":     ("data-email", "data-location"),
    "resume.html":    ("data-email", "data-phone", "data-location"),
    "products.html":  ("data-email",),
    "contact.html":   ("data-email", "data-phone", "data-location", "data-wa"),
}

failures = []


def fail(scope, msg):
    failures.append("[%s] %s" % (scope, msg))


def read(path, kind="html"):
    fp = os.path.join(ROOT, path)
    if not os.path.isfile(fp):
        fail("files", "missing %s" % path)
        return ""
    with open(fp, encoding="utf-8") as f:
        return f.read()


def between(text, start, end):
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i + len(start))
    if j < 0:
        return None
    return text[i:j + len(end)]


def extract_config(src):
    """Pull the fields the site itself reads out of site.js."""
    def grab(pattern):
        m = re.search(pattern, src)
        return m.group(1).replace('\\"', '"') if m else None

    certs_block = re.search(r'certs:\s*\[(.*?)\]\s*\}', src, re.S)
    exp_block = re.search(r'var experience\s*=\s*\[(.*?)\]\s*;', src, re.S)
    certs = re.findall(r'\bname:\s*"', certs_block.group(1) if certs_block else "")
    vals = re.findall(r'\b(?:role|company|when):\s*"([^"]*)"',
                      exp_block.group(1) if exp_block else "")
    return {
        "email": grab(r'email:\s*"([^"]*)"'),
        "phone": grab(r'phone:\s*"([^"]*)"'),
        "location": grab(r'location:\s*"([^"]*)"'),
        "certs": len(certs),
        "jobs": [vals[i:i + 3] for i in range(0, len(vals), 3)],
    }


def extract_pdf_jobs(src):
    """(role, company) pairs from make_resume_pdf.py's EXPERIENCE list."""
    return re.findall(r'"role":\s*"([^"]*)"\s*,\s*"company":\s*"([^"]*)"', src)


# ---------------------------------------------------------------- checks
def check_nav_footer():
    def norm(block):
        # the current-page marker is the one intentional per-page difference;
        # blank lines / trailing spaces are cosmetic and not real divergence
        block = re.sub(r' aria-current="page"', "", block)
        return re.sub(r'[ \t]+\n|\n\s*\n', "\n", block).strip()

    navs, footers = {}, {}
    for p in PAGES:
        html = read(p)
        nav = between(html, '<header class="nav">', "</header>")
        if nav is None:
            fail("nav/footer", "%s: nav block not found" % p)
            continue
        navs.setdefault(norm(nav), []).append(p)
    if len(navs) > 1:
        for nav, pages in navs.items():
            fail("nav/footer", "nav differs between pages: %s" % ", ".join(pages))

    for p in CONTENT_PAGES:
        html = read(p)
        footer = between(html, '<footer class="footer">', "</footer>")
        if footer is None:
            fail("nav/footer", "%s: footer block not found" % p)
            continue
        footers.setdefault(footer, []).append(p)
    if len(footers) > 1:
        for footer, pages in footers.items():
            fail("nav/footer", "footer differs between pages: %s" % ", ".join(pages))

    print("  nav + footer blocks identical across pages")


def strip_json_ld(html):
    """Remove <script type="application/ld+json"> blocks — they intentionally
    mirror contact details for crawlers and are not the single-edit-point."""
    return re.sub(r'<script type="application/ld\+json">.*?</script>', "", html, flags=re.S)


def check_single_edit_point():
    for p in PAGES:
        html = strip_json_ld(read(p))
        for lit in LITERALS:
            if lit in html:
                fail("contact", "%s hardcodes %r — move it into siteConfig (site.js)" % (p, lit))
    for p, hooks in HOOKS.items():
        html = read(p)
        for h in hooks:
            if h not in html:
                fail("contact", "%s is missing the %s hook" % (p, h))
    print("  no personal-contact literals in pages; expected hooks present")


def check_no_flash_snippet():
    marker = "No-flash theme"
    for p in PAGES:
        if marker not in read(p):
            fail("theme", "%s is missing the no-flash theme snippet in <head>" % p)
    print("  every page has the no-flash theme snippet")


def check_config_and_stats(cfg):
    if not cfg["email"] or not cfg["phone"] or not cfg["location"]:
        fail("config", "siteConfig is missing email/phone/location")

    index = read("index.html")
    fallback = re.search(r'data-stat="certs">(\d+)<', index)
    static = int(fallback.group(1)) if fallback else None
    if static is not None and static != cfg["certs"]:
        fail("config", "index.html cert fallback says %d, siteConfig has %d certs"
             % (static, cfg["certs"]))

    idx_cert_blocks = len(re.findall(r'<div class="cert">', index))
    if idx_cert_blocks != cfg["certs"]:
        fail("config", "index.html shows %d certification cards, siteConfig lists %d"
             % (idx_cert_blocks, cfg["certs"]))

    resume = read("resume.html")
    certs_sec = between(resume, "<h2>Certifications</h2>", "</section>") or ""
    resume_certs = len(re.findall(r'<div class="r-item">', certs_sec))
    if resume_certs != cfg["certs"]:
        fail("config", "resume.html shows %d certifications, siteConfig lists %d"
             % (resume_certs, cfg["certs"]))

    print("  cert counts in sync (siteConfig = index = resume = %d)" % cfg["certs"])


def check_experience_sync(cfg):
    resume = read("resume.html")
    pdf = read(MAKE_PDF, "py")
    pdf_jobs = extract_pdf_jobs(pdf)

    for role, company, when in cfg["jobs"]:
        if role not in resume:
            fail("resume", "resume.html is missing role %r (in siteConfig)" % role)
        if company not in resume:
            fail("resume", "resume.html is missing company %r (in siteConfig)" % company)
        if not any(r == role and c == company for r, c in pdf_jobs):
            fail("pdf", "make_resume_pdf.py is missing (%s @ %s) — keep it in sync with resume.html" % (role, company))

    if len(cfg["jobs"]) != len(pdf_jobs):
        fail("pdf", "%d jobs in siteConfig, %d in make_resume_pdf.py EXPERIENCE"
             % (len(cfg["jobs"]), len(pdf_jobs)))
    print("  resume.html + Resume.pdf-EXPERIENCE match siteConfig jobs (%d)" % len(cfg["jobs"]))


def check_sitemap():
    sitemap = read("sitemap.xml")
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
    names = set()
    for loc in locs:
        if loc.strip().endswith("/"):
            names.add("index.html")          # the root page entry "…/My-Project/"
        else:
            names.add(loc.strip().rsplit("/", 1)[-1])
    expected = set(CONTENT_PAGES)
    if names != expected:
        fail("sitemap", "sitemap covers %s; expected %s"
             % (", ".join(sorted(names)), ", ".join(sorted(expected))))

    robots = read("robots.txt", "txt")
    if "sitemap.xml" not in robots:
        fail("robots", "robots.txt does not reference the sitemap")
    for p in CONTENT_PAGES + ["404.html"]:
        if not os.path.isfile(os.path.join(ROOT, p)):
            fail("files", "missing page %s" % p)
    print("  sitemap + robots consistent with the served pages")


def main():
    print("checking %s …" % ROOT)
    cfg = extract_config(read(SITE_JS, "js"))
    check_nav_footer()
    check_single_edit_point()
    check_no_flash_snippet()
    check_config_and_stats(cfg)
    check_experience_sync(cfg)
    check_sitemap()

    if failures:
        print("\n%d problem%s found:\n" % (len(failures), "" if len(failures) == 1 else "s"))
        for f in failures:
            print("  ✗ " + f)
        print("\nFix the issues above, or run the site's generators again:")
        print("  python3 tools/make_resume_pdf.py")
        sys.exit(1)
    print("\nAll checks passed ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
