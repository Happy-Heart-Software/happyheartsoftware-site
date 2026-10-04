#!/usr/bin/env python3
"""Builds the app catalog at /apps/ (apps/index.html) from the APPS list below, inside the same
header and footer as privacy.html. Edit this file, not the HTML, then run:

    python3 scripts/apps-catalog.py

When an app is added or removed, also update the cards in index.html's #apps section, the
ICONS, APPS and GOALS lists in its script (the app's pixel illustration, first step and goal),
and the "apps" count in the About section."""
from html import escape
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent.parent

# Reuse the privacy pages' shell and page() helper, so the catalog matches the rest of the site.
_spec = importlib.util.spec_from_file_location('app_privacy', ROOT / 'scripts' / 'app-privacy.py')
_ap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ap)

# Areas, in the order they appear, with the same tag colors as the cards on the home page.
AREAS = [
    ('Money', '#E6F4EC', '#2F9E6E'),
    ('Create', '#FCEEDB', '#B45A0E'),
    ('Wellness', '#E5EFF8', '#2F76B8'),
    ('Learn', '#FFF4CC', '#8A6100'),
    ('Everyday', '#DDF4F1', '#0F766E'),
    ('Play', '#EFE8F8', '#7B4FC0'),
    ('Business', '#FDE7EF', '#B5306A'),
]

