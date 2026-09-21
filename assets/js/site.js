/* ============================================================
   Vishvanath Patil — Career Portfolio
   site.js — personal data + theme/nav interactions
   ============================================================ */

/* ------------------------------------------------------------
   1. SITE CONFIG — ✏️ EDIT YOUR DETAILS HERE (single edit point)
   GitHub  : https://github.com/Vishvanath-Patil
   LinkedIn: https://www.linkedin.com/in/vishvanath-patil/
   ------------------------------------------------------------ */
var siteConfig = {
  name: "Vishvanath Patil",
  initials: "VP",
  role: "Senior Cloud Engineer",
  company: "TerraPay",
  companyUrl: "",               // ← optional company website (leave "" to hide link)
  location: "Bengaluru, Karnataka, India",
  summary:
    "Cloud & DevOps engineer with 5+ years of experience designing, deploying, and " +
    "operating resilient infrastructure on AWS. AWS Certified Solutions Architect and " +
    "Red Hat Certified System Administrator building CI/CD pipelines, Kubernetes " +
    "platforms, and GitOps workflows that ship fintech-scale systems with confidence.",
  email: "pvishva93@gmail.com",
  phone: "+91 92410 93877",
  whatsapp: "https://wa.me/919241093877",     // WhatsApp · +91 9241093877
  socials: {
    linkedin:  { url: "https://www.linkedin.com/in/vishvanath-patil/",  label: "LinkedIn"  },
    github:    { url: "https://github.com/Vishvanath-Patil",            label: "GitHub"    },
    instagram: { url: "https://instagram.com/vishvanath.patil",         label: "Instagram" }, // ← ✏️ replace
    youtube:   { url: "https://youtube.com/@VishvanathPatil",           label: "YouTube"   }  // ← ✏️ replace
  },
  stats: {
    years: "5+",
    repos: "117+",
    certs: "6"
  }
};

/* ------------------------------------------------------------
   2. SOCIAL ICONS (inline SVG — no external requests)
   ------------------------------------------------------------ */
var socialIcon = {
  linkedin:
    '<svg viewBox="0 0 24 24" fill="currentColor" role="img" aria-hidden="true" focusable="false"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.8 0 0 .78 0 1.74v20.52C0 23.22.8 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.74V1.74C24 .78 23.2 0 22.22 0z"/></svg>',
  github:
    '<svg viewBox="0 0 24 24" fill="currentColor" role="img" aria-hidden="true" focusable="false"><path d="M12 .3a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.31 3.5 1 .1-.78.42-1.31.76-1.61-2.66-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.49 5.92.43.38.82 1.12.82 2.26v3.35c0 .32.22.7.83.58A12 12 0 0 0 12 .3z"/></svg>',
  instagram:
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
  youtube:
    '<svg viewBox="0 0 24 24" fill="currentColor" role="img" aria-hidden="true" focusable="false"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19C0 8.07 0 12 0 12s0 3.93.5 5.81a3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14C24 15.93 24 12 24 12s0-3.93-.5-5.81zM9.55 15.57V8.43L15.82 12l-6.27 3.57z"/></svg>'
};

/* ------------------------------------------------------------
   3. RENDER SOCIAL LINKS — runs on every page
   ------------------------------------------------------------ */
function renderSocials() {
  var hosts = document.querySelectorAll("[data-socials]");
  hosts.forEach(function (host, hi) {
    var out = "";
    Object.keys(siteConfig.socials).forEach(function (net) {
      var s = siteConfig.socials[net];
      out +=
        '<li><a href="' + s.url.replace(/&/g, "&amp;") + '" target="_blank" rel="noopener" ' +
        'data-net="' + net + '" aria-label="' + s.label + ' (opens in a new tab)">' +
        socialIcon[net] + "</a></li>";
    });
    // mail icon: only on the home/contact hosts that opt in
    if (host.getAttribute("data-socials") === "mail") {
      out +=
        '<li><a href="mailto:' + siteConfig.email.replace(/&/g, "&amp;") +
        '" data-net="mail" aria-label="Email">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></a></li>';
    }
    host.innerHTML = out;
  });
}

