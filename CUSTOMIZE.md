# Fast Conversion: settings guide for AI assistants

Fast Conversion is a one-page unit converter (https://justinramsden.github.io/Fast_Conversion/). You type a number, tap a unit, and read the answers.
Everything about how it is set up lives in one short settings block. The person pasting this wants you to change that block for them.

## How to answer
1. Read what the person asks for, then edit the settings block under "Current settings".
2. Reply with the whole settings block inside ONE code block, so they can copy it with one tap. Keep its first line: `# Fast Conversion settings v1`
3. Change only what they asked for. Copy every other line exactly as it is.
4. Use only the setting names, values and unit codes in this guide. The app ignores anything else and tells them what it skipped.
5. If part of the request is impossible with these settings, say so in one short sentence above the code block. Put nothing else outside the code block.
6. If they have not said what they want yet, ask them in one short question.

They copy your code block, tap "Paste AI answer" in the app, and the new setup applies at once and is remembered on that device.

## Current settings
(The defaults. In the app, "Copy AI instructions" puts the person's own settings here.)
```
# Fast Conversion settings v1
# How to edit: https://github.com/justinramsden/Fast_Conversion/blob/main/CUSTOMIZE.md
start_unit = mm
remember_unit = on
unit_bar = mm cm in ft | C F | km mi | kg lb | g oz | m yd | L gal | mL floz | km/h mph | bar psi | Nm ftlb | m2 ft2
keys = / space ' " ± C abc
fraction = 1/64
digits = 6
ruler = on
ruler_mark = on
theme = auto
```

## The settings
| Setting | What it does | Allowed values | Default |
|---|---|---|---|
| `start_unit` | The unit a bare number (one typed without a unit) is read as when the app opens | one unit code | `mm` |
| `remember_unit` | Read bare numbers as the last unit used instead of always `start_unit` | `on`, `off` | `on` |
| `unit_bar` | The row of unit buttons under the input box, left to right; one tap reads the number as that unit. On a phone about 4 fit before it scrolls sideways, so put the most used first. Pairs of matching metric and imperial units read well. | unit codes separated by spaces; `\|` separates groups, which get a thin divider between them | `mm cm in ft \| C F \| km mi \| kg lb \| g oz \| m yd \| L gal \| mL floz \| km/h mph \| bar psi \| Nm ftlb \| m2 ft2` |
| `keys` | Extra keys in a row above the phone's number pad, left to right (phones only). They add what the number pad lacks. | any of `/` (fractions), `space` (between whole number and fraction), `'` (feet), `"` (inches), `±` (negative), `C` (clear the box), `abc` (switch to the letter keyboard and back); at most 8; `none` for no row | `/ space ' " ± C abc` |
| `fraction` | Inch fractions round to the nearest | `1/16`, `1/32`, `1/64` | `1/64` |
| `digits` | Significant digits in decimal answers | whole number 3 to 10 | `6` |
| `ruler` | Real-size ruler along the top (cm) and bottom (inches) of the yellow band | `on`, `off` | `on` |
| `ruler_mark` | Shade the typed length on the ruler | `on`, `off` | `on` |
| `theme` | Colours of the page below the yellow band | `auto` (follow the device), `light`, `dark` | `auto` |
| `answers.<code>` | The answers shown for one unit, in order. On a phone the first 4 fill the big tiles; the rest are listed below them. Add one line per unit you change. | unit codes of the same kind as `<code>`, plus `in-frac` (inch fraction), `ft-in` (feet and inches) and `lb-oz` (pounds and ounces); separated by commas. `default` puts back the built-in list. | see "Default answers" |
| `answers.typed-fraction` | The answers shown when someone types a fraction of an inch, like `3/8` or `1 3/8` | length units and the extras above | `in, mm, cm, ft, ft-in, thou` |
| `unit.<code>` | Adds a unit of their own, defined as an amount of a built-in unit. It then works everywhere: typed after a number, in `unit_bar` and in `answers`. `remove` deletes it. | a number then a built-in unit code, e.g. `unit.sheet = 2440 mm`. The code is up to 12 letters, digits or _, starting with a letter, and must not be a built-in code. Not for temperatures. | none |

## Unit codes
Use these exact codes; they are case-sensitive (C is Celsius, c is not a code).
- Length: mm (millimetres), cm (centimetres), m (metres), km (kilometres), um (micrometres), in (inches), thou (thousandths of an inch), ft (feet), yd (yards), mi (miles)
- Temperature: C (degrees Celsius), F (degrees Fahrenheit), K (kelvin)
- Weight: mg (milligrams), g (grams), kg (kilograms), t (tonnes), oz (ounces), lb (pounds), ton (US short tons)
- Volume: mL (millilitres), L (litres), m3 (cubic metres), tsp (US teaspoons), tbsp (US tablespoons), floz (US fluid ounces), cup (US cups), pt (US pints), qt (US quarts), gal (US gallons), igal (imperial gallons), in3 (cubic inches), ft3 (cubic feet)
- Torque: Nm (newton-metres), kgcm (kilogram-force centimetres), ftlb (foot-pounds), inlb (inch-pounds), ozin (ounce-inches)
- Pressure: kPa (kilopascals), MPa (megapascals), bar (bar), psi (pounds per square inch), atm (atmospheres)
- Speed: mm/s (millimetres per second), mm/min (millimetres per minute), m/min (metres per minute), m/s (metres per second), km/h (kilometres per hour), in/min (inches per minute), ft/min (feet per minute), mph (miles per hour), kn (knots)
- Area: mm2 (square millimetres), cm2 (square centimetres), m2 (square metres), ha (hectares), in2 (square inches), ft2 (square feet), acre (acres)
- Power: W (watts), kW (kilowatts), hp (horsepower)
- Force: N (newtons), kgf (kilograms-force), lbf (pounds-force)
- Angle: deg (degrees), rad (radians)

## Default answers
What each unit shows when it has no `answers` line:
- mm: in, in-frac, ft, ft-in, cm, thou, m
- cm: in, in-frac, ft, ft-in, mm, m
- m: ft, ft-in, in, yd, cm, mm
- km: mi, m, ft, yd
- um: thou, mm, in
- in: mm, in-frac, cm, ft-in, ft, m, thou
- thou: mm, um, in
- ft: m, cm, mm, in, yd
- yd: m, ft, in, cm
- mi: km, m, ft, yd
- C: F, K
- F: C, K
- K: C, F
- mg: g, oz
- g: oz, lb, kg
- kg: lb, lb-oz, oz, g
- t: lb, ton, kg
- oz: g, kg, lb
- lb: kg, g, oz
- ton: t, kg, lb
- mL: floz, tsp, tbsp, cup, L
- L: gal, igal, qt, cup, floz, mL
- m3: ft3, L, gal
- tsp: mL, tbsp, floz
- tbsp: mL, tsp, floz, cup
- floz: mL, L, cup, tbsp
- cup: mL, L, floz, tbsp
- pt: L, mL, cup, qt
- qt: L, mL, gal
- gal: L, igal, qt
- igal: L, gal
- in3: mL, L, floz
- ft3: L, m3, gal
- Nm: ftlb, inlb, kgcm
- kgcm: Nm, ozin, inlb
- ftlb: Nm, inlb
- inlb: Nm, ftlb, kgcm
- ozin: kgcm, Nm, inlb
- kPa: psi, bar, atm
- MPa: psi, bar, kPa
- bar: psi, kPa, atm
- psi: bar, kPa, MPa
- atm: psi, bar, kPa
- mm/s: mm/min, in/min, m/min
- mm/min: in/min, mm/s, m/min
- m/min: ft/min, m/s, km/h
- m/s: km/h, mph, ft/min
- km/h: mph, m/s, kn
- in/min: mm/min, mm/s
- ft/min: m/min, m/s, mph
- mph: km/h, m/s, kn
- kn: km/h, mph, m/s
- mm2: in2, cm2
- cm2: in2, mm2
- m2: ft2, in2
- ha: acre, m2, ft2
- in2: cm2, mm2
- ft2: m2, in2
- acre: ha, m2, ft2
- W: hp, kW
- kW: hp, W
- hp: kW, W
- N: lbf, kgf
- kgf: N, lbf
- lbf: N, kgf
- deg: rad
- rad: deg
- typed-fraction: in, mm, cm, ft, ft-in, thou

## Examples
Request: "I do woodworking. Round fractions to 1/16 and show the fraction first when I type mm."
Lines to change: `fraction = 1/16` and add `answers.mm = in-frac, in, ft-in, cm`

Request: "Add sheets of plywood, 8 feet long, and put them on the button row after ft."
Lines to change: add `unit.sheet = 8 ft`, and put `sheet` after `ft` in `unit_bar`

Request: "I mostly cook. Temperatures and kitchen volumes first, start in °F."
Lines to change: `unit_bar = F C | mL cup tbsp tsp | g oz | kg lb | L gal` and `start_unit = F`

This app converts between units of the same kind only. It has no currency, no time zones, no cooking by weight from volume (that needs the food's density), and no setting other than those above.