# status: 'live', 'soon' (temporarily offline) or 'early' (early access, ask us).
APPS = [
    dict(name='BET', tagline='Budget & Expense Tracker', area='Money', status='live',
         url='https://bet.happyheartsoftware.com', android='https://bet.happyheartsoftware.com/downloads/BET.apk',
         privacy='https://bet.happyheartsoftware.com/privacy', works='Web and Android',
         what='Track your spending in simple ledgers that live in your own Google Drive. Add expenses in seconds, attach receipts, import transactions, and share a ledger with someone you budget with.',
         who=['Households and couples who share a budget', 'Anyone who wants a budget spreadsheet without building one', 'People who want their money records in their own Google account, not someone else’s server']),
    dict(name='Quire', tagline='Book formatting', area='Create', status='live',
         url='https://quire.happyheartsoftware.com', privacy='https://quire.happyheartsoftware.com/privacy', works='Web (invite only)',
         what='Turn a finished manuscript into a print-ready 6×9 PDF and an EPUB e-book, with clean typography and no design skills needed.',
         who=['Independent authors self-publishing a book', 'Small presses preparing manuscripts for print', 'Writers who want a professional-looking book without layout software']),
    dict(name='Pubstar', tagline='Publishing for creators', area='Create', status='live',
         url='https://pubstar.happyheartsoftware.com', android='https://pubstar.happyheartsoftware.com/downloads/Pubstar.apk',
         privacy='https://pubstar.happyheartsoftware.com/privacy', works='Web and Android',
         what='A private portal where our publishing studio and its creators share where each published work is available, while the studio handles marketing and distribution.',
         who=['Writers, artists and makers who publish with the Pubstar studio', 'Creators who want one clear view of where their work is sold']),
    dict(name='Fitness & Gains', tagline='Food, training & wellness', area='Wellness', status='live',
         url='https://fitness.happyheartsoftware.com', android='https://fitness.happyheartsoftware.com/downloads/FitnessAndGains.apk',
         privacy='https://fitness.happyheartsoftware.com/privacy', works='Web and Android',
         what='Log food with real nutrition facts, find exercises and routines, track lifts and progress, and keep everyday wellness habits. Everything is saved on your own device.',
         who=['People starting or restarting a fitness routine', 'Anyone tracking food or lifts who doesn’t want an account', 'People who want a private, ad-free fitness log']),
    dict(name='Wellness & Recovery', tagline='Daily recovery companion', area='Wellness', status='live',
         url='https://recovery.happyheartsoftware.com', android='https://recovery.happyheartsoftware.com/downloads/WellnessAndRecovery.apk',
         privacy='https://recovery.happyheartsoftware.com/privacy', works='Web and Android',
         what='Daily planning, check-ins, CBT and SMART Recovery-style worksheets, coping tools and wellbeing activities, all saved privately on your device. An educational tool, not a replacement for professional care.',
         who=['People working to change harmful, compulsive or unwanted behaviors', 'Anyone building steadier daily routines and coping skills', 'Supporters who want to understand recovery tools']),
    dict(name='Oneira', tagline='Learn to lucid dream', area='Wellness', status='live',
         url='https://oneira.happyheartsoftware.com', android='https://oneira.happyheartsoftware.com/downloads/Oneira.apk',
         privacy='https://oneira.happyheartsoftware.com/privacy', works='Web and Android',
         what='Learn lucid dreaming step by step: short lessons and courses on proven techniques, a dream journal, dream signs, reality-check reminders, a wake-back-to-bed alarm and your progress over time. Optional backup is encrypted on your device first.',
         who=['Anyone curious about lucid dreaming', 'People who want to remember their dreams better', 'Dream journal keepers who want privacy by design']),
    dict(name='Mnemora', tagline='Study with flashcards', area='Learn', status='live',
         url='https://mnemora.happyheartsoftware.com', android='https://mnemora.happyheartsoftware.com/downloads/Mnemora.apk',
         privacy='https://mnemora.happyheartsoftware.com/privacy/policy', works='Web and Android',
         what='Step-by-step lessons that teach from zero, plus flashcards with spaced repetition that explain why each answer is right. Courses cover psychopharmacology, geometry and trigonometry, and coding, and you can make your own cards or import them from Quizlet or Anki. Everything stays on your device and works offline.',
         who=['Students preparing for exams', 'Lifelong learners picking up a new subject', 'Anyone who wants a private study app with no account']),
    dict(name='Daily Travel Log', tagline='Travel tracking', area='Everyday', status='live',
         url='https://travel.happyheartsoftware.com', android='https://travel.happyheartsoftware.com/downloads/DailyTravelLog.apk',
         privacy='https://travel.happyheartsoftware.com/privacy', works='Web and Android',
         what='A simple, readable log of your trips for your phone or computer, kept on your device. Export to CSV or copy it to your own Google Sheet.',
         who=['People who log trips or mileage for work, expenses or taxes', 'Travelers who want a simple record of where they’ve been']),
    dict(name='Multiflora', tagline='Word puzzles', area='Play', status='live',
         url='https://multiflora.app', privacy='https://multiflora.app/privacy.html', play='https://play.google.com/store/apps/details?id=app.multiflora.android', works='Web and Android (Google Play)',
         what='An app for playing Rows Garden crossword puzzles, the flower-shaped word puzzle with interlocking rows and blooms.',
         who=['Crossword and word-puzzle fans', 'Anyone who likes a daily brain workout']),
    dict(name='Heartforms', tagline='Forms for any website', area='Business', status='early',
         url='https://forms.happyheartsoftware.com', privacy='https://forms.happyheartsoftware.com/privacy', works='Web',
         what='Collect what people send through your website and app forms: contact, support, sign-ups, waitlists, RSVPs, surveys, quotes and job applications. Every message is saved and emailed to the right person, and you can build a form page in minutes without code.',
         who=['Small businesses and organizations with a website', 'Event organizers taking RSVPs and sign-ups', 'Developers who want a simple form backend']),
]

# Search engines read these to tell what kind of app each one is.
CATEGORY = {
    'Money': 'FinanceApplication',
    'Create': 'DesignApplication',
    'Wellness': 'HealthApplication',
    'Learn': 'EducationalApplication',
    'Everyday': 'TravelApplication',
    'Play': 'GameApplication',
    'Business': 'BusinessApplication',
}

SITE = 'https://happyheartsoftware.com'
TITLE = 'All our apps'
DESCRIPTION = ('Every Happy Heart Software app: budgeting, book formatting, publishing, fitness, '
               'wellness, dream journaling, flashcard study, travel logs, word puzzles and website forms. '
               'What each one does, who it helps and where it works.')


