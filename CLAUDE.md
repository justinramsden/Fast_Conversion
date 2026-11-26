# Fast Conversion: notes for AI assistants working on this repo

## Load-time budget
Speed of opening is a feature. For every change, report the expected load-time cost before building it.

Current weight (gzipped, as GitHub Pages serves it):
- index.html: about 40 KB. On a slow 4G phone (1.6 Mbps) each 1 KB costs about 5 ms on the first visit.
- styles.css: under 1 KB. The extra keypad looks. The page asks for it only when a look other than the default is chosen; the offline copy keeps it either way.
- fonts/: 5 files, 71 KB (subset to Basic Latin plus the symbols the app uses; other characters fall back to a system font), loaded with font-display: swap, so text shows at once in a fallback font. Two are preloaded (42 KB).
- Reopening the installed app reads everything from the phone's offline copy (sw.js), so it opens in about 0.3 s with or without signal. New versions download in the background and apply on the next open.

Rules:
- No new requests to other servers (each costs a new connection: roughly 0.3 to 0.6 s on mobile).
- No libraries or frameworks; keep everything in index.html. The one exception is extra keypad looks, which go in styles.css so nobody pays for a look they don't use.
- Keep each keystroke's work under about 10 ms on a 4x-throttled CPU.
- Bump CACHE in sw.js when adding files the app needs offline, and add them to FILES.

## The built-in keypad
On touch screens the app types through its own keypad (`#pad`), so it is ready the moment it opens: iOS will not raise its keyboard without a tap. Keep these true:
- In keypad mode the number box is read-only with `inputmode="none"` and is never focused. The page draws its own caret and "next number replaces this" highlight in the overlay (`paintGhost`). Keys always type at the end.
- Keys act on `touchstart`. Only the `abc` key waits for `touchend`: that is a user gesture, the moment iOS lets the page focus the second box (`#qa`) and raise the phone's keyboard. Putting that keyboard away returns to the keypad. The extra keys are a row above the digits; with the phone's keyboard up only the digits hide, so `abc`/`123` never moves.
- Nothing above the keypad may change height while typing (fixed box height, fixed answer-tile rows, messages inside the tile area, "Copied" as a floating note). A key that moves under a finger is a bug.
- Every button shows a pressed state on touch-down (`.dn`). Hover styles live under `@media (hover: hover)`.
- A keypad look is a set of CSS variables on `.pad`. To add one: write its `[data-pad="name"] .pad { ... }` block in styles.css, then add the name to `PAD_STYLES` in index.html. The settings guide and the "Keypad look" buttons pick it up from there.
- Settings: `keypad`, `keypad_order`, `keypad_style`, `keypad_colors` (see CUSTOMIZE.md, which is generated from `UC.settings.guide`).
- Not yet confirmed on a real iPhone or Android phone (only in Chrome's phone emulation): `abc` raising the keyboard from a cold start, the return to the keypad on Done, dictation, and the fit above the fold.

## Answers by size
Each unit can have size ranges (`RANGES` in the engine, and `answers.<code> from|under <n>` lines in settings): once the typed value passes the size, that list leads and the unit's usual answers follow. The rule with the most extreme matching size wins. Feet-inches, inch fractions and pounds-ounces stop at 1000. Change defaults in `RANGES`; the AI guide lists them from there.

## Spoken input
`spoken()` in the engine rewrites dictated phrases before the parser reads them ("three quarters of an inch" → "3/4 inch", "five feet and six inches", "an hour and a half", "72 degrees fahrenheit", "how many feet in a mile"). Every rule needs a spoken word, so typed input passes through unchanged. The "spoken:" lines in tests.js list what it must read; add a line there for any new phrase.

## Tests
Run `node tests.js` after every change and report the result. All tests must pass before committing.
For anything that touches the page, also run `sh checks/run.sh`: it runs the engine tests, then the browser checks in `checks/` (Playwright driving Chrome as a touch phone and as a desktop) and the per-key timing. `pad.py` prints a pass count; the others print their findings and end with an empty error list. They are checks in an emulated phone, not proof on a real one.
After changing the page, rebuild the claude.ai copy with `python3 tools/make_artifact.py <folder>` and republish that folder's index.html and styles.css (the repo is the source).
Nothing in `checks/` or `tools/` is requested by the app, so they cost no load time. Keep them out of FILES in sw.js.
