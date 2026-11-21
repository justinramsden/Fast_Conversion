import sys, asyncio, json
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8780/'
out = []
def check(n, c, g=''): out.append(('ok   ' if c else 'FAIL ') + n + ('' if c else f'  → {g!r}'))
KEY = {'/':'#pad [data-key="/"]', ' ':'#pad [data-key=" "]', "'":'#pad [data-key="\'"]', '"':'#pad [data-key=\'"\']'}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':375,'height':629}, screen={'width':375,'height':812}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA, permissions=['clipboard-read','clipboard-write'])
        pg = await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        cdp = await ctx.new_cdp_session(pg)
        await pg.goto(URL); await pg.wait_for_timeout(700)
        val = lambda: pg.evaluate("[...document.querySelectorAll('.qin')].find(e => !e.hidden).value")
        act = lambda: pg.evaluate("document.activeElement.id || document.activeElement.tagName")
        quad = lambda: pg.eval_on_selector_all('.quad button', "bs => bs.map(b => b.querySelector('.v').textContent + (b.querySelector('.u') ? ' ' + b.querySelector('.u').textContent : ''))")
        bandB = lambda: pg.evaluate("Math.round((document.getElementById('pad').getBoundingClientRect().top + scrollY) * 10) / 10")  # where the keypad starts on the page
        vis = lambda s: pg.eval_on_selector(s, "e => getComputedStyle(e).display !== 'none'")
        async def keys(t):
            for ch in t: await pg.tap(KEY.get(ch, f'#pad [data-key="{ch}"]'))
        tap = pg.tap

        # ── launch ──
        check('nothing is focused at launch (no phone keyboard can appear)', await act() == 'BODY', await act())
        check('keypad is showing', await vis('#pad'))
        check('number box is read-only with no system keyboard', await pg.eval_on_selector('#q', "e => e.readOnly && e.getAttribute('inputmode') === 'none'"))
        check('empty box: the space under the keypad says to scroll', 'Scroll down here' in await pg.inner_text('#also') and await pg.locator('#also .row').count() == 0)
        check('extra-key row is gone (its keys are in the keypad)', await pg.locator('#padkeys button').count() == 0)
        check('our caret shows', await pg.locator('#ghost u').count() == 1)
        order = await pg.eval_on_selector_all('#pad .pd button', "bs => bs.map(b => b.dataset.key || b.dataset.act).join('')")
        check('phone order: 123 / 456 / 789 / . 0 delete', order == '123456789.0bs', order)
        fkeys = await pg.eval_on_selector_all('#pad .pf button', "bs => bs.map(b => b.dataset.key || b.dataset.act).join('|')")
        check('extra keys block', fkeys == '/| |\'|"|neg|clear|kb', fkeys)
        fits = await pg.evaluate("document.getElementById('pad').getBoundingClientRect().bottom <= innerHeight")
        check('band + keypad fit the screen without scrolling', fits)
        b0 = await bandB()

        # ── typing ──
        await keys('25.4'); check('first tap types (no tap on the box)', await val() == '25.4', await val())
        check('answers follow', (await quad())[0] == '1 in', await quad())
        check('still nothing focused', await act() == 'BODY', await act())
        await tap('#pad [data-act="bs"]'); check('delete removes one', await val() == '25.', await val())
        await tap('#pad [data-act="clear"]'); check('C clears', await val() == '', await val())
        await keys('1 3/8'); check('fraction keys', await val() == '1 3/8' and (await quad())[0] == '1.375 in', [await val(), await quad()])
        await tap('#pad [data-act="clear"]'); await keys("5'7\""); check('feet and inches keys', await val() == "5'7\"" and (await quad())[0] == '1701.8 mm', [await val(), await quad()])
        await tap('#pad [data-act="clear"]'); await keys('40'); await tap('#pad [data-act="neg"]'); check('± toggles', await val() == '-40', await val())
        await tap('#pad [data-act="neg"]'); check('± toggles back', await val() == '40', await val())
        # hold delete
        await keys('5'); check('typed value: more answers replace the scroll note', await pg.locator('#also .row').count() > 0 and 'Scroll down' not in await pg.inner_text('#also'))
        await tap('#pad [data-act="clear"]'); await keys('123456789')
        box = await pg.locator('#pad [data-act="bs"]').bounding_box(); pt = [{'x': box['x'] + box['width']/2, 'y': box['y'] + box['height']/2}]
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pt}); await pg.wait_for_timeout(900)
        dn = await pg.eval_on_selector('#pad [data-act="bs"]', "e => e.classList.contains('dn')")
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); await pg.wait_for_timeout(120)
        v = await val(); check('holding delete repeats', 0 < len(v) <= 4 or v == '', v)
        check('a held key looks pressed', dn)
        check('and releases', not await pg.eval_on_selector('#pad [data-act="bs"]', "e => e.classList.contains('dn')"))
        v1 = await val(); await pg.wait_for_timeout(300); check('repeat stops on release', await val() == v1, [v1, await val()])

        # ── nothing above the keypad changes height ──
        hs = {}
        await tap('#pad [data-act="clear"]'); hs['empty'] = await bandB()
        await keys('123456789012'); hs['long number'] = await bandB()
        await tap('#pad [data-act="clear"]'); await keys('1/0'); hs['unreadable'] = await bandB()
        check('unreadable number explains itself in the answer area', 'as a number' in await pg.inner_text('.quad .msg'), await pg.inner_text('.quad'))
        await tap('#pad [data-act="clear"]'); await tap('[data-pin="C"]'); await keys('20'); hs['two answers'] = await bandB()
        check('two answers share the space', await quad() == ['68 °F', '293.15 K'], await quad())
        await tap('[data-pin="kcal"]') if await pg.locator('[data-pin="kcal"]').count() else None
        await tap('[data-pin="mm"]'); await tap('#pad [data-act="clear"]'); await keys('100')
        await tap('.quad button:nth-child(2)'); await pg.wait_for_timeout(120); hs['copied toast'] = await bandB()
        check('the keypad never moves: everything above it keeps its height', len(set(hs.values())) == 1 and list(hs.values())[0] == b0, [b0, hs])
        # ── after a copy ──
        check('copy works', await pg.evaluate('navigator.clipboard.readText()') == '3 15/16', await pg.evaluate('navigator.clipboard.readText()'))
        check('toast says so', 'Copied 3 15/16' in await pg.inner_text('#hint') and await vis('#hint'), await pg.inner_text('#hint'))
        check('copied tile keeps its flash', await pg.eval_on_selector('.quad button:nth-child(2)', "e => e.classList.contains('copied')"))
        check('value is highlighted for replacing', await pg.locator('#ghost i.all').count() == 1)
        await keys('7'); check('next digit replaces', await val() == '7', await val())
        # ── after picking a unit ──
        await keys('5'); await tap('[data-pin="in"]')
        check('unit pick keeps the number and highlights it', await val() == '75' and await pg.locator('#ghost i.all').count() == 1 and (await quad())[0] == '1905 mm', [await val(), await quad()])
        await tap('#pad [data-act="bs"]'); check('delete on a highlighted value fixes the last digit', await val() == '7', await val())
        await tap('[data-pin="ft"]'); await tap('#q'); await pg.wait_for_timeout(50)
        check('a tap on the box drops the highlight, opens nothing', await pg.locator('#ghost i.all').count() == 0 and await vis('#pad'), await act())
        await keys('2'); check('then typing adds on', await val() == '72', await val())
        await tap('[data-pin="mm"]'); await tap("#pad [data-key=\"'\"]"); check("a unit key onto a highlighted number adds to it", await val() == "72'", await val())

        # ── the phone's keyboard, and back ──
        await tap('#pad [data-act="clear"]'); await keys('10')
        kb0 = await pg.eval_on_selector('#pad [data-act="kb"]', "e => { const p = document.querySelector('#pad').getBoundingClientRect(); return [e.offsetLeft, e.offsetTop, e.offsetWidth, Math.round(p.x), Math.round(p.y + scrollY)]; }")
        await tap('#pad [data-act="kb"]'); await pg.wait_for_timeout(80)
        check('abc: letter box focused', await act() == 'qa', await act())
        check('abc: asks for the text keyboard', await pg.eval_on_selector('#qa', "e => e.inputMode === 'text' && !e.readOnly"))
        check('abc: value carried, digits hidden, extra keys stay', await val() == '10' and not await vis('#pad .pd') and await vis('#pad .pf') and await pg.locator('#pad .pf button').count() == 7 and await pg.locator('#padkeys button').count() == 0, [await val()])
        kb1 = await pg.eval_on_selector('#pad [data-act="kb"]', "e => { const p = document.querySelector('#pad').getBoundingClientRect(); return [e.offsetLeft, e.offsetTop, e.offsetWidth, Math.round(p.x), Math.round(p.y + scrollY)]; }")
        check('123 key sits exactly where abc was', kb1 == kb0, [kb0, kb1])
        check('abc: row offers 123', (await pg.inner_text('#pad [data-act="kb"]')).split() == ['123', 'keypad'])
        await pg.keyboard.type(' psi'); check('letters convert', (await quad())[0] == '0.689476 bar', await quad())
        await tap('#pad [data-key="/"]'); check('extra row still types at the caret', await val() == '10 psi/', await val())
        await pg.keyboard.press('Backspace')
        await tap('#pad [data-act="kb"]'); await pg.wait_for_timeout(80)
        check('123: keypad back, value kept, focus released', await vis('#pad .pd') and (await pg.inner_text('#pad [data-act="kb"]')).split() == ['abc', 'keyboard'] and await val() == '10 psi' and await act() == 'BODY', [await val(), await act()])
        await tap('#pad [data-act="bs"]'); check('keypad edits the carried value', await val() == '10 ps', await val())
        await tap('#pad [data-act="kb"]'); await pg.wait_for_timeout(80)
        await pg.evaluate("document.activeElement.blur()"); await pg.wait_for_timeout(260)
        check('putting the phone keyboard away brings the keypad back', await vis('#pad .pd') and await act() == 'BODY', await act())
        # chips while in phone-keyboard mode keep it there
        await tap('#pad [data-act="clear"]'); await keys('10'); await tap('#pad [data-act="kb"]'); await pg.keyboard.type(' mi')
        await tap('#suggest [data-sug="thou"]'); await pg.wait_for_timeout(250)
        check('chip tap keeps the phone keyboard', await act() == 'qa' and await val() == '10 thou', [await act(), await val()])
        await tap('#pad [data-act="kb"]')

        # ── a real keyboard attached to a touch device ──
        await tap('#pad [data-act="clear"]'); await pg.keyboard.type('3.5mm'); await pg.keyboard.press('Backspace')
        check('hardware keys type through the keypad', await val() == '3.5m', await val())
        await pg.keyboard.press('Escape'); check('Esc clears', await val() == '', await val())

        # ── settings ──
        await pg.evaluate("document.querySelector('[data-set=\"keypad_order = calculator\"]').scrollIntoView()")
        await pg.click('[data-set="keypad_order = calculator"]'); await pg.wait_for_timeout(60)
        order = await pg.eval_on_selector_all('#pad .pd button', "bs => bs.map(b => b.dataset.key || b.dataset.act).join('')")
        check('calculator order: 789 on top', order == '789456123.0bs', order)
        check('quick button shows as chosen', await pg.eval_on_selector('[data-set="keypad_order = calculator"]', "e => e.classList.contains('on')") and not await pg.eval_on_selector('[data-set="keypad_order = phone"]', "e => e.classList.contains('on')"))
        check('settings box shows it', 'keypad_order = calculator' in await pg.eval_on_selector('#setText', 'e => e.value'))
        await pg.click('[data-set="keypad_style = tile"]'); await pg.wait_for_timeout(300)
        bg = await pg.eval_on_selector('#pad .d', "e => getComputedStyle(e).backgroundColor")
        check('tile style loads from styles.css and applies', await pg.evaluate("document.documentElement.dataset.pad") == 'tile' and await pg.locator('#looks').count() == 1 and bg == 'rgba(255, 255, 255, 0.36)', bg)
        await pg.evaluate("t => navigator.clipboard.writeText(t)", 'keypad_colors = #10261a #1f4a33 #eafff2 #17382a #9be2b8\nkeypad_style = pill')
        await pg.click('#aiPaste'); await pg.wait_for_timeout(100)
        bg = await pg.eval_on_selector('#pad .d', "e => getComputedStyle(e).backgroundColor")
        check('own colours from pasted settings', bg == 'rgb(31, 74, 51)', [bg, await pg.inner_text('#setMsg')])
        await pg.evaluate("t => navigator.clipboard.writeText(t)", 'keypad_colors = default\nkeys = / space C')
        await pg.click('#aiPaste'); await pg.wait_for_timeout(100)
        fkeys = await pg.eval_on_selector_all('#pad .pf button', "bs => bs.map(b => b.dataset.key || b.dataset.act).join('|')")
        check('keys setting fills the extra block, abc always kept', fkeys == '/| |clear|kb', fkeys)
        await pg.reload(); await pg.wait_for_timeout(600)
        order = await pg.eval_on_selector_all('#pad .pd button', "bs => bs.map(b => b.dataset.key || b.dataset.act).join('')")
        check('keypad settings remembered after reload', order == '789456123.0bs' and await vis('#pad'), order)
        # keypad off: the phone's own number pad, as before
        await pg.evaluate("document.querySelector('[data-set=\"keypad = off\"]').scrollIntoView()")
        await pg.click('[data-set="keypad = off"]'); await pg.wait_for_timeout(80)
        check('keypad off: hidden, box editable with the decimal pad, extra row shown', not await vis('#pad') and await pg.eval_on_selector('#q', "e => !e.readOnly && e.getAttribute('inputmode') === 'decimal'") and await pg.locator('#padkeys button').count() == 3)
        await pg.evaluate("scrollTo(0,0)"); await tap('#q'); await pg.keyboard.type('12'); check('keypad off: typing in the box works', await val() == '12' and await act() == 'q', [await val(), await act()])
        await pg.evaluate("document.querySelector('[data-set=\"keypad = on\"]').scrollIntoView()")
        await pg.click('[data-set="keypad = on"]'); await pg.wait_for_timeout(80)
        check('keypad back on', await vis('#pad') and await pg.eval_on_selector('#q', "e => e.readOnly"))
        check('no page errors (phone)', not errs, errs)

        # ── a computer: no keypad, nothing changed ──
        d = await (await b.new_context(viewport={'width':1200,'height':800})).new_page(); derr=[]; d.on('pageerror', lambda e: derr.append(str(e)))
        await d.goto(URL); await d.wait_for_timeout(500)
        check('desktop: no keypad, box focused and editable', await d.eval_on_selector('#pad', "e => getComputedStyle(e).display") == 'none' and await d.evaluate("document.activeElement.id") == 'q' and not await d.eval_on_selector('#q', 'e => e.readOnly'))
        await d.keyboard.type('25.4mm'); check('desktop: typing converts', await d.eval_on_selector('.quad button .v', 'e => e.textContent') == '1', await d.inner_text('.quad'))
        check('desktop: keypad settings rows hidden', not await d.is_visible('[data-set="keypad = on"]'))
        await d.keyboard.type(' zz'); check('desktop: unknown unit message', 'No unit matches' in await d.inner_text('.quad .msg'), await d.inner_text('.quad'))
        s = await d.evaluate("(() => { const c = getComputedStyle(document.getElementById('hint')); return [c.marginTop, c.fontSize, c.fontWeight]; })()")
        check('desktop: hint line style restored', s == ['0px', '15px', '500'], s)
        check('no page errors (desktop)', not derr, derr)
        print('\n'.join(out)); print(f"{sum(o.startswith('ok') for o in out)}/{len(out)} keypad checks passed")
        await b.close()
asyncio.run(main())