def head_tags():
    """Canonical link, link-preview tags and a schema.org list of the apps, for the catalog's <head>."""
    apps = []
    for i, app in enumerate(APPS, 1):
        item = {
            '@type': 'SoftwareApplication',
            'name': app['name'],
            'description': app['what'],
            'url': app['url'],
            'applicationCategory': CATEGORY[app['area']],
            'operatingSystem': 'Web, Android' if 'Android' in app['works'] else 'Web',
            'publisher': {'@type': 'Organization', 'name': 'Happy Heart Software', 'url': SITE + '/'},
        }
        if app.get('play'):
            item['installUrl'] = app['play']
        apps.append({'@type': 'ListItem', 'position': i, 'url': f'{SITE}/apps/#{slug(app)}', 'item': item})
    data = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Happy Heart Software apps', 'itemListElement': apps}
    ld = json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')
    d = escape(DESCRIPTION)
    return f'''<link rel="canonical" href="{SITE}/apps/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Happy Heart Software">
<meta property="og:title" content="{TITLE} | Happy Heart Software">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}/apps/">
<meta property="og:image" content="{SITE}/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Happy Heart Software: Small steps. Happy heart.">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{ld}
</script>'''


def slug(app):
    return app['name'].lower().replace(' & ', '-').replace(' ', '-')


STATUS = {
    'live': ('Live', '#B8F5C9', '#6EE08F'),
    'soon': ('Back soon', '#FFE2A8', '#FFC24D'),
    'early': ('Early access', '#D8CCFF', '#A88BFF'),
}

STYLE = '''<style>
.hh-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.hh-legal.hh-catalog{max-width:1180px}
.hh-cat-intro{max-width:760px;font-size:19px!important}
.hh-cat-jump{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0 8px;padding:0;list-style:none}
.hh-cat-jump a{display:inline-block;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,0.25);color:#fff;text-decoration:none;font-weight:700;font-size:15px}
.hh-cat-jump a:hover{background:rgba(255,255,255,0.08)}
.hh-cat-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:18px}
@media (max-width:860px){.hh-cat-grid{grid-template-columns:1fr}}
.hh-cat-card{padding:28px;border-radius:20px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.14);display:flex;flex-direction:column;gap:12px}
.hh-cat-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
.hh-cat-tag{padding:6px 12px;border-radius:999px;font-size:13px;font-weight:800}
.hh-cat-status{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700}
.hh-cat-status i{width:8px;height:8px;border-radius:999px;display:inline-block}
.hh-cat-card h3{margin:4px 0 0;font-family:Sora,'Plus Jakarta Sans',sans-serif;font-size:26px;line-height:1.15}
.hh-cat-card .hh-cat-tagline{margin:0;font-size:14px;font-weight:700;color:#C9C4DA}
.hh-cat-card .hh-cat-label{margin:6px 0 0;font-size:13px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:#B9A6FF}
.hh-cat-card p,.hh-cat-card li{font-size:16px!important;line-height:1.6!important}
.hh-cat-card ul{margin:0!important}
.hh-cat-works{font-size:14px!important;color:#C9C4DA!important;margin:4px 0 0!important}
.hh-cat-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:auto;padding-top:8px}
.hh-cat-actions a{padding:11px 18px;border-radius:999px;border:1px solid rgba(255,255,255,0.3);color:#fff;text-decoration:none;font-size:15px;font-weight:700}
.hh-cat-actions a.hh-cat-primary{background:#fff;color:#150A2E;border-color:#fff}
.hh-cat-actions a.hh-cat-soft{background:rgba(255,255,255,0.12);border-color:transparent}
.hh-cat-actions a.hh-cat-plain{border-color:transparent;text-decoration:underline;padding-left:6px;padding-right:6px}
</style>'''


