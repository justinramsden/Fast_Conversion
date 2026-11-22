// Fast Conversion engine tests. Run: node tests.js   (no page load cost; never loaded by the browser)
const fs = require('fs'), path = require('path'), vm = require('vm');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const core = html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const UC = vm.runInNewContext(core + '\nUC;', { Math, Number, String, Map, Set, Object, JSON, RegExp, Array, parseFloat });
UC.configure(UC.settings.defaults());
const top = (t, n = 0, pin = 'mm') => {
  const p = UC.parse(t, pin); p.den = 64;
  const r = p.unit ? UC.rows(p)[n] : null;
  return { how: p.how, unit: p.unit && p.unit.id, value: p.value, ans: r ? (r.show + (r.unit ? ' ' + r.unit : '')) : null, all: p.unit ? UC.rows(p).map(x => x.show + (x.unit ? ' ' + x.unit : '')) : [] };
};
let pass = 0, fail = 0;
const eq = (name, got, want) => { if (got === want) pass++; else { fail++; console.log(`FAIL ${name}\n  got:  ${got}\n  want: ${want}`); } };
// [input, expected unit, expected first answer]
const CASES = [
  ['25.4mm', 'mm', '1 in'], ['1 3/8', 'in', '1.375 in'], [`5' 7"`, 'in', '1701.8 mm'], ['5ft 7in', 'in', '1701.8 mm'],
  ['72f', 'F', '22.2222 °C'], ['-40c', 'C', '-40 °F'], ['40psi>kpa', 'psi', '275.79 kPa'], ['3 lb 4 oz', 'lb', '1.47418 kg'],
  ['1 h 30 min', 'h', '90 min'], ['thou', 'thou', '0.0254 mm'], ['10nm', 'Nm', '7.37562 ft·lb'], ['1,5 in', 'in', '38.1 mm'],
  ['1,500 mm', 'mm', '59.0551 in'], ['25,4 mm', 'mm', '1 in'], ['12 mm to in', 'mm', '0.472441 in'], ['100 km/h', 'km/h', '62.1371 mph'],
  ['30 mpg', 'mpg', '7.84049 L/100km'], ['5ft2', 'ft2', '0.464515 m²'], ['2 cups', 'cup', '473.176 mL'], ['1/2 in to mm', 'in', '12.7 mm'],
  ['60 degrees', 'deg', '1.0472 rad'], ['-1/16', 'in', '-0.0625 in'], ['4 ft 13 in', 'in', '1549.4 mm'], ['.75', 'mm', '0.0295276 in'],
];
for (const [t, u, a] of CASES) { const r = top(t); eq(`${t} unit`, r.unit, u); eq(`${t} answer`, r.ans, a); }
eq('1/0 is not a number', top('1/0').how, 'badnum');
eq('1.5.2 is not a number', top('1.5.2').how, 'badnum');
eq('abc is unknown', top('abc').how, 'unknown');
eq('nm offers nanometres too', UC.parse('10nm', 'mm').cands.some(c => c.id === 'nm'), true);
eq('12 mm fraction row', top('12 mm', 1).ans, '15/32 in');
eq('no alias clashes', UC.clashes.length, 0);
// Known bugs from the 2026-11-20 review: these fail until fixed
eq('ft-in drops a zero whole inch', top('5m 20cm').all.find(s => s.includes('′')), '17′ 3/4″');
eq('0 mpg gives no fake 0 answer', top('0 mpg').ans === '0 mpg (imp)', false);
eq('1e3 mm reads as 1000 mm', top('1e3 mm').value, 1000);
// keypad settings
const S0 = UC.settings.defaults();
eq('keypad defaults', [S0.keypad, S0.keypad_order, S0.keypad_style, S0.keypad_colors.length].join(), 'on,phone,flat,0');
let ks = UC.settings.parse('keypad_order = calculator\nkeypad_style = tile\nkeypad = off\nkeypad_colors = #102030 #405060 #fff #000000 #ABCDEF', S0);
eq('keypad settings are read', [ks.s.keypad, ks.s.keypad_order, ks.s.keypad_style, ks.s.keypad_colors.join(' '), ks.errors.length].join('|'), 'off|calculator|tile|#102030 #405060 #fff #000000 #abcdef|0');
eq('settings survive a round trip', UC.settings.text(UC.settings.parse(UC.settings.text(ks.s), S0).s), UC.settings.text(ks.s));
eq('defaults survive a round trip', UC.settings.text(UC.settings.parse(UC.settings.text(S0), S0).s), UC.settings.text(S0));
ks = UC.settings.parse('keypad_style = neon\nkeypad_order = sideways\nkeypad_colors = red blue', S0);
eq('a retired keypad look falls back to the default', UC.settings.parse('keypad_style = blueprint', S0).s.keypad_style + UC.settings.parse('keypad_style = blueprint', S0).errors.length, 'flat0');
eq('key hints: on by default, can be turned off, bad value reported', [S0.key_hints, UC.settings.parse('key_hints = off', S0).s.key_hints, UC.settings.parse('key_hints = maybe', S0).errors.length, /^key_hints = on$/m.test(UC.settings.text(S0))].join(), 'on,off,1,true');
eq('bad keypad values are reported and left alone', [ks.errors.length, ks.s.keypad_style, ks.s.keypad_order, ks.s.keypad_colors.length].join(), '3,flat,phone,0');
eq('every keypad style is offered to the AI guide', UC.settings.styles.every(k => UC.settings.guide('').includes('`' + k + '`')), true);
const yr = UC.rows(UC.parse('1 yr')).map(r => r.unit + '=' + r.show).join(' ');
eq('a year converts to days, weeks and hours', yr, 'd=365.25 wk=52.1786 h=8766');
eq('"2 years" and "2 yrs" read as years', [UC.parse('2 years').unit.id, UC.parse('2 yrs').unit.id].join(), 'yr,yr');
eq('"3 y" still guesses yards, as before', UC.parse('3 y').unit.id, 'yd');
eq('"3 ye" guesses years', UC.parse('3 ye').unit.id, 'yr');

