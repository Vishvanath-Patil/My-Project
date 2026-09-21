#!/usr/bin/env python3
"""Generate a small, valid placeholder Resume.pdf using only the Python stdlib.

Run:  python3 make_resume_pdf.py
Outputs:  assets/resume/Resume.pdf

NOTE: this is a *placeholder* — the source of truth for the resume is
resume.html. Use "Print / Save as PDF" from the resume page for a styled
copy, or overwrite this file with the real resume PDF at the same path.
"""
import os

LM = 56          # left margin (pt)
TOP = 740        # first baseline from bottom of a 612x792 page
PAGE_H = 792
FONT_IDS = {"HEL": 1, "HEB": 2, "HEI": 3}   # /F1 Helvetica, /F2 Helvetica-Bold ...
FONT_NAMES = {"HEL": "Helvetica", "HEB": "Helvetica-Bold", "HEI": "Helvetica-Oblique"}


def esc(s: str) -> str:
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def streams_for(ops):
    """ops: list of (font, size, y, text). Returns (content_bytes, length)."""
    lines = ["BT"]
    for font, size, y, text in ops:
        fid = FONT_IDS[font]
        lines.append(f"1 0 0 1 {LM} {y} Tm /F{fid} {size} Tf ({esc(text)}) Tj")
    lines.append("ET")
    content = "\n".join(lines).encode("latin-1", "replace")
    return content, len(content)


def main():
    ops = []
    y = TOP

    def heading(text, size=11, gap=4):
        nonlocal y
        ops.append(("HEB", size, y, text))
        y -= size + gap

    def line(text, size=9.5, gap=2):
        nonlocal y
        for chunk in [text[i:i + 92] for i in range(0, len(text), 92)]:
            ops.append(("HEL", size, y, chunk))
            y -= size + gap
        y -= 2
        if y < 70:  # safety: never write below printable area
            raise RuntimeError("content out of page")

    ops.append(("HEB", 22, y, "VISHVANATH PATIL")); y -= 26
    ops.append(("HEL", 11, y, "Senior Cloud Engineer  |  AWS  |  Kubernetes  |  Terraform  |  DevOps")); y -= 22
    ops.append(("HEL", 10, y,
                "Bengaluru, Karnataka, India  |  github.com/Vishvanath-Patil  |  "
                "linkedin.com/in/vishvanath-patil  |  pvishva93@gmail.com")); y -= 26

    heading("SUMMARY")
    line("Senior Cloud Engineer with 5+ years of experience designing, deploying, and operating "
         "resilient AWS infrastructure at fintech scale. AWS Certified Solutions Architect - Associate "
         "and RHCSA with hands-on expertise in Kubernetes (EKS), Terraform, CI/CD and GitOps "
         "(Jenkins, ArgoCD), and DevSecOps. Passionate about reliability, security, and automation - "
         "and about teaching the next generation of cloud engineers.")

    heading("EXPERIENCE")
    ops.append(("HEB", 12, y, "Sr Cloud Engineer - TerraPay, India  |  Feb 2024 - Present")); y -= 18
    for b in [
        "- Design and operate TerraPay's global money-movement platform on AWS; 99.9%+ uptime on payment-critical infrastructure.",
        "- Own CI/CD and GitOps pipelines (Jenkins, ArgoCD) for zero-downtime releases across EKS clusters.",
        "- Automate provisioning with Terraform; harden AWS (IAM, VPC, security groups, KMS) for PCI-DSS and fintech compliance.",
        "- Drive observability with Prometheus, Grafana, and Loki to cut alert noise and MTTR.",
        "- Mentor engineers, conduct technical interviews; recognized with TerraPay's Superlative Performance Award.",
    ]:
        line(b)
    ops.append(("HEB", 12, y, "DevOps Engineer - Tata Consultancy Services, Bangalore  |  May 2022 - Feb 2024")); y -= 18
    for b in [
        "- End-to-end AWS projects: three-tier applications, EKS platforms, serverless, and ECS/Fargate workloads.",
        "- Complete DevSecOps pipelines: Jenkins, SonarQube, Trivy, Vault, ArgoCD - security shifted left.",
    ]:
        line(b)
    ops.append(("HEB", 12, y, "Network Engineer - Alackrity Consols, Bengaluru  |  May 2018 - May 2022")); y -= 18
    for b in [
        "- Automated Linux systems administration (Ansible) and SSL/TLS certificate lifecycle management.",
        "- Enterprise network operations: CCNA-level TCP/IP, routing and switching, Sophos firewall.",
    ]:
        line(b)

    heading("SKILLS")
    for s in [
        "Cloud & Infra:   AWS (EC2, VPC, EKS, ECS/Fargate, ECR, RDS, IAM, KMS, Lambda), Terraform, Helm, Ansible, Docker",
        "CI/CD & DevSecOps:  Jenkins, ArgoCD / GitOps, SonarQube, Trivy, OWASP Dependency-Check, HashiCorp Vault",
        "Observability:   Prometheus, Grafana, Loki, CloudWatch, alerting and runbooks",
        "OS & Networking: Linux (RHEL/Rocky), Bash, SSL/TLS, TCP/IP, CCNA-level networking, Sophos firewall",
        "Application Dev: Python, Java (Spring Boot), React + TypeScript basics",
    ]:
        line(s)

    heading("CERTIFICATIONS")
    for c in [
        "- AWS Certified Solutions Architect - Associate  |  Amazon Web Services  |  Oct 2023 - Oct 2026",
        "- Red Hat Certified System Administrator (RHCSA) EX200  |  Red Hat  |  Dec 2024 - Dec 2027",
        "- Advanced Networking (CCNA)  |  NSDC  |  Feb 2022    Sophos Firewall Engineer / Technician  |  Feb 2022",
        "- Mastering SSL (TLS), Keys and Certificates  |  Udemy  |  Jul 2025",
    ]:
        line(c)

    heading("EDUCATION")
    line("B.E. / Computer Engineering - Karnataka, India")

    stream, length = streams_for(ops)

    body = []
    body.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    body.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    body.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                b"/Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> "
                b"/Contents 7 0 R >>\nendobj\n")
    body.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    body.append(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    body.append(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>\nendobj\n")
    body.append(b"7 0 obj\n<< /Length " + str(length).encode() + b" >>\nstream\n" + stream + b"\nendstream\nendobj\n")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for raw in body:
        offsets.append(len(out))
        out += raw
    xref_pos = len(out)
    n = len(body) + 1
    out += b"xref\n0 " + str(n).encode() + b"\n0000000000 65535 f \n"
    for off in offsets[1:]:
        out += ("%010d 00000 n \n" % off).encode()
    out += (b"trailer\n<< /Size " + str(n).encode() + b" /Root 1 0 R >>\nstartxref\n"
            + str(xref_pos).encode() + b"\n%%EOF")

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "resume", "Resume.pdf")
    with open(path, "wb") as f:
        f.write(bytes(out))
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
