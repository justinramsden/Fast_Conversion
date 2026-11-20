# Fast Conversion: notes for AI assistants working on this repo

## Load-time budget
Speed of opening is a feature. For every change, report the expected load-time cost before building it.

Current weight (gzipped, as GitHub Pages serves it):
- index.html: about 33 KB. On a slow 4G phone (1.6 Mbps) each 1 KB costs about 5 ms on the first visit.
- fonts/: 5 files, 71 KB (subset to Basic Latin plus the symbols the app uses; other characters fall back to a system font), loaded with font-display: swap, so text shows at once in a fallback font. Two are preloaded (42 KB).
- Reopening the installed app reads everything from the phone's offline copy (sw.js), so it opens in about 0.3 s with or without signal. New versions download in the background and apply on the next open.

Rules:
- No new requests to other servers (each costs a new connection: roughly 0.3 to 0.6 s on mobile).
- No libraries or frameworks; keep everything in index.html.
- Keep each keystroke's work under about 10 ms on a 4x-throttled CPU.
- Bump CACHE in sw.js when adding files the app needs offline, and add them to FILES.

## Tests
Run `node tests.js` after every change and report the result. All tests must pass before committing.
After changing the page, rebuild the claude.ai copy from this repo and republish it (the repo is the source).
