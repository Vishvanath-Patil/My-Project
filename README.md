# Vishvanath Patil — Career Portfolio

Personal career portfolio for **Vishvanath Patil** (Senior Cloud Engineer @ TerraPay, Bengaluru).
A pure static HTML/CSS/JS website — **no server, no build step, no dependencies**.

- 🔖 **Digital resume** — `resume.html` (print / "Save as PDF" friendly) + downloadable `assets/resume/Resume.pdf`
- 📦 **Digital products** — `products.html` (study kits, guides, learning resources)
- 📬 **Contact** — `contact.html` (mailto-based contact form, social links)
- 🌐 **Socials** — LinkedIn, GitHub, Instagram, YouTube (footer of every page)

---

## 1. Run locally on any Windows machine (no server)

Just **double-click `index.html`**. That's it. No Node, no Python, no install.
Every asset uses a relative path, so the site works straight from `file://`.

> Tip: if you ever want a nicer local preview, `python -m http.server` works too — but it is never required.

## 2. Deploy to GitHub Pages

**Method A — GitHub web UI (recommended for beginners):**
1. Create a **new public repository** on GitHub, e.g. `My-Project`. Do *not* tick "Add a README" (we already have one).
2. Push this folder there:

   ```bash
   git remote add origin https://github.com/Vishvanath-Patil/My-Project.git
   git push -u origin master
   ```
   (If you created the portfolio as the *project root*, run `git add . && git commit -m "Initial commit"` first.)

3. On GitHub: repo → **Settings → Pages** → under **Build and deployment**, select:
   - Source: **Deploy from a branch**
   - Branch: `master`, folder: `/ (root)` → **Save**
4. Wait ~1 minute. Your site is live at:

   **`https://Vishvanath-Patil.github.io/My-Project/`**

5. Want your own subdomain later? A `CNAME` file with your domain + DNS record turns it into `https://vishvanath.dev/`.

**Method B — GitHub CLI (`gh`):**
```bash
cd career-portfolio
git add . && git commit -m "Initial commit"
gh repo create My-Project --public --source=. --push
gh repo edit --enable-pages --source master  # or via web UI
```

---

## 3. Customize — the only file you *must* touch

**`assets/js/site.js`** — one `siteConfig` object drives the social icons, footer, and contact links:

| Field | Current value | Action |
|---|---|---|
| `name` | `Vishvanath Patil` | keep |
| `role` | `Senior Cloud Engineer` | edit if you like |
| `email` | `pvishva93@gmail.com` | set — used by contact form & resume |
| `linkedin` | `https://www.linkedin.com/in/vishvanath-patil/` | keep |
| `github` | `https://github.com/Vishvanath-Patil` | keep |
| `instagram` | `https://instagram.com/your-handle` | **replace with your handle** |
| `youtube` | `https://youtube.com/@your-channel` | **replace with your channel** |

Static text (about section, project cards, experience) lives directly in each `.html` file — find-and-replace by section.

### Resume
- The real resume PDF goes at **`assets/resume/Resume.pdf`** (the included file is a generated placeholder with the same content).
- No PDF handy? Open **`resume.html`** → click **Print / Save as PDF** — the page is styled for A4 printing and produces a clean PDF from any browser.

### Favicon & images
- `favicon.svg` is hand-drawn; replace if you want.
- Hero art and product thumbnails in `assets/img/` are inline SVGs — swap them for your own photos (`assets/img/profile.jpg`) and update the `<img>` tags if you wish.

---

## 4. Project structure

```
career-portfolio/
  index.html        Home — hero, about, skills, certs, experience, featured projects
  resume.html       Digital resume (print-optimized)
  products.html     Digital products / learning resources
  contact.html      Contact page
  404.html          Custom 404 (GitHub Pages)
  robots.txt, favicon.svg
  assets/
    css/style.css   Design system (light/dark, responsive, print)
    js/site.js      siteConfig + interactions
    img/            Hand-drawn SVG art (incl. og-cover for social sharing)
    resume/Resume.pdf
  tools/
    make_resume_pdf.py   Regenerates the placeholder Resume.pdf (stdlib-only)
```

## 5. Tech notes (for the curious)
- **Zero dependencies** — no fonts, icons, or JS from CDNs; everything is local so it works offline (`file://`) and on GitHub Pages identically.
- **Dark / light theme** — honors your OS setting (`prefers-color-scheme`), with a manual toggle saved in `localStorage`.
- **Accessible** — semantic landmarks, skip link, aria-labels on icon links.
