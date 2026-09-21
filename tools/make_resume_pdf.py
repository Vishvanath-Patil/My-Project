#!/usr/bin/env python3
"""Generate a polished A4 Resume.pdf using only the Python stdlib.

Run:  python3 tools/make_resume_pdf.py
Outputs:  assets/resume/Resume.pdf

This hand-assembles a valid PDF (no external libraries, no build step) that
mirrors resume.html: A4 page, brand colour #2f5fd0, real word-wrapping via a
Helvetica glyph-width table, bullet lists, right-aligned dates, section
underline bars, and automatic multi-page pagination.

It is the file behind every "Download PDF / Download Resume" button on the
site, so keep the content below in sync with resume.html (source of truth).
For a byte-for-byte copy of the HTML page, the "Print / Save as PDF" button
is the better tool; this script produces the standalone downloadable file.
"""
import os

PAGE_W, PAGE_H = 595, 842      # A4 in points
LM = 52                        # left/right margin
TM = 788                       # first baseline from page bottom
BM = 56                        # bottom margin
CONTENT_W = PAGE_W - 2 * LM

FONT_IDS = {"HEL": 1, "HEB": 2, "HEI": 3}
FONT_NAMES = {1: "Helvetica", 2: "Helvetica-Bold", 3: "Helvetica-Oblique"}

# Named colours as PDF rg-triplets — same palette as style.css.
COL = {
    "ink":      (0.11, 0.141, 0.188),   # #1c2430
    "body":     (0.20, 0.24, 0.31),     # body bullets
    "soft":     (0.29, 0.33, 0.41),     # #4b5568 — meta/dates
    "faint":    (0.52, 0.58, 0.67),     # #8494ac — tags
    "blue":     (0.184, 0.373, 0.816),  # #2f5fd0 — brand
    "blueSoft": (0.78, 0.82, 0.93),     # #c8d2ee — section rule
}

# Helvetica glyph widths (units: 1/1000 em). Missing glyphs default to 556.
CH_W = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667,
    "'": 191, "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333,
    ".": 278, "/": 278, "0": 556, "1": 556, "2": 556, "3": 556, "4": 556,
    "5": 556, "6": 556, "7": 556, "8": 556, "9": 556, ":": 278, ";": 278,
    "<": 584, "=": 584, ">": 584, "?": 556, "@": 1015, "A": 667, "B": 667,
    "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722, "I": 278,
    "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944,
    "X": 667, "Y": 667, "Z": 611, "[": 278, "\\": 278, "]": 278, "^": 469,
    "_": 556, "`": 333, "a": 556, "b": 556, "c": 500, "d": 556, "e": 556,
    "f": 278, "g": 556, "h": 556, "i": 222, "j": 222, "k": 500, "l": 222,
    "m": 833, "n": 556, "o": 556, "p": 556, "q": 556, "r": 333, "s": 500,
    "t": 278, "u": 556, "v": 500, "w": 722, "x": 500, "y": 500, "z": 500,
    "{": 334, "|": 260, "}": 334, "~": 584,
    # non-ASCII glyphs we use (WinAnsi): bullet, en/em dash, middle dot
    "•": 350, "–": 556, "—": 1000, "·": 250,
}


def w_pt(s, size, font="HEL"):
    """Approximate rendered width of *s* in points for a given font/size."""
    k = 1.0 if font in ("HEL", "HEI") else 1.04   # bold runs slightly wider
    return sum(CH_W.get(ch, 556) for ch in s) / 1000.0 * size * k


def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


"""=========================== CONTENT (keep in sync with resume.html) =="""
ROLE = "Senior Cloud Engineer  ·  DevOps  ·  AWS  ·  Kubernetes  ·  Terraform"
CONTACT = ("Bengaluru, Karnataka, India  |  pvishva93@gmail.com  |  "
           "+91 92410 93877  |  linkedin.com/in/vishvanath-patil  |  "
           "github.com/Vishvanath-Patil")

SUMMARY = ("Senior Cloud Engineer with 8+ years of experience designing, deploying, and operating "
           "resilient AWS infrastructure at fintech scale. AWS Certified Solutions Architect – "
           "Associate and RHCSA with hands-on expertise in Kubernetes (EKS), Terraform, CI/CD and "
           "GitOps (Jenkins, ArgoCD), and DevSecOps. Passionate about reliability, security, "
           "automation — and about teaching the next generation of cloud engineers.")

