import sys, asyncio
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':375,'height':720}, screen={'width':375,'height':812}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=UA)
        pg = await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(800)
        await pg.keyboard.type('100')
        print('status:', await pg.inner_text('#calStatus'))
        await pg.click('#calOpen'); await pg.wait_for_timeout(200)
        w = await pg.eval_on_selector('#calbar','e=>e.getBoundingClientRect().width')
        print('card bar css px', round(w,1), '-> px/mm', round(w/53.98,3), '(iPhone X/XS/11 Pro expected 6.011)')
        await pg.click('#calPlus'); await pg.click('#calPlus')
        print('after +2:', await pg.evaluate("localStorage.getItem('uc-pxmm')"), '|', await pg.inner_text('#calStatus'))
        await pg.screenshot(path='r1.png')
        await pg.click('#calReset'); print('reset:', await pg.inner_text('#calStatus'))
        await pg.click('#calDone'); await pg.keyboard.type('5'); print('typing after done:', await pg.eval_on_selector('#q','e=>e.value'))
        a = await b.new_context(viewport={'width':412,'height':800}, device_scale_factor=2.6, is_mobile=True, user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) Chrome/120 Mobile')
        q = await a.new_page(); await q.goto('file://'+sys.argv[1]); await q.wait_for_timeout(500)
        print('android status:', await q.inner_text('#calStatus'))
        print('errors', errs); await b.close()
asyncio.run(main())
