import sys, asyncio, urllib.parse
from playwright.async_api import async_playwright
SET = "start_unit = in\nunit_bar = in ft mm | F C\nkeys = / space ' \" ± C abc\nfraction = 1/16\nunit.sheet = 8 ft"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        url = 'file://'+sys.argv[1]+'#s='+urllib.parse.quote(SET)
        ctx = await b.new_context(viewport={'width':375,'height':700}, is_mobile=True, has_touch=True, permissions=['clipboard-read','clipboard-write'])
        pg = await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url); await pg.wait_for_timeout(500)
        bar = await pg.eval_on_selector_all('#unitbar button','bs=>bs.map(b=>b.textContent)')
        print('fresh: applied', bar, '| hash cleared:', await pg.evaluate('location.hash')=='' , '| offer hidden:', await pg.evaluate("document.getElementById('offer').hidden"))
        # now has settings; open a different shared link
        await pg.goto('file://'+sys.argv[1]+'#s='+urllib.parse.quote('unit_bar = kg lb\nfraction = 1/32')); await pg.reload(); await pg.wait_for_timeout(300)
        await pg.goto('file://'+sys.argv[1]+'?x#s='+urllib.parse.quote('unit_bar = kg lb\nfraction = 1/32')); await pg.wait_for_timeout(500)
        print('existing: offer shown', not await pg.evaluate("document.getElementById('offer').hidden"), '| bar unchanged', (await pg.eval_on_selector_all('#unitbar button','bs=>bs.map(b=>b.textContent)'))[:2])
        await pg.click('#offerUse'); await pg.wait_for_timeout(100)
        print('after Use it:', await pg.eval_on_selector_all('#unitbar button','bs=>bs.map(b=>b.textContent)'))
        await pg.click('#setShare'); await pg.wait_for_timeout(200)
        print('share ->', (await pg.evaluate('navigator.clipboard.readText()'))[:95], '|', await pg.inner_text('#setMsg'))
        print('errors', errs); await b.close()
asyncio.run(main())