EXPERIENCE = [
    {
        "role": "Sr Cloud Engineer", "company": "TerraPay",
        "meta": "Full-time · India (Hybrid)",
        "tags": "DevOps · Amazon Web Services (AWS)",
        "when": "Feb 2024 – Present",
        "points": [
            "Design and operate TerraPay's global money-movement platform on AWS — meeting 99.9%+ uptime on payment-critical infrastructure.",
            "Build and own CI/CD & GitOps pipelines (Jenkins, ArgoCD) for zero-downtime releases across EKS clusters.",
            "Automate provisioning with Terraform and harden the AWS environment (IAM, VPC, security groups, KMS) for PCI-DSS & fintech compliance.",
            "Drive observability with Prometheus, Grafana, and Loki to reduce alert noise and MTTR.",
            "Mentor engineers, conduct technical interviews, and represent the platform team's reliability culture.",
            "Recognized with TerraPay's Superlative Performance Award.",
        ],
    },
    {
        "role": "DevOps Engineer", "company": "Tata Consultancy Services",
        "meta": "Full-time · Bangalore",
        "tags": "Prometheus · Kubernetes",
        "when": "May 2022 – Feb 2024",
        "points": [
            "Delivered end-to-end AWS projects — three-tier applications, EKS platforms, serverless, and ECS/Fargate workloads.",
            "Implemented complete DevSecOps pipelines (Jenkins, SonarQube, Trivy, Vault, ArgoCD), shifting security left in the SDLC.",
        ],
    },
    {
        "role": "Network Engineer", "company": "Alackrity Consols",
        "meta": "Full-time · Bengaluru, Karnataka, India",
        "tags": "",
        "when": "May 2018 – May 2022",
        "points": [
            "Automated Linux systems administration, Ansible orchestration, and SSL/TLS certificate lifecycle management.",
            "Enterprise network operations — CCNA-level TCP/IP, routing & switching — and Sophos firewall management.",
        ],
    },
]

SKILLS = [
    ("Cloud & Infrastructure",
     "AWS (EC2, VPC, EKS, ECS/Fargate, ECR, RDS, IAM, KMS, Lambda), Terraform, Helm, Ansible, Docker"),
    ("CI/CD & DevSecOps",
     "Jenkins, ArgoCD / GitOps, SonarQube, Trivy, OWASP Dependency-Check, HashiCorp Vault"),
    ("Observability", "Prometheus, Grafana, Loki, CloudWatch, Alerting & runbooks"),
    ("OS & Networking",
     "Linux (RHEL/Rocky), Bash, SSL/TLS, TCP/IP, CCNA-level networking, Sophos firewall"),
    ("Application Dev", "Python, Java (Spring Boot), React + TypeScript basics"),
]

CERTS = [
    ("AWS Certified Solutions Architect – Associate",
     "Amazon Web Services · Oct 2023 – Oct 2026"),
    ("Red Hat Certified System Administrator (RHCSA)",
     "Red Hat · EX200 · Dec 2024 – Dec 2027"),
    ("Advanced Networking (CCNA)",
     "National Skill Development Corporation · Feb 2022"),
    ("Mastering SSL (TLS), Keys & Certificates", "Udemy · Jul 2025"),
    ("Sophos Firewall Engineer / Technician", "Sophos · Feb 2022"),
    ("Computer Hardware Professional",
     "National Skill Development Corporation · Mar 2021"),
]

EDUCATION = [
    ("B.E. / Computer Engineering",
     "Karnataka, India — Foundation for engineering, networking, and programming "
     "fundamentals (detail available on request)."),
]


