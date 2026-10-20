# Kenny's portfolio

Static site: `index.html` + `stats.json`. Hosted on GitHub Pages.

## Put it online (one time, ~10 minutes)
1. Make a GitHub account. Create a **public** repo named `<your-username>.github.io`.
2. Upload everything in this folder (keep the hidden `.github` folder; on a Mac press Cmd+Shift+. in Finder to see it).
   Easiest: GitHub Desktop, or `git push` from Terminal. The web uploader can skip hidden folders.
3. Repo → Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
4. Your site is live at `https://<your-username>.github.io` in a minute or two.

## Turn on automatic citation updates
1. Open your Google Scholar profile. Copy the ID after `user=` in the URL.
2. Repo → Settings → Secrets and variables → Actions → **Variables** tab → New variable:
   name `SCHOLAR_ID`, value = that ID.
3. Repo → Settings → Actions → General → Workflow permissions → "Read and write permissions".
4. Actions tab → "Update citations" → Run workflow, to test it once.
After that it runs every Monday. If Scholar ever blocks it, the site just keeps the last numbers.

## Add photos
Put images in an `img/` folder, then in `index.html` replace a placeholder like
`<span class="slot">Photo slot: ...</span>` with `<img src="img/fobs.jpg" alt="Macadamia-shell key fobs">`.
Export at ~2000 px wide, JPEG quality ~80, so pages load fast.

## Custom domain (optional, ~$12/year)
Buy e.g. `kennyt.com` (Cloudflare Registrar or Porkbun), then Settings → Pages → Custom domain,
and follow GitHub's DNS instructions.
