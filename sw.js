// Opens instantly from this phone's copy, with or without signal. A newer version, if there is one,
// downloads in the background and is used the next time the app opens.
const CACHE = 'convert-v3';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png',
  'fonts/b612-mono-latin-400-normal.woff2', 'fonts/b612-mono-latin-700-normal.woff2',
  'fonts/barlow-semi-condensed-latin-400-normal.woff2', 'fonts/barlow-semi-condensed-latin-500-normal.woff2',
  'fonts/barlow-semi-condensed-latin-600-normal.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k.startsWith('convert-')).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const page = e.request.mode === 'navigate';
  const key = page ? 'index.html' : e.request;
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(key, { ignoreSearch: page });
    const fresh = fetch(e.request).then(r => { if (r.ok) c.put(key, r.clone()); return r; });
    if (hit) { e.waitUntil(fresh.catch(() => {})); return hit; } // the stored copy now, the update for next time
    return fresh.catch(() => c.match('index.html'));
  }));
});
