import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await (await b.new_context(viewport={'width':375,'height':720}, device_scale_factor=2, is_mobile=True, has_touch=True)).new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(500)
        await pg.click('#qrOpen'); await pg.wait_for_timeout(100); await pg.screenshot(path='qr.png')
        await pg.click('#qrClose'); print('closed:', await pg.evaluate("document.getElementById('qr').hidden"))
        await pg.click('#qrOpen'); await pg.keyboard.press('Escape'); print('esc closes:', await pg.evaluate("document.getElementById('qr').hidden"))
        await pg.keyboard.type('12'); print('typing works after:', await pg.eval_on_selector('#q','e=>e.value'))
        print('errors', errs); await b.close()
asyncio.run(main())
