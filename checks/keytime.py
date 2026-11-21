import asyncio
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':375,'height':629}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=UA)
        pg = await ctx.new_page(); cdp = await ctx.new_cdp_session(pg)
        await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        await pg.goto('http://localhost:8780/'); await pg.wait_for_timeout(900)
        # time a real key path: dispatch touchstart on a keypad key, measure handler + forced layout
        t = await pg.evaluate("""() => { const keys = [...'1234567890'].map(c => document.querySelector(`#pad [data-key="${c}"]`)); const c = document.querySelector('#pad [data-act="clear"]');
          const fire = b => { const t = new Touch({ identifier: 1, target: b, clientX: 10, clientY: 10 }); b.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [t], targetTouches: [t], changedTouches: [t] })); b.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [t] })); };
          let total = 0, n = 0;
          for (let r = 0; r < 6; r++) { fire(c); for (const k of keys.slice(0, 6)) { const t0 = performance.now(); fire(k); document.body.offsetHeight; total += performance.now() - t0; n++; } }
          return total / n; }""")
        print('per keypad key, script + layout, 4x slower CPU: %.1f ms' % t)
        await b.close()
asyncio.run(main())
