"""Builds privacy/<app>.html pages from privacy.html's header, footer and styles.

Run from the repo root: python3 scripts/app-privacy.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EFFECTIVE = 'October 2, 2026'
CONTACT = '<a href="mailto:contact@happyheartsoftware.com">contact@happyheartsoftware.com</a>'

COMMON_END = f'''
    <h2>Children</h2>
    <p>{{app}} isn't directed to children under 13, and we don't knowingly collect their personal information. If you believe a child has sent us information, contact us and we'll delete it.</p>

    <h2>Your choices and rights</h2>
    <p>You can ask us what personal information we hold about you, and ask us to correct or delete it. Email {CONTACT} and we'll help. Depending on where you live, you may have additional rights, and we'll honor them.</p>

    <h2>Changes to this policy</h2>
    <p>If we change this policy, we'll post the new version here and update the date at the top. If a change affects information we already hold, we'll tell you in the app before it takes effect.</p>

    <h2>Contact us</h2>
    <p>Questions about your privacy? Email {CONTACT}.</p>
'''

APPS = {
'daily-travel-log': dict(
  name='Daily Travel Log', url='https://travel.happyheartsoftware.com',
  summary="your home location and your trips are saved on your device. We don't run a server that receives them, and there are no accounts, ads or analytics. If you connect Google Sheets, the five log columns are copied to a spreadsheet in your own Google account.",
  body=f'''
    <h2>Who we are</h2>
    <p>Daily Travel Log (the website at travel.happyheartsoftware.com and the Android and iPhone apps) is made by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us"). This policy covers Daily Travel Log only.</p>

    <h2>What stays on your device</h2>
    <ul>
      <li><strong>Your home location</strong> (coordinates) and the home radius you choose.</li>
      <li><strong>Your trips:</strong> date, time you left, expected return, destination and return time.</li>
      <li><strong>Settings</strong>, such as your Google Sheets spreadsheet ID.</li>
    </ul>
    <p>This is kept in your browser's storage, or in the app's storage on your phone. We never receive it. If Android backup is turned on for your phone, Android may include the app's data in your Google backup.</p>

    <h2>How location is used</h2>
    <p>The app uses your location only to notice when you leave and return home. On the website, your position is checked while the app is open and is used only to work out your distance from home; it isn't saved. The Android and iPhone apps ask for "Allow all the time" location so they can record departures and returns while the app is closed. They do this by giving your home location to your phone's built-in geofencing service (Google Play services on Android, Apple Location Services on iPhone), which alerts the app when you cross the boundary. Your location is never sent to us, and isn't used for ads.</p>
    <p>Notifications are created on your phone. We don't send push notifications.</p>

    <h2>Google Sheets (optional)</h2>
    <p>If you choose to connect Google Sheets, you sign in with Google and allow the app to use Google Sheets. The app then creates or opens a spreadsheet in your Google Drive and copies the five log columns into it: Date, Time Leave, Expected Return, Destination and Return Time. Your home location is never sent to the sheet. The connection goes directly from your device to Google; the access Google grants is kept only in memory on the website, and isn't stored by us.</p>
    <p>Google's permission screen covers your spreadsheets in general, but the app only reads and changes its own Daily Travel Log sheet. Daily Travel Log's use of information received from Google APIs adheres to the <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" rel="noopener">Google API Services User Data Policy</a>, including the Limited Use requirements. You can remove the app's access at any time at <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener">myaccount.google.com/permissions</a>.</p>

    <h2>What we don't do</h2>
    <p>There are no accounts, ads, analytics, tracking or crash reporting, and the app doesn't set cookies. We don't sell your information or share it for advertising.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Cloudflare</strong> hosts the website and, like any web host, may keep basic request logs such as IP addresses for security.</li>
      <li><strong>Google</strong> provides sign-in and Google Sheets if you connect them, the fonts used in the app (your device requests them from Google Fonts, which receives your IP address), and geofencing on Android.</li>
      <li><strong>Apple</strong> provides geofencing on iPhone.</li>
      <li><strong>GitHub</strong> hosts the Android app download.</li>
    </ul>

    <h2>Deleting your data</h2>
    <ul>
      <li>Delete any trip from the Travel log. If Google Sheets is connected, its row is removed from the sheet too.</li>
      <li>Uninstalling the app, or clearing this site's data in your browser, removes everything stored on that device, including your home location.</li>
      <li>Your Google Sheet belongs to you; delete it in Google Drive whenever you like.</li>
    </ul>
    <p>Download CSV on the Travel log page exports your trips at any time.</p>
'''),

'fitness-and-gains': dict(
  name='Fitness & Gains', url='https://fitness.happyheartsoftware.com',
  summary="your profile, food diary, workouts and check-ins are saved only on your device. There are no accounts, ads or analytics. When you search for a food, the search words go to our server to look up nutrition facts, but they aren't linked to you.",
  body=f'''
    <h2>Who we are</h2>
    <p>Fitness &amp; Gains (the web app at fitness.happyheartsoftware.com and its Android app) is made by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us"). This policy covers Fitness &amp; Gains only.</p>

    <h2>What stays on your device</h2>
    <ul>
      <li><strong>Your profile:</strong> height, weight, age, sex (optional), goal weight, goals and accomplishments.</li>
      <li><strong>Your food diary</strong>, saved foods and custom foods.</li>
      <li><strong>Your workouts:</strong> lift log, weekly routine, favorites and completed workouts.</li>
      <li><strong>Wellness check-ins</strong> (energy, sleep, stress) and your yoga routine and settings.</li>
    </ul>
    <p>This is kept in your browser's storage. We never receive it. The Android app opens Fitness &amp; Gains in Chrome, so its data is kept in Chrome's storage for the site.</p>

    <h2>What leaves your device</h2>
    <p><strong>Food searches.</strong> When you search for a food or restaurant, your search words are sent to our server, which looks up nutrition facts from the U.S. Department of Agriculture's FoodData Central and, for restaurant menus, from HealthyFastFood. We save the search words and results in a shared catalog so later searches are faster. They aren't linked to you, your device or your diary. Our host's request logs may record the search along with your IP address for a short time.</p>
    <p><strong>Feedback.</strong> If you send feedback, your message, the topic you pick and the email address you add (optional) are delivered to our inbox through Heartforms, our own form service, which keeps a copy so we can answer you. Please don't include medical records or other sensitive health information.</p>

    <h2>What we don't do</h2>
    <p>There are no accounts, ads, analytics or tracking, and the app doesn't set cookies. The Android app doesn't ask for any phone permissions. We don't sell your information or share it for advertising.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Cloudflare</strong> hosts the app and our food catalog, and keeps request logs, including IP addresses, for security and troubleshooting.</li>
      <li><strong>USDA FoodData Central</strong> and <strong>HealthyFastFood</strong> receive food search words and restaurant names from our server, never your personal details.</li>
      <li><strong>Heartforms</strong>, our own form service, receives feedback messages and keeps a copy until we delete it. It runs on <strong>Cloudflare</strong> and sends the email through <strong>Resend</strong>. Our inbox is hosted by <strong>Google Workspace</strong>.</li>
      <li><strong>Google Fonts</strong> supplies the app's typefaces and <strong>GitHub</strong> supplies exercise pictures. Your device requests these directly, so those services receive your IP address.</li>
    </ul>

    <h2>Deleting your data</h2>
    <ul>
      <li>Delete individual foods, diary entries and lifts in the app.</li>
      <li>"Clear this device" on the Profile page and "Clear data" on the Progress page each erase everything Fitness &amp; Gains has saved on this device, including your food diary, saved foods, lift log, routines and settings.</li>
      <li>You can also clear this site's data in your browser. On Android, open the app's storage settings and choose Manage space.</li>
    </ul>
    <p>You can download a full backup file from the Profile page at any time.</p>

    <h2>Health information</h2>
    <p>Fitness &amp; Gains offers general fitness and nutrition information, not medical advice. Talk with a doctor before starting a new diet or exercise program.</p>
'''),

'wellness-and-recovery': dict(
  name='Wellness & Recovery', url='https://recovery.happyheartsoftware.com',
  summary="everything you write in Wellness & Recovery, including your plans, check-ins, worksheets and recovery dates, is saved only on your device. There are no accounts, ads or analytics. Nothing you've saved is shared unless you choose to export it. The only exception is what you type into the optional AI Recovery Guide.",
  body=f'''
    <h2>Who we are</h2>
    <p>Wellness &amp; Recovery (the web app at recovery.happyheartsoftware.com and its Android app) is made by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us"). This policy covers Wellness &amp; Recovery only.</p>

    <h2>What stays on your device</h2>
    <ul>
      <li><strong>Your profile:</strong> name, recovery start date and goal, interests and area, and an optional emergency contact.</li>
      <li><strong>Your daily use:</strong> plans, check-ins (mood and energy), reflections, weekly reflections and pinned shortcuts.</li>
      <li><strong>Your recovery tools:</strong> worksheets such as ABC, cost-benefit and values, urge logs, DBT and SMART Recovery practice, meeting notes and debriefs, saved meetings, and your personal support plan, including a trusted person's name and phone number.</li>
      <li><strong>PDFs you add</strong> to the reader.</li>
    </ul>
    <p>This is kept in your browser's storage. We never receive it. The Android app opens Wellness &amp; Recovery in Chrome, so its data is kept in Chrome's storage for the site.</p>

    <h2>What leaves your device</h2>
    <p><strong>AI Recovery Guide (optional).</strong> The guide only runs after you tick the consent box. It sends the answers you type into it: what you'd like to change, difficult moments (up to 500 characters each), and the time and support options you pick. These go through our server and Vercel's AI Gateway to Google's Gemini model, which writes the draft. Your saved plans, worksheets, logs and history are never included, and we don't save your answers or the draft. If your answers suggest a crisis, the request isn't sent to the AI, and you're shown crisis resources instead.</p>
    <p>To prevent abuse, the guide is limited to a few requests a day per network. To count them, we keep a scrambled code made from your IP address. It can't be turned back into the address, and it's deleted automatically after about 24 hours.</p>
    <p><strong>Feedback.</strong> If you send feedback, your message, the topic, the name in your profile (if you've set one) and the email address you add (optional) are delivered to our inbox through Heartforms, our own form service, which keeps a copy so we can answer you.</p>
    <p><strong>Finding meetings.</strong> If you use your location to find nearby meetings, it's used only to open a Google Maps search. It isn't saved or sent to us.</p>

    <h2>What we don't do</h2>
    <p>There are no accounts, ads, analytics or tracking, and the app doesn't set cookies. The Android app doesn't ask for any phone permissions. We don't sell your information or share it for advertising.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Cloudflare</strong> and <strong>Vercel</strong> host the app and its AI feature, and keep request logs, including IP addresses, for security and troubleshooting.</li>
      <li><strong>Google (Gemini)</strong>, through <strong>Vercel AI Gateway</strong>, creates AI Recovery Guide drafts from the answers you choose to send.</li>
      <li><strong>Upstash</strong> stores the scrambled request counters described above.</li>
      <li><strong>Heartforms</strong>, our own form service, receives feedback messages and keeps a copy until we delete it. It runs on <strong>Cloudflare</strong> and sends the email through <strong>Resend</strong>. Our inbox is hosted by <strong>Google Workspace</strong>.</li>
      <li><strong>Google Fonts</strong> supplies the app's typefaces. Your device requests them directly, so Google receives your IP address.</li>
    </ul>

    <h2>Deleting your data</h2>
    <ul>
      <li>Settings, then Reset to Defaults, erases your saved app data from this device, and the app reloads itself and any other open tabs.</li>
      <li>PDFs you added to the reader are kept by Reset to Defaults. Delete them one at a time from the reader.</li>
      <li>To remove everything, clear this site's data in your browser. On Android, open the app's storage settings and choose Manage space.</li>
    </ul>
    <p>You can export a backup from Settings at any time. It doesn't include your PDFs.</p>

    <h2>Not a medical service</h2>
    <p>Wellness &amp; Recovery is a self-help companion. It doesn't diagnose or treat any condition and isn't a substitute for professional care. If you are in crisis in the U.S., call or text 988, or call 911 in an emergency.</p>
'''),

'oneira': dict(
  name='Oneira', url='https://oneira.happyheartsoftware.com', effective='October 2, 2026',
  summary="your dream journal, practice and progress are saved on your device. There are no ads, analytics or tracking. An account is optional: if you turn on backup, everything is encrypted on your device first, with a key made from your password, so we can't read your dreams.",
  body=f'''
    <h2>Who we are</h2>
    <p>Oneira (the web app at oneira.happyheartsoftware.com and its Android app) is made by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us"). This policy covers Oneira only.</p>

    <h2>What stays on your device</h2>
    <ul>
      <li><strong>Your dream journal:</strong> entries, titles, tags, moods, lucidity and vividness ratings, and unsaved drafts.</li>
      <li><strong>Your practice:</strong> reality checks, technique courses, Wake Back to Bed sessions, lessons read and dream signs.</li>
      <li><strong>Your profile and settings:</strong> goals, sleep schedule, chosen technique, reminder settings, milestones, theme and text size.</li>
    </ul>
    <p>This is kept in the app's storage on your phone, or in your browser's storage on the website. Without an account, we never receive it. If Android backup is turned on for your phone, Android may include the app's data in your Google backup.</p>
    <p>Dream signs are found on your device by counting words and tags across your entries. No AI service or server reads your journal.</p>

    <h2>Reminders and alarms</h2>
    <p>Reality check reminders, the morning journal prompt and the Wake Back to Bed alarm are scheduled on your phone. We don't send push notifications. On the website, reminders only appear while Oneira is open.</p>

    <h2>Optional account and encrypted backup</h2>
    <p>You can use Oneira fully without an account. If you create one, Oneira backs up your journal, practice and profile (not your theme, text size or drafts) and keeps your devices in step.</p>
    <ul>
      <li><strong>Encrypted on your device.</strong> Before anything leaves your device, it's encrypted with a key that only your password or your recovery key can unlock. Your password and recovery key never reach us.</li>
      <li><strong>What our server stores:</strong> your email address, a check value derived from your password (stored only after hashing it again), your encryption key locked by your password and by your recovery key, the encrypted records, and sign-in sessions. We can see how many records you have, their sizes and when they last changed, but not what they say.</li>
      <li><strong>Your email</strong> is used only to sign you in. We don't send you email or marketing.</li>
      <li><strong>Security:</strong> to protect accounts, our server counts failed sign-ins and briefly limits repeated attempts from the same IP address.</li>
    </ul>
    <p>Because we can't read your backup, we can't reset your password for you. If you lose both your password and your recovery key, your backup can't be opened by anyone, including us.</p>

    <h2>Contacting us</h2>
    <p>If you use the contact form, your message, the topic you pick, your email address and your name (optional) are delivered to our inbox through Heartforms, our own form service, which keeps a copy so we can answer you, along with the app version and whether you're using Android or the web. Please don't include dream details you want to keep private. The Email us button opens your own email app instead.</p>

    <h2>Updates to the Android app</h2>
    <p>While Oneira's Android app is installed from our website, it checks oneira.happyheartsoftware.com for a newer version when it opens. This sends nothing about you beyond the request itself.</p>

    <h2>What we don't do</h2>
    <p>There are no ads, analytics, tracking or crash reporting, and Oneira doesn't set cookies. We don't sell your information or share it for advertising. The Android app asks only for permission to show notifications.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Cloudflare</strong> hosts the website, the Android app download and our backup server and database, and keeps request logs, including IP addresses, for security.</li>
      <li><strong>Heartforms</strong>, our own form service, receives contact form messages and keeps a copy until we delete it. It runs on <strong>Cloudflare</strong> and sends the email through <strong>Resend</strong>. Our inbox is hosted by <strong>Google Workspace</strong>.</li>
    </ul>

    <h2>Deleting your data</h2>
    <ul>
      <li>Delete any dream from your journal. With backup on, the deletion reaches your other devices too.</li>
      <li>Settings, Account &amp; backup, Delete account and backup removes your account and everything backed up with it from our server straight away. Copies in our database's recovery history are gone within 30 days. Your journal stays on your device.</li>
      <li>Signing out stops backing up and leaves your journal on your device.</li>
      <li>Uninstalling the app, or clearing this site's data in your browser, removes everything Oneira stored on that device.</li>
    </ul>

    <h2>Health information</h2>
    <p>Oneira offers general information about sleep and lucid dreaming, not medical advice. If sleep problems, nightmares or anything else affects your health, talk with a doctor.</p>
'''),

'pubstar': dict(
  name='Pubstar', url='https://pubstar.happyheartsoftware.com',
  summary="Pubstar is a private portal where our studio and the creators we work with share the status of their published work. We collect the account and profile details you give us, use them only to run the studio, and never sell them or use them for ads.",
  body=f'''
    <h2>Who we are</h2>
    <p>Pubstar is made and run by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us", "the studio"). This policy covers Pubstar only.</p>

    <h2>What we collect</h2>
    <ul>
      <li><strong>Your account:</strong> your email address and password. Your password is handled by our sign-in provider, and we never see it.</li>
      <li><strong>Your profile:</strong> the details you choose to add, such as your full name, creator name, location, portfolio link and bio.</li>
      <li><strong>Creator and catalog records:</strong> details the studio keeps about you and your work, such as titles, status, sales channels and preview images or PDFs that the studio uploads.</li>
      <li><strong>Messages:</strong> when you use a contact or catalog-update form, your name, email and message are delivered to our inbox. Forms sent from the portal also include your account email, creator name and, for update requests, the title and status of that work.</li>
    </ul>

    <h2>Who can see it</h2>
    <p>Pubstar isn't public. You can see only your own profile, records and previews. Studio administrators can see all creator profiles, records and previews so they can manage the catalog. Preview files are kept in private storage and opened through links that expire after an hour.</p>

    <h2>How we use your information</h2>
    <ul>
      <li>To run your account and show you the status of your work.</li>
      <li>To market and distribute your work as agreed with you.</li>
      <li>To reply to your messages, and to send sign-up and password-reset emails.</li>
    </ul>
    <p>Pubstar doesn't use ads, analytics or tracking. We don't sell your information or share it for advertising.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Supabase</strong> provides sign-in, our database and file storage, and sends account emails. Your browser keeps your sign-in session in its local storage.</li>
      <li><strong>Vercel</strong> hosts Pubstar and may keep request logs, including IP addresses, for security.</li>
      <li><strong>Heartforms</strong>, our own form service, receives support and studio messages and keeps a copy until we delete it. It runs on <strong>Cloudflare</strong> and sends the email through <strong>Resend</strong>. Our inbox is hosted by <strong>Google Workspace</strong>.</li>
    </ul>

    <h2>How long we keep it</h2>
    <p>We keep your account, profile and records while you work with the studio, and for as long as we need them for business and legal records after that. Messages are kept in our email for as long as we need them to work with you.</p>

    <h2>Deleting your data</h2>
    <p>You can edit your profile in the portal at any time. To close your account, or to have your records and preview files deleted, email {CONTACT} and we'll do it for you.</p>
'''),

'quire': dict(
  name='Quire', url='https://quire.happyheartsoftware.com',
  summary="Quire is an invite-only tool that turns your manuscript into print-ready files. We keep your account details and your books so the service works. We don't use ads, analytics or tracking, and we never sell your information.",
  body=f'''
    <h2>Who we are</h2>
    <p>Quire, at quire.happyheartsoftware.com, is made and run by Happy Heart Software LLC, doing business as Happy Heart Software, based in Ohio, USA ("Happy Heart Software", "we", "us"). This policy covers Quire only.</p>

    <h2>What we collect</h2>
    <ul>
      <li><strong>Your account:</strong> your name, email address and profile picture (if you sign in with Google), plus your role, who manages your account, when your access ends, and when you last signed in.</li>
      <li><strong>Your books:</strong> manuscripts, chapters, images, covers, book details and settings, and the PDF and EPUB files Quire makes.</li>
      <li><strong>Earlier versions:</strong> the last 20 saved versions of each chapter, chapters you've removed, and a record of each build.</li>
      <li><strong>Change history:</strong> a record of account changes (such as invitations, role changes and removals), including who made them and the names and email addresses involved. We keep the most recent 1,000 entries.</li>
      <li><strong>Google Docs imports:</strong> if you import a Google Doc, you share it by link and our server downloads a copy.</li>
    </ul>

    <h2>Who can see it</h2>
    <p>Your library is private to you, and to people you share a library with. Administrators, and the manager of your account, can also open your library to help you and manage access.</p>

    <h2>How we use your information</h2>
    <p>Only to run Quire: to sign you in, store and build your books, manage access, and send reminder emails to administrators and managers when someone's access is about to end. Quire doesn't use ads, analytics or tracking, and its only cookies keep you signed in. We don't sell your information or share it for advertising.</p>

    <h2>Services involved</h2>
    <ul>
      <li><strong>Clerk</strong> handles sign-in (including Google sign-in), stores your account details and sends invitation emails.</li>
      <li><strong>Vercel</strong> hosts Quire, stores your books and our backups, and may keep request logs, including IP addresses, for security.</li>
      <li><strong>Resend</strong> sends reminder emails, which include the names, email addresses and access end dates of the people concerned.</li>
      <li><strong>Google</strong> provides Google sign-in, and the Google Docs you choose to import.</li>
    </ul>

    <h2>How long we keep it</h2>
    <ul>
      <li>Your books are kept until they're deleted. When you delete a book in Quire, it's moved to a trash folder rather than erased straight away, so it can be recovered if deleted by mistake. Books in the trash are permanently deleted after 30 days. Copies in our nightly backups disappear within 14 days after that.</li>
      <li>We make a backup of Quire every night and keep each one for 14 days.</li>
      <li>If your account is removed, your sign-in details are deleted, but your books are kept unless you ask us to delete them.</li>
    </ul>

    <h2>Deleting your data</h2>
    <p>To have your account, your books and everything in the trash permanently deleted, email {CONTACT}. We'll confirm when it's done. Copies in our nightly backups disappear within 14 days after that.</p>
    <p>You can download your finished PDF and EPUB files from Quire at any time.</p>
'''),
}

MAIN = '''  <main class="hh-legal">
    <span class="hh-kicker">{name}</span>
    <h1>{name} Privacy Policy</h1>
    <p class="hh-date">Effective {effective}</p>
    <div class="hh-summary"><strong>The short version:</strong> {summary}</div>
{body}{end}
    <a class="hh-back" href="/privacy/">&larr; All privacy policies</a>
  </main>'''

INDEX_BODY = '''
    <h2>Our apps</h2>
    <p>Each of our apps has its own privacy policy explaining exactly what it stores and where.</p>
    <ul>
{items}
    </ul>
    <h2>This website</h2>
    <p>For happyheartsoftware.com itself, see our <a href="/privacy.html">website privacy policy</a>.</p>

    <h2>Contact us</h2>
    <p>Questions about your privacy? Email {contact}.</p>
'''

# Apps whose policy lives on the app's own site.
EXTERNAL = [('BET', 'https://bet.happyheartsoftware.com/privacy')]


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
    for slug, app in APPS.items():
        esc = app['name'].replace('&', '&amp;')
        body = MAIN.format(name=esc, effective=app.get('effective', EFFECTIVE), summary=app['summary'].replace('&', '&amp;'),
                           body=app['body'], end=COMMON_END.format(app=esc))
        (out / f'{slug}.html').write_text(page(base, f'{esc} Privacy Policy', f'How {esc} handles your information.', body))
    links = sorted([(a['name'].replace('&', '&amp;'), f'/privacy/{s}') for s, a in APPS.items()] + EXTERNAL)
    items = '\n'.join(f'      <li><a href="{href}">{name}</a></li>' for name, href in links)
    index = MAIN.format(name='Privacy', effective=EFFECTIVE,
                        summary="we build small apps that keep as much of your information on your own device as possible. We don't sell your information, show ads or track you.",
                        body=INDEX_BODY.format(items=items, contact=CONTACT), end='')
    index = index.replace('<h1>Privacy Privacy Policy</h1>', '<h1>Privacy at Happy Heart Software</h1>').replace(
        '\n    <a class="hh-back" href="/privacy/">&larr; All privacy policies</a>', '\n    <a class="hh-back" href="/">&larr; Back to Happy Heart Software</a>')
    (out / 'index.html').write_text(page(base, 'Privacy', 'Privacy policies for Happy Heart Software apps.', index))


if __name__ == '__main__':
    main()