def card(app):
    tag_bg, tag_fg = next((bg, fg) for a, bg, fg in AREAS if a == app['area'])
    label, text_color, dot = STATUS[app['status']]
    n = escape(app['name'])
    actions = []
    if app['status'] == 'soon':
        actions.append(f'<a class="hh-cat-soft" href="/#start">Ask about {n}</a>')
    else:
        actions.append(f'<a class="hh-cat-primary" href="{escape(app["url"])}" target="_blank" rel="noopener">{"Learn more" if app["status"] == "early" else "Open " + n} <span aria-hidden="true">↗</span><span class="hh-sr"> (opens in a new tab)</span></a>')
    if app['status'] == 'early':
        actions.append('<a class="hh-cat-soft" href="/#start">Ask for access</a>')
    if app.get('android'):
        actions.append(f'<a class="hh-cat-soft" href="{escape(app["android"])}" download>Android app <span aria-hidden="true">↓</span><span class="hh-sr"> (download the {n} app for Android)</span></a>')
    if app.get('play'):
        actions.append(f'<a class="hh-cat-soft" href="{escape(app["play"])}" target="_blank" rel="noopener">Google Play <span aria-hidden="true">↗</span><span class="hh-sr"> (get the {n} app for Android on Google Play, opens in a new tab)</span></a>')
    if app.get('privacy'):
        actions.append(f'<a class="hh-cat-plain" href="{escape(app["privacy"])}">Privacy</a>')
    who = '\n'.join(f'          <li>{escape(w)}</li>' for w in app['who'])
    return f'''      <article class="hh-cat-card" id="{escape(slug(app))}">
        <div class="hh-cat-top"><span class="hh-cat-tag" style="background:{tag_bg};color:{tag_fg}">{escape(app['area'])}</span><span class="hh-cat-status" style="color:{text_color}"><i aria-hidden="true" style="background:{dot}"></i>{label}</span></div>
        <h3>{n}</h3>
        <p class="hh-cat-tagline">{escape(app['tagline'])}</p>
        <p class="hh-cat-label">What it does</p>
        <p>{escape(app['what'])}</p>
        <p class="hh-cat-label">Who it’s for</p>
        <ul>
{who}
        </ul>
        <p class="hh-cat-works">Works on: {escape(app['works'])}</p>
        <div class="hh-cat-actions">{''.join(actions)}</div>
      </article>'''


def main():
    used = [a for a, _, _ in AREAS if any(app['area'] == a for app in APPS)]
    jump = '\n'.join(f'      <li><a href="#area-{a.lower()}">{a}</a></li>' for a in used)
    sections = []
    for area in used:
        cards = '\n'.join(card(app) for app in APPS if app['area'] == area)
        sections.append(f'''    <h2 id="area-{area.lower()}">{area}</h2>
    <div class="hh-cat-grid">
{cards}
    </div>''')
    body = f'''  <main class="hh-legal hh-catalog">
    {STYLE}
    <span class="hh-kicker">App catalog</span>
    <h1>All our apps</h1>
    <p class="hh-cat-intro">Small, focused apps for everyday life and work. Here’s what each one does and who it helps. Most keep your information on your own device, and none of them show ads.</p>
    <ul class="hh-cat-jump" aria-label="Jump to an area">
{jump}
    </ul>
{chr(10).join(sections)}
    <p style="margin-top:48px">Looking for something we don’t make yet? We also build <a href="/#services">custom software and websites</a>.</p>
    <a class="hh-back" href="/">&larr; Back to Happy Heart Software</a>
  </main>'''
    out = ROOT / 'apps'
    out.mkdir(exist_ok=True)
    html = _ap.page(_ap.shell(), TITLE, escape(DESCRIPTION), body)
    desc_tag = f'<meta name="description" content="{escape(DESCRIPTION)}">'
    assert html.count(desc_tag) == 1
    html = html.replace(desc_tag, desc_tag + '\n' + head_tags())
    (out / 'index.html').write_text(html)
    print(f'wrote apps/index.html with {len(APPS)} apps')


if __name__ == '__main__':
    main()
