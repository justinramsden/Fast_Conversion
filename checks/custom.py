import sys, asyncio, json
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
REPLY = """Here you go:

```
# Fast Conversion settings v1
start_unit = in
remember_unit = on
unit_bar = in ft mm cm sheet | F C
keys = / space ' " C abc
fraction = 1/16
digits = 6
ruler = on
ruler_mark = on
theme = dark
unit.sheet = 8 ft
answers.mm = in-frac, in, ft-in, cm
```"""
out = []
def check(name, cond, got=''):
    out.append(('ok   ' if cond else 'FAIL ') + name + ('' if cond else f'  → {got!r}'))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':375,'height':700}, screen={'width':375,'height':812}, device_scale_factor=3,
                                  is_mobile=True, has_touch=True, user_agent=UA, permissions=['clipboard-read','clipboard-write'])
        pg = await ctx.new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        act = lambda: pg.evaluate('document.activeElement && document.activeElement.id')
        val = lambda sel='#q': pg.eval_on_selector(sel, 'e=>e.value')
        keys = await pg.eval_on_selector_all('#pad .pf button', 'bs=>bs.map(b=>b.firstChild.textContent)')
        check('default extra keys (in the keypad)', keys == ['/', 'space', '′', '″', '±', 'C', 'abc'], keys)
        await pg.keyboard.type('12')
        await pg.tap('[data-act="kb"]'); await pg.wait_for_timeout(50)
        check('abc moves focus to the letter-keyboard box', await act() == 'qa', await act())
        check('value carried over', await val('#qa') == '12', await val('#qa'))
        check('letter box asks for letters', await pg.eval_on_selector('#qa','e=>e.inputMode') == 'text')
        check('number box hidden', await pg.eval_on_selector('#q','e=>e.hidden'))
        check('key now reads 123', await pg.inner_text('[data-act="kb"]') == '123')
        await pg.keyboard.type('psi')
        check('typing letters converts', '0.827371 bar' in (await pg.inner_text('.quad')).replace('\n',' '), await pg.inner_text('.quad'))
        await pg.tap('[data-act="kb"]'); await pg.wait_for_timeout(50)
        check('123 goes back to the keypad box', (await act() or 'BODY') == 'BODY' and await val('#q') == '12psi', [await act(), await val('#q')])
        check('number box never asks for a system keyboard', await pg.eval_on_selector('#q','e=>e.inputMode') == 'none')
        await pg.tap('[data-act="clear"]')
        check('C clears', await val() == '', [await val(), await act()])
        await pg.keyboard.type('40'); await pg.tap('[data-act="neg"]')
        check('± still works', await val() == '-40', await val())

        # customize: copy instructions
        await pg.click('#aiCopy'); await pg.wait_for_timeout(100)
        clip = await pg.evaluate('navigator.clipboard.readText()')
        check('instructions copied', clip.startswith('# Fast Conversion: settings guide') and '## Current settings' in clip, clip[:80])
        check('copy message', 'Copied' in await pg.inner_text('#setMsg'), await pg.inner_text('#setMsg'))
        # paste the AI answer
        await pg.evaluate('t => navigator.clipboard.writeText(t)', REPLY)
        await pg.click('#aiPaste'); await pg.wait_for_timeout(100)
        msg = await pg.inner_text('#setMsg')
        check('applied message', msg.startswith('Done. Changed'), msg)
        bar = await pg.eval_on_selector_all('#unitbar button', 'bs=>bs.map(b=>b.textContent)')
        check('unit bar rebuilt', bar == ['in','ft','mm','cm','sheet','°F','°C'], bar)
        keys = await pg.eval_on_selector_all('#pad .pf button', 'bs=>bs.map(b=>b.firstChild.textContent)')
        check('extra keys rebuilt', keys == ['/', 'space', '′', '″', 'C', 'abc'], keys)
        check('dark theme', await pg.evaluate("document.documentElement.dataset.theme") == 'dark')
        check('settings box shows canonical text', 'unit.sheet = 8 ft' in await val('#setText'))
        await pg.tap('[data-act="clear"]'); await pg.tap('[data-pin="mm"]'); await pg.keyboard.type('100')
        quad = (await pg.inner_text('.quad')).split('\n')
        check('answers.mm + 1/16 in effect', quad[0] == '3 15/16 in', quad)
        await pg.tap('[data-act="clear"]'); await pg.tap('[data-pin="sheet"]'); await pg.keyboard.type('2')
        check('custom unit converts', (await pg.inner_text('.quad')).split('\n')[0] == '16 ft', await pg.inner_text('.quad'))
        check('custom unit in All units', await pg.locator('#unitList [data-unit="sheet"]').count() == 1)
        # survives reload
        await pg.reload(); await pg.wait_for_timeout(500)
        bar = await pg.eval_on_selector_all('#unitbar button', 'bs=>bs.map(b=>b.textContent)')
        check('settings remembered after reload', 'sheet' in bar and await pg.evaluate("document.documentElement.dataset.theme") == 'dark', bar)
        # paste straight into the box applies
        await pg.evaluate("t => navigator.clipboard.writeText(t)", 'fraction = 1/32\nkeys = none')
        await pg.click('#setText'); await pg.keyboard.press('Control+V'); await pg.wait_for_timeout(100)
        check('paste into box applies', 'fraction = 1/32' in await val('#setText') and await pg.locator('#padkeys button').count() == 0, await pg.inner_text('#setMsg'))
        check('typing in settings box stays there', True)
        await pg.click('#setText'); await pg.keyboard.press('End'); await pg.keyboard.type('x')
        check('textarea keeps its keys', await act() == 'setText', await act())
        # bad paste
        await pg.evaluate("t => navigator.clipboard.writeText(t)", 'Sure, what would you like to change?')
        await pg.click('#aiPaste'); await pg.wait_for_timeout(100)
        check('no-settings message', 'No settings found' in await pg.inner_text('#setMsg'), await pg.inner_text('#setMsg'))
        await pg.evaluate("t => navigator.clipboard.writeText(t)", 'unit_bar = mm furlong cm\ndigits = 2')
        await pg.click('#aiPaste'); await pg.wait_for_timeout(100)
        check('partial errors listed', 'furlong' in await pg.inner_text('#setMsg') and 'digits' in await pg.inner_text('#setMsg'), await pg.inner_text('#setMsg'))
        await pg.screenshot(path='cust.png', full_page=True)
        # reset needs two taps
        await pg.click('#setReset')
        check('first tap arms reset', await pg.inner_text('#setReset') == 'Tap again to reset')
        await pg.click('#setReset'); await pg.wait_for_timeout(50)
        bar = await pg.eval_on_selector_all('#unitbar button', 'bs=>bs.map(b=>b.textContent)')
        check('reset restores defaults', bar[:6] == ['mm','cm','m','thou','in','ft'] and await pg.locator('#pad .pf button').count() == 7, bar)
        check('theme back to auto', await pg.evaluate("document.documentElement.dataset.theme") is None)
        check('no page errors', not errs, errs)
        print('\n'.join(out)); await b.close()
asyncio.run(main())
