import http.server, gzip, os, sys
root = sys.argv[1]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=root, **k)
    def log_message(s, *a): pass
    def send_head(s):
        path = s.translate_path(s.path.split('?')[0])
        if os.path.isdir(path): path = os.path.join(path, 'index.html')
        if not os.path.exists(path): return super().send_head()
        data = open(path, 'rb').read(); ctype = s.guess_type(path)
        if path.endswith(('.html', '.js', '.webmanifest', '.css')) and 'gzip' in s.headers.get('Accept-Encoding', ''):
            data = gzip.compress(data); enc = True
        else: enc = False
        s.send_response(200); s.send_header('Content-Type', ctype); s.send_header('Content-Length', str(len(data)))
        if enc: s.send_header('Content-Encoding', 'gzip')
        s.send_header('Cache-Control', 'max-age=600'); s.end_headers()
        import io; return io.BytesIO(data)
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[2])), H).serve_forever()
