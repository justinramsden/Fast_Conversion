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
// speed: the engine part of a keystroke (budget for the whole keystroke is 10 ms)
const t0 = process.hrtime.bigint(); for (let i = 0; i < 2000; i++) top('1 3/8 in to mm');
const ms = Number(process.hrtime.bigint() - t0) / 1e6 / 2000; eq(`engine under 1 ms per keystroke (${ms.toFixed(3)} ms)`, ms < 1, true);
console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