// spoken measurements (phone dictation) read the same as typed ones
const said = t => { const p = UC.parse(t); return p.unit ? p.value + ' ' + p.unit.id : '?'; };
eq("spoken: 3/4 of an inch", said("3/4 of an inch"), "0.75 in");
eq("spoken: half an inch", said("half an inch"), "0.5 in");
eq("spoken: a half inch", said("a half inch"), "0.5 in");
eq("spoken: an inch and a half", said("an inch and a half"), "1.5 in");
eq("spoken: one and a half inches", said("one and a half inches"), "1.5 in");
eq("spoken: 1 and 1/2 inches", said("1 and 1/2 inches"), "1.5 in");
eq("spoken: 2 and 3/4 inches", said("2 and 3/4 inches"), "2.75 in");
eq("spoken: three and three quarters inches", said("three and three quarters inches"), "3.75 in");
eq("spoken: five feet six inches", said("five feet six inches"), "66 in");
eq("spoken: 5 feet and 6 inches", said("5 feet and 6 inches"), "66 in");
eq("spoken: 6 foot 2 and a half", said("6 foot 2 and a half"), "74.5 in");
eq("spoken: a quarter of an inch", said("a quarter of an inch"), "0.25 in");
eq("spoken: three eighths of an inch", said("three eighths of an inch"), "0.375 in");
eq("spoken: 3/8ths of an inch", said("3/8ths of an inch"), "0.375 in");
eq("spoken: 7 thirty seconds of an inch", said("7 thirty seconds of an inch"), "0.21875 in");
eq("spoken: three sixty-fourths of an inch", said("three sixty-fourths of an inch"), "0.046875 in");
eq("spoken: two point five millimeters", said("two point five millimeters"), "2.5 mm");
eq("spoken: point 5 inches", said("point 5 inches"), "0.5 in");
eq("spoken: twenty-five millimeters", said("twenty-five millimeters"), "25 mm");
eq("spoken: a hundred feet", said("a hundred feet"), "100 ft");
eq("spoken: two hundred and fifty grams", said("two hundred and fifty grams"), "250 g");
eq("spoken: negative 40 Celsius", said("negative 40 Celsius"), "-40 C");
eq("spoken: 72 degrees Fahrenheit", said("72 degrees Fahrenheit"), "72 F");
eq("spoken: half a mile", said("half a mile"), "0.5 mi");
eq("spoken: a foot and a half", said("a foot and a half"), "1.5 ft");
eq("spoken: 10 thousandths", said("10 thousandths"), "10 thou");
eq("spoken: 60 miles an hour", said("60 miles an hour"), "60 mph");
eq("spoken: 100 km per hour", said("100 km per hour"), "100 km/h");
eq("spoken: an hour and a half", said("an hour and a half"), "1.5 h");
eq("spoken: thirty seconds", said("thirty seconds"), "30 s");
eq("spoken: how many feet in a mile", said("how many feet in a mile"), "1 mi");
eq("spoken: What's 3/4 inch in mm?", said("What's 3/4 inch in mm?"), "0.75 in");
eq("spoken: 5'6\"", said("5'6\""), "66 in");
eq("spoken: 3 in to mm", said("3 in to mm"), "3 in");
eq("spoken: 1/2", said("1/2"), "0.5 in");
eq('spoken: a target still works', UC.parse('how many feet in a mile').target.id, 'ft');
UC.configure(S0);
// speed: the engine part of a keystroke (budget for the whole keystroke is 10 ms)
const t0 = process.hrtime.bigint(); for (let i = 0; i < 2000; i++) top('1 3/8 in to mm');
const ms = Number(process.hrtime.bigint() - t0) / 1e6 / 2000; eq(`engine under 1 ms per keystroke (${ms.toFixed(3)} ms)`, ms < 1, true);
console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