class Doc:
    """Tracks the current page, cursor, and per-page operator streams."""

    def __init__(self):
        self.pages = [[]]          # list of lists of operator strings
        self.y = TM

    @property
    def page(self):
        return self.pages[-1]

    def ensure(self, need):
        """Open a new page when the next drawing would cross the bottom margin."""
        if self.y - need < BM:
            self.pages.append([])
            self.y = TM

    def advance(self, n):
        self.y -= n

    def text_at(self, text, size, font, color, x):
        r, g, b = COL[color]
        self.page.append("BT /F%d %g Tf %.3f %.3f %.3f rg 1 0 0 1 %.2f %.2f Tm (%s) Tj ET"
                         % (FONT_IDS[font], size, r, g, b, x, self.y, esc(text)))

    def rule(self, y_off, width, thickness=1.1, color="blueSoft"):
        r, g, b = COL[color]
        self.page.append("%.3f %.3f %.3f rg %.2f %.2f %.2f %.2f re f"
                         % (r, g, b, LM, self.y + y_off, width, thickness))

    def wrap(self, text, size, font="HEL", avail=CONTENT_W):
        words, lines, cur = text.split(), [], ""
        for wd in words:
            trial = (cur + " " + wd) if cur else wd
            if w_pt(trial, size, font) <= avail or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, text, *, size=9.6, font="HEL", color="body", indent=0, hang=0,
             bullet=None, leading=None, space_after=4.0, bullet_color="blue"):
        """Draw a (possibly wrapped) paragraph. `bullet` draws a glyph before
        line 1; `hang` indents every line so wrapped text lines up after it."""
        width = CONTENT_W - indent - hang
        if leading is None:
            leading = max(size + 3.4, 11.0)
        tx = LM + indent + hang
        bx = LM + indent
        for i, ln in enumerate(self.wrap(text, size, font, width)):
            self.ensure(leading)
            if bullet is not None and i == 0:
                self.text_at(bullet, size, font, bullet_color, bx)
            self.text_at(ln, size, font, color, tx)
            self.advance(leading)
        self.advance(space_after)

    def section(self, title):
        self.ensure(34)
        self.advance(8)
        self.text_at(title.upper(), 11.2, "HEB", "blue", LM)
        self.rule(-3.0, CONTENT_W, 1.1, "blueSoft")
        self.advance(14)

    def experience(self, e):
        title = "%s — %s" % (e["role"], e["company"])
        when = e["when"]
        date_w = w_pt(when, 9.2, "HEL")
        right_x = PAGE_W - LM - date_w
        budget = CONTENT_W - date_w - 14
        if w_pt(title, 10.6, "HEB") <= budget:
            self.ensure(15.2)
            self.text_at(when, 9.2, "HEL", "soft", right_x)
            self.text_at(title, 10.6, "HEB", "ink", LM)
            self.advance(15.2)
        else:
            for i, ln in enumerate(self.wrap(title, 10.6, "HEB", budget)):
                self.ensure(15.2)
                self.text_at(ln, 10.6, "HEB", "ink", LM)
                if i == 0:
                    self.text_at(when, 9.2, "HEL", "soft", right_x)
                self.advance(15.2)
        sub = "  |  ".join(x for x in (e.get("meta", ""), e.get("tags", "")) if x)
        if sub:
            self.para(sub, size=8.8, color="faint", leading=11.2, space_after=3.0)
        for pt in e["points"]:
            self.para(pt, size=9.4, leading=12.3, hang=12, bullet="•",
                      space_after=0.8)
        self.advance(2.5)

    def named(self, name, detail):
        self.para(name, size=9.6, font="HEB", color="ink", leading=12.4, space_after=0)
        if detail:
            self.para(detail, size=8.9, color="faint", leading=11.0,
                      indent=10, space_after=3.2)
        else:
            self.advance(3.2)

    def grid2(self, items, gap=26.0):
        """Two-column layout for (name, detail) pairs — mirrors .r-grid2."""
        col_w = (CONTENT_W - gap) / 2.0
        pad = 6.0
        n_size, d_size, n_lead, d_lead = 9.6, 8.9, 12.4, 11.0

        def rows(item):
            name, detail = item
            rs = [("n", ln) for ln in self.wrap(name, n_size, "HEB", col_w - 10)]
            if detail:
                rs += [("d", ln) for ln in self.wrap(detail, d_size, "HEL", col_w - 10)]
            return rs

        def height(item):
            return sum(n_lead if t == "n" else d_lead for t, _ in rows(item)) + pad

        hs = [height(it) for it in items]
        half = sum(hs) / 2.0
        acc, split = 0.0, len(items)
        for i, h in enumerate(hs):
            if acc > 0 and acc + h > half:
                split = i
                break
            acc += h
        cols = [items[:split], items[split:]]
        xs = [LM, LM + col_w + gap]
        y0 = self.y

        def draw(citems, x0):
            for item in citems:
                for t, ln in rows(item):
                    self.ensure(n_lead if t == "n" else d_lead)
                    self.text_at(ln, n_size if t == "n" else d_size,
                                 "HEB" if t == "n" else "HEL",
                                 "ink" if t == "n" else "faint",
                                 x0 + (0 if t == "n" else 10))
                    self.advance(n_lead if t == "n" else d_lead)
                self.advance(pad)

        draw(cols[0], xs[0])
        end1 = y0 - self.y
        self.y = y0
        draw(cols[1], xs[1])
        end2 = y0 - self.y
        self.y = y0 - max(end1, end2)


