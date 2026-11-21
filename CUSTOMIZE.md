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
unit_bar = mm cm m | thou in ft | C F | km mi | kg lb | g oz | L gal | mL floz | bar psi | Nm ftlb | m2 ft2
keys = / space ' " ± C abc
keypad = on
key_hints = on
keypad_order = phone
keypad_style = flat
keypad_colors = default
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
| `unit_bar` | The row of unit buttons under the input box, left to right; one tap reads the number as that unit. On a phone about 4 fit before it scrolls sideways, so put the most used first. Pairs of matching metric and imperial units read well. | unit codes separated by spaces; `\|` separates groups, which get a thin divider between them | `mm cm m \| thou in ft \| C F \| km mi \| kg lb \| g oz \| L gal \| mL floz \| bar psi \| Nm ftlb \| m2 ft2` |
| `keys` | The extra keys. On the built-in keypad they are a line above the digits, left to right (two lines when there are more than seven), and stay in the same place when the phone's keyboard is up. With the phone's own keyboard they are a row above it. | any of `/` (fractions), `space` (between whole number and fraction), `'` (feet), `"` (inches), `±` (negative), `C` (clear the box), `abc` (bring up the phone's keyboard for letters and dictation, and go back); at most 8; `none` for none (the keypad always keeps `abc`) | `/ space ' " ± C abc` |
| `keypad` | The app's own number keypad on phones and tablets. It is there the moment the app opens, with no tap on the box first. `off` uses the phone's keyboard instead. | `on`, `off` | `on` |
| `key_hints` | The small words under the extra keys on the keypad (fraction, ft, in, clear, keyboard). `off` leaves only the symbols | `on`, `off` | `on` |
| `keypad_order` | Which digits are on the keypad's top row | `phone` (1 2 3 on top), `calculator` (7 8 9 on top) | `phone` |
| `keypad_style` | The keypad's look | `flat` (plain grey keys, like a phone keyboard), `pill` (round dark number keys under a row of yellow extra keys, like a phone calculator), `tile` (pale keys on tape yellow, matching the answer tiles) | `flat` |
| `keypad_colors` | Their own keypad colours, used in place of the style's | `default`, or five hex colours in this order: keypad background, number keys, number text, extra keys, extra-key text. Example: `#10261a #1f4a33 #eafff2 #17382a #9be2b8` | `default` |
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
- Length: mm (millimetres), cm (centimetres), m (metres), km (kilometres), um (micrometres), nm (nanometres), in (inches), thou (thousandths of an inch), ft (feet), yd (yards), mi (miles)
- Temperature: C (degrees Celsius), F (degrees Fahrenheit), K (kelvin)
- Weight: mg (milligrams), g (grams), kg (kilograms), t (tonnes), oz (ounces), lb (pounds), st (stone), ton (US short tons)
- Volume: mL (millilitres), L (litres), m3 (cubic metres), tsp (US teaspoons), tbsp (US tablespoons), floz (US fluid ounces), cup (US cups), pt (US pints), qt (US quarts), gal (US gallons), igal (imperial gallons), in3 (cubic inches), ft3 (cubic feet)
- Torque: Nm (newton-metres), kgcm (kilogram-force centimetres), ftlb (foot-pounds), inlb (inch-pounds), ozin (ounce-inches)
- Pressure: kPa (kilopascals), MPa (megapascals), bar (bar), psi (pounds per square inch), atm (atmospheres), hPa (millibar), inHg (inches of mercury), mmHg (millimetres of mercury)
- Speed: mm/s (millimetres per second), mm/min (millimetres per minute), m/min (metres per minute), m/s (metres per second), km/h (kilometres per hour), in/min (inches per minute), ft/min (feet per minute), mph (miles per hour), kn (knots)
- Area: mm2 (square millimetres), cm2 (square centimetres), m2 (square metres), ha (hectares), in2 (square inches), ft2 (square feet), acre (acres)
- Power: W (watts), kW (kilowatts), hp (horsepower)
- Force: N (newtons), kgf (kilograms-force), lbf (pounds-force)
- Angle: deg (degrees), rad (radians), rev (revolutions)
- Time: ms (milliseconds), s (seconds), min (minutes), h (hours), d (days), wk (weeks)
- Energy: J (joules), kJ (kilojoules), Wh (watt-hours), kWh (kilowatt-hours), kcal (food calories), BTU (British thermal units)
- Fuel use: L/100km (litres per 100 km), mpg (miles per US gallon), mpgUK (miles per imperial gallon)

## Default answers
What each unit shows when it has no `answers` line:
- mm: in, in-frac, ft, ft-in, cm, thou, m, um
- cm: in, in-frac, ft, ft-in, mm, m
- m: ft, ft-in, in, yd, cm, mm
- km: mi, m, ft, yd
- um: thou, mm, in, nm
- nm: um, mm, thou
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
- st: kg, lb
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
- hPa: kPa, inHg, psi
- inHg: hPa, kPa, psi
- mmHg: kPa, psi, inHg
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
- deg: rad, rev
- rad: deg, rev
- rev: deg, rad
- ms: s, min
- s: min, ms, h
- min: h, s, d
- h: min, d, s
- d: h, min, wk
- wk: d, h
- J: Wh, kcal, BTU
- kJ: kcal, Wh, BTU
- Wh: J, kJ, kWh
- kWh: kJ, BTU, kcal
- kcal: kJ, Wh, BTU
- BTU: kJ, Wh, kcal
- L/100km: mpg, mpgUK
- mpg: L/100km, mpgUK
- mpgUK: L/100km, mpg
- typed-fraction: in, mm, cm, ft, ft-in, thou

## Examples
Request: "I do woodworking. Round fractions to 1/16 and show the fraction first when I type mm."
Lines to change: `fraction = 1/16` and add `answers.mm = in-frac, in, ft-in, cm`

Request: "Add sheets of plywood, 8 feet long, and put them on the button row after ft."
Lines to change: add `unit.sheet = 8 ft`, and put `sheet` after `ft` in `unit_bar`

Request: "7 8 9 on the top row, and the yellow keypad."
Lines to change: `keypad_order = calculator` and `keypad_style = tile`

Request: "I mostly cook. Temperatures and kitchen volumes first, start in °F."
Lines to change: `unit_bar = F C | mL cup tbsp tsp | g oz | kg lb | L gal` and `start_unit = F`

This app converts between units of the same kind only. It has no currency, no time zones, no cooking by weight from volume (that needs the food's density), and no setting other than those above.
