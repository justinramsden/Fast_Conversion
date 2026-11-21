import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await (await b.new_context(viewport={'width':375,'height':700}, device_scale_factor=2, is_mobile=True, has_touch=True)).new_page()
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(400)
        print('phone: tips visible', await pg.is_visible('#waysHead'), '| open', await pg.evaluate("document.getElementById('tips').open"))
        await pg.tap('#tips summary'); await pg.wait_for_timeout(100)
        await pg.tap('[data-try="3 lb 4 oz"]'); await pg.wait_for_timeout(100)
        print('try button:', await pg.eval_on_selector('#q','e=>e.value'), '|', (await pg.inner_text('.quad')).split('\n')[0], '| scrolled top', await pg.evaluate('scrollY'))
        await pg.evaluate("document.getElementById('tips').scrollIntoView()"); await pg.screenshot(path='tips.png')
        d = await (await b.new_context(viewport={'width':1200,'height':800})).new_page(); await d.goto('file://'+sys.argv[1]); await d.wait_for_timeout(300)
        print('desktop: open', await d.evaluate("document.getElementById('tips').open"), '| keys notes visible', await d.is_visible('#keysHead'))
        print('errors', errs); await b.close()
asyncio.run(main())
