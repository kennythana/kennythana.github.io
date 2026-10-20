"""Refresh stats.json from a public Google Scholar profile.

Run by .github/workflows/update-citations.yml once a week.
If Scholar blocks the request or the page layout changes, the script
leaves stats.json untouched, so the site keeps showing the last good numbers.
"""
import datetime
import json
import os
import sys

import requests
from bs4 import BeautifulSoup

SCHOLAR_ID = os.environ.get("SCHOLAR_ID", "").strip()

# Words from each paper title -> key used in index.html (data-pub="...")
PAPERS = {
    "paper-waste": "using paper waste",
    "interior": "modern interior materials",
    "review": "a review delving",
    "sawdust": "utilizing sawdust",
    "egg": "egg packaging",
    "decorative": "decorative and design applications",
}


def main():
    if not SCHOLAR_ID:
        sys.exit("Set SCHOLAR_ID (the user=... part of your Scholar URL).")
    url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&cstart=0&pagesize=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        html = requests.get(url, headers=headers, timeout=30).text
    except requests.RequestException as e:
        print(f"Request failed, keeping old stats: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")
    cells = soup.select("#gsc_rsb_st td.gsc_rsb_std")
    if len(cells) < 3:
        print("Scholar did not return the profile table (probably a CAPTCHA). Keeping old stats.")
        return

    citations = int(cells[0].text)
    h_index = int(cells[2].text)

    papers = {}
    for row in soup.select("tr.gsc_a_tr"):
        title = row.select_one(".gsc_a_at").text.lower()
        cited_text = row.select_one(".gsc_a_ac").text.strip()
        cited = int(cited_text) if cited_text.isdigit() else 0
        for key, words in PAPERS.items():
            if words in title:
                # Scholar sometimes lists a duplicate entry; keep the larger count
                papers[key] = max(papers.get(key, 0), cited)

    path = os.path.join(os.path.dirname(__file__), "..", "stats.json")
    with open(path) as f:
        old = json.load(f)
    old_papers = old.get("papers", {})
    new = {
        "citations": citations,
        "h_index": h_index,
        "updated": datetime.date.today().strftime("%b %Y"),
        "papers": {**old_papers, **papers},
    }
    with open(path, "w") as f:
        json.dump(new, f, indent=2)
        f.write("\n")
    print(f"Updated: {citations} citations, h-index {h_index}")


if __name__ == "__main__":
    main()
