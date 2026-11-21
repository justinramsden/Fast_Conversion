import sys, asyncio
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
out=[]
def check(n,c,g=''): out.append(('ok   ' if c else 'FAIL ')+n+('' if c else f'  → {g!r}'))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':375,'height':700}, screen={'width':375,'height':812}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=UA)
        pg = await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        vis = lambda sel: pg.eval_on_selector(sel, 'e=>getComputedStyle(e).display!=="none"')
        await pg.keyboard.type('10')
        check('unit bar shown for a bare number', await vis('#unitbar') and not await vis('#suggest'))
        await pg.tap('[data-act="kb"]'); await pg.keyboard.type(' mi')
        check('ghost completes the name', await pg.eval_on_selector('#ghost','e=>e.textContent') == '10 miles', await pg.inner_text('#ghost'))
        chips = await pg.eval_on_selector_all('#suggest button', 'bs=>bs.map(b=>b.textContent+(b.classList.contains("on")?"*":""))')
        check('suggestion chips replace the unit bar', await vis('#suggest') and not await vis('#unitbar') and chips[:3]==['mi*','mm','thou'], chips)
        await pg.screenshot(path='sug1.png', clip={'x':0,'y':0,'width':375,'height':300})
        await pg.tap('#suggest [data-sug="thou"]')
        check('tap swaps the unit', await pg.eval_on_selector('#qa','e=>e.value') == '10 thou', await pg.eval_on_selector('#qa','e=>e.value'))
        check('focus stays in the box', await pg.evaluate('document.activeElement.id') == 'qa')
        check('answers follow', (await pg.inner_text('.quad')).split('\n')[0] == '0.254 mm', await pg.inner_text('.quad'))
        await pg.keyboard.type('k')
        check('after a pick, a unit letter swaps just the unit', await pg.eval_on_selector('#qa','e=>e.value') == '10k', await pg.eval_on_selector('#qa','e=>e.value'))
        chips = await pg.eval_on_selector_all('#suggest button', 'bs=>bs.map(b=>b.textContent)')
        check('10 k: kelvin with km, kg one tap away', await pg.eval_on_selector('#ghost','e=>e.textContent') == '10kelvin' and chips[1:3]==['km','kg'], [await pg.inner_text('#ghost'), chips])
        await pg.tap('#suggest [data-sug="kg"]')
        check('10 kg', (await pg.inner_text('.quad')).split('\n')[0] == '22.0462 lb', await pg.inner_text('.quad'))
        await pg.tap('[data-act="clear"]'); await pg.keyboard.type('5')
        check('back to unit bar after clear', await vis('#unitbar') and not await vis('#suggest'))
        check('no page errors', not errs, errs)
        print('\n'.join(out)); await b.close()
asyncio.run(main())
