"""Build 404.html from privacy.html's header and footer.

GitHub Pages serves 404.html for any address that doesn't exist, at any depth,
so every link on it must start with a slash. Run: python3 scripts/not-found.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAIN = '''  <main class="hh-legal" style="text-align: center; padding-top: 120px; padding-bottom: 80px">
    <span class="hh-kicker">Page not found</span>
    <h1>This step doesn't lead anywhere</h1>
    <p>The page you're looking for isn't here. It may have moved, or the address may have a typo.</p>
    <p style="margin-top: 36px"><a href="/" class="hh-shift" style="display: inline-block; padding: 16px 28px; border-radius: 999px; background-image: linear-gradient(90deg, #FF3CAC, #FF8A00, #FFD23F, #34D399, #22D3EE, #7C3AED, #FF3CAC); color: #150A2E; text-decoration: none; font-weight: 800">Back to Happy Heart Software</a></p>
    <p style="margin-top: 28px">Looking for an app? <a href="/#apps">See all our apps</a> or <a href="/#help">get help</a>.</p>
  </main>'''


def main():
    html = (ROOT / 'privacy.html').read_text()
    html = html.replace('href="privacy.html"', 'href="/privacy.html"').replace('href="terms.html"', 'href="/terms.html"')
    html = re.sub(r'<title>.*?</title>', '<title>Page not found | Happy Heart Software</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="This page doesn\'t exist.">\n<meta name="robots" content="noindex">', html, count=1)
    html, n = re.subn(r'  <main class="hh-legal">.*?</main>', lambda _: MAIN, html, count=1, flags=re.S)
    assert n == 1
    assert not re.search(r'(href|src)="(?!/|#|https?:|mailto:|data:)', html), 'relative link would break on nested 404s'
    (ROOT / '404.html').write_text(html)


if __name__ == '__main__':
    main()
