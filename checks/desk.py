import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':1100,'height':900}, permissions=['clipboard-read','clipboard-write'])
        pg = await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(700)
        await pg.keyboard.type(sys.argv[2] if len(sys.argv)>2 else '10mils')
        await pg.screenshot(path='desk_new.png')
        vis = lambda sel: pg.eval_on_selector(sel, 'e=>getComputedStyle(e).display')
        print('padkeys', await vis('#padkeys'), '| quad', await vis('.quad'), '| hint', await vis('#hint'))
        await pg.keyboard.press('ArrowDown'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(100)
        print('arrow+Enter copies tile 2:', await pg.evaluate('navigator.clipboard.readText()'), '| hint:', await pg.inner_text('#hint'))
        print('errors', errs); await b.close()
asyncio.run(main())