/* ------------------------------------------------------------
   4. EXPERIENCE DATA — used by index + resume (single edit point)
   To add or edit a job, just change this array.
   ------------------------------------------------------------ */
var experience = [
  {
    role: "Sr Cloud Engineer",
    company: "TerraPay",
    where: "India · Hybrid",
    when: "Feb 2024 - Present",
    skills: ["DevOps", "Amazon Web Services (AWS)"],
    points: [
      "Design and operate TerraPay's global money-movement platform on AWS — meeting 99.9%+ uptime on payment-critical infrastructure.",
      "Build and own CI/CD & GitOps pipelines (Jenkins, ArgoCD) powering zero-downtime releases across EKS clusters.",
      "Automate cloud provisioning with Terraform and harden the AWS environment — IAM, VPC, security groups, KMS — in line with PCI-DSS and fintech compliance.",
      "Drive observability with Prometheus, Grafana, and Loki; slash alert noise and mean-time-to-recovery with runbooks.",
      "Mentor engineers and conduct technical interviews to grow the platform team.",
      "Recognized with TerraPay's Superlative Performance Award."
    ]
  },
  {
    role: "DevOps Engineer",
    company: "Tata Consultancy Services",
    where: "Bangalore",
    when: "May 2022 - Feb 2024",
    skills: ["Prometheus", "Kubernetes"],
    points: [
      "Delivered end-to-end infrastructure projects across AWS: three-tier applications, Kubernetes (EKS) platforms, serverless, and containerized workloads on ECS/Fargate.",
      "Implemented complete DevSecOps pipelines — Jenkins, SonarQube, Trivy, HashiCorp Vault, and ArgoCD — shifting security left."
    ]
  },
  {
    role: "Network Engineer",
    company: "Alackrity Consols",
    where: "Bengaluru, Karnataka, India",
    when: "May 2018 - May 2022",
    points: [
      "Automated Linux systems administration, orchestration (Ansible), and SSL/TLS lifecycle management.",
      "Enterprise network operations — CCNA-level TCP/IP, routing & switching — and Sophos firewall management."
    ]
  }
];

/* ------------------------------------------------------------
   5. PAGE FEED-IN — set document title, header, footer brand
   ------------------------------------------------------------ */
function feedPage() {
  // <title> name: suffix
  var t = document.title;
  if (t && t.indexOf(siteConfig.name) === -1) document.title = t + " — " + siteConfig.name;

  // brand in nav + footer
  document.querySelectorAll("[data-brand-name]").forEach(function (el) {
    el.textContent = siteConfig.name;
  });
}

/* ------------------------------------------------------------
   6. THEME TOGGLE (dark / light, remembers choice)
   ------------------------------------------------------------ */
function setupTheme() {
  var toggle = document.getElementById("themeToggle");
  if (!toggle) return;

  var apply = function (theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
  };

  // initial: stored choice, else OS preference
  var stored = null;
  try { stored = localStorage.getItem("theme"); } catch (e) {}
  apply(stored || (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"));

  toggle.addEventListener("click", function () {
    apply(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });
}

/* ------------------------------------------------------------
   7. MOBILE NAV TOGGLE
   ------------------------------------------------------------ */
function setupNav() {
  var btn = document.getElementById("navToggle");
  var menu = document.getElementById("navMenu");
  if (!btn || !menu) return;

  btn.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // close after choosing a link on mobile
  menu.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () { menu.classList.remove("open"); });
  });
}

/* ------------------------------------------------------------
   8. FOOTER YEAR
   ------------------------------------------------------------ */
function setupYear() {
  var el = document.getElementById("year");
  if (el) el.textContent = new Date().getFullYear();
}

/* ------------------------------------------------------------
   Init
   ------------------------------------------------------------ */
document.addEventListener("DOMContentLoaded", function () {
  renderSocials();
  feedPage();
  setupTheme();
  setupNav();
  setupYear();
});