def compose():
    d = Doc()
    # Header
    d.text_at("Vishvanath Patil", 23, "HEB", "ink", LM)
    d.advance(21.5)
    d.text_at(ROLE, 10.8, "HEB", "blue", LM)
    d.advance(14.5)
    d.para(CONTACT, size=9.2, color="soft", leading=12.6, space_after=6)
    d.rule(-4.0, CONTENT_W, 1.6, "blue")     # brand rule under the header
    d.advance(3)

    # Sections
    d.section("Summary")
    d.para(SUMMARY, size=9.6, leading=12.8)

    d.section("Experience")
    for e in EXPERIENCE:
        d.experience(e)

    d.section("Skills")
    d.grid2(SKILLS)

    d.section("Certifications")
    d.grid2(CERTS)

    d.section("Education")
    for name, detail in EDUCATION:
        d.named(name, detail)

    return d.pages


"""=========================== PDF layout ==================================="""
def build_pdf(ops_pages, title="Vishvanath Patil - Resume",
              author="Vishvanath Patil"):
    n = len(ops_pages)
    page0, fonts0, stream0 = 3, 3 + n, 3 + n + 3
    info = stream0 + n

    objects = [(1, b"<< /Type /Catalog /Pages 2 0 R >>")]
    kids = " ".join("%d 0 R" % (page0 + i) for i in range(n))
    objects.append((2, b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids.encode(), n)))
    for i in range(n):
        page = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
                "/Resources << /Font << /F1 %d 0 R /F2 %d 0 R /F3 %d 0 R >> >> "
                "/Contents %d 0 R >>" % (PAGE_W, PAGE_H, fonts0, fonts0 + 1, fonts0 + 2, stream0 + i))
        objects.append((page0 + i, page.encode()))
    for i, name in enumerate([b"/Helvetica", b"/Helvetica-Bold", b"/Helvetica-Oblique"]):
        objects.append((fonts0 + i, b"<< /Type /Font /Subtype /Type1 /BaseFont " + name +
                        b" /Encoding /WinAnsiEncoding >>"))
    for i, ops in enumerate(ops_pages):
        content = "\n".join(ops).encode("cp1252", "replace")
        objects.append((stream0 + i, b"<< /Length %d >>\nstream\n" % len(content) +
                        content + b"\nendstream"))
    objects.append((info, b"<< /Title (%s) /Author (%s) >>"
                    % (esc(title).encode("latin-1"), esc(author).encode("latin-1"))))

    objects.sort()  # emit in object-number order
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for num, data in objects:
        offsets.append(len(out))
        out += b"%d 0 obj\n" % num + data + b"\nendobj\n"
    xref_pos = len(out)
    total = len(objects) + 1
    out += b"xref\n0 %d\n0000000000 65535 f \n" % total
    for off in offsets[1:]:
        out += ("%010d 00000 n \n" % off).encode()
    out += b"trailer\n<< /Size %d /Root 1 0 R /Info %d 0 R >>\nstartxref\n" % (total, info)
    out += str(xref_pos).encode() + b"\n%%EOF"
    return bytes(out)


def main():
    pages = compose()
    stream = build_pdf(pages)
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "resume", "Resume.pdf")
    with open(path, "wb") as f:
        f.write(stream)
    n = len(pages)
    print("wrote %s  (%d bytes, %d page%s)"
          % (path, len(stream), n, "" if n == 1 else "s"))


if __name__ == "__main__":
    main()
