"""Builds the privacy index (privacy/index.html) and the privacy/<app>.html pages that send old links
on to each app's own policy, inside privacy.html's header, footer and styles.

Each app's full policy lives in that app's repo and is served by the app. Edit it there.

Run from the repo root: python3 scripts/app-privacy.py
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EFFECTIVE = 'October 2, 2026'
CONTACT = '<a href="mailto:contact@happyheartsoftware.com">contact@happyheartsoftware.com</a>'

# Every app's policy, as (name, URL served by the app).
APPS = [
    ('BET', 'https://bet.happyheartsoftware.com/privacy'),
    ('Daily Travel Log', 'https://travel.happyheartsoftware.com/privacy'),
    ('Fitness & Gains', 'https://fitness.happyheartsoftware.com/privacy'),
    ('Heartforms', 'https://forms.happyheartsoftware.com/privacy'),
    ('Mnemora', 'https://mnemora.happyheartsoftware.com/privacy/policy'),
    ('Multiflora', 'https://multiflora.app/privacy.html'),
    ('Oneira', 'https://oneira.happyheartsoftware.com/privacy'),
    ('Pubstar', 'https://pubstar.happyheartsoftware.com/privacy'),
    ('Quire', 'https://quire.happyheartsoftware.com/privacy'),
    ('Wellness & Recovery', 'https://recovery.happyheartsoftware.com/privacy'),
]

# Policies that used to be served here, at /privacy/<slug>. Their pages now redirect, since app
# stores, Google sign-in screens and older app versions may still link to them.
MOVED = {
    'daily-travel-log': 'Daily Travel Log',
    'fitness-and-gains': 'Fitness & Gains',
    'heartforms': 'Heartforms',
    'mnemora': 'Mnemora',
    'oneira': 'Oneira',
    'pubstar': 'Pubstar',
    'quire': 'Quire',
    'wellness-and-recovery': 'Wellness & Recovery',
}

INDEX = '''  <main class="hh-legal">
    <span class="hh-kicker">Privacy</span>
    <h1>Privacy at Happy Heart Software</h1>
    <p class="hh-date">Effective {effective}</p>
    <div class="hh-summary"><strong>The short version:</strong> we build small apps that keep as much of your information on your own device as possible. We don't sell your information, show ads or track you.</div>

    <h2>Our apps</h2>
    <p>Each of our apps has its own privacy policy explaining exactly what it stores and where.</p>
    <ul>
{items}
    </ul>
    <h2>This website</h2>
    <p>For happyheartsoftware.com itself, see our <a href="/privacy.html">website privacy policy</a>.</p>

    <h2>Contact us</h2>
    <p>Questions about your privacy? Email {contact}.</p>

    <a class="hh-back" href="/">&larr; Back to Happy Heart Software</a>
  </main>'''

MOVED_MAIN = '''  <main class="hh-legal">
    <span class="hh-kicker">{name}</span>
    <h1>{name} Privacy Policy</h1>
    <p>The {name} privacy policy has moved to <a href="{url}">{url}</a>.</p>
    <a class="hh-back" href="/privacy/">&larr; All privacy policies</a>
  </main>'''


def shell():
    html = (ROOT / 'privacy.html').read_text()
    # Pages live one folder down, so the footer's relative links need a leading slash.
    html = html.replace('href="privacy.html"', 'href="/privacy.html"').replace('href="terms.html"', 'href="/terms.html"')
    return html


def page(shell_html, title, description, main):
    html = re.sub(r'<title>.*?</title>', f'<title>{title} | Happy Heart Software</title>', shell_html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', html, count=1)
    html, n = re.subn(r'  <main class="hh-legal">.*?</main>', lambda _: main, html, count=1, flags=re.S)
    assert n == 1
    return html


def main():
    base = shell()
    out = ROOT / 'privacy'
    out.mkdir(exist_ok=True)
    urls = dict(APPS)
    for slug, name in MOVED.items():
        esc, url = escape(name), escape(urls[name])
        html = page(base, f'{esc} Privacy Policy', f'The {esc} privacy policy has moved to {url}.', MOVED_MAIN.format(name=esc, url=url))
        html = html.replace('</title>', f'</title>\n<meta http-equiv="refresh" content="0; url={url}">\n'
                            f'<link rel="canonical" href="{url}">\n<meta name="robots" content="noindex">', 1)
        (out / f'{slug}.html').write_text(html)
    items = '\n'.join(f'      <li><a href="{escape(url)}">{escape(name)}</a></li>' for name, url in APPS)
    index = INDEX.format(effective=EFFECTIVE, items=items, contact=CONTACT)
    (out / 'index.html').write_text(page(base, 'Privacy', 'Privacy policies for Happy Heart Software apps.', index))


if __name__ == '__main__':
    main()
