# Builds the claude.ai copy: the GitHub page minus the install/offline bits, with fonts from Google Fonts
# (a claude.ai artifact cannot serve the fonts/ folder). Usage: python3 tools/make_artifact.py [output folder]
# Publish the output folder's index.html and styles.css together.
import os, sys, shutil
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/fast_conversion_artifact'
os.makedirs(out, exist_ok=True)
s = open(os.path.join(repo, 'index.html'), encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
rep('''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Fast Conversion">
<meta name="theme-color" content="#f2c92e">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">''', '<meta name="viewport" content="width=device-width, initial-scale=1">')
rep('''.band { padding-top: env(safe-area-inset-top); }
body { padding-bottom: env(safe-area-inset-bottom); }
''', '')
rep("""  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => { /* works online without it */ });
""", '')
import re
s = re.sub(r'<link rel="preload" href="fonts/[^>]*>\n', '', s)
s = re.sub(r"/\* fonts ship with the app[^\n]*\n(@font-face[^\n]*\n)+", '', s)
s = s.replace('<title>', '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=B612+Mono:wght@400;700&family=Barlow+Semi+Condensed:wght@400;500;600&display=swap" rel="stylesheet">\n<title>''', 1)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(s)
shutil.copy(os.path.join(repo, 'styles.css'), out)
print('artifact copy written to', out)
