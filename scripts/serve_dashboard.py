"""
Local Web Server for Sales Performance & Revenue Growth Dashboard
Serves the web/ dashboard on http://localhost:8050
"""

import os
import sys
import http.server
import socketserver

PORT = 8050
WEB_DIR = os.path.join(r"D:\Power BI\Sales Performance & Revenue Growth Dashboard", "web")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable cache during active review
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def run_server():
    os.chdir(WEB_DIR)
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"================================================================")
        print(f"  SALES PERFORMANCE & REVENUE GROWTH DASHBOARD LOCAL SERVER")
        print(f"  Access Dashboard at: http://localhost:{PORT}")
        print(f"  Root Directory: {WEB_DIR}")
        print(f"================================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer terminated by user.")

if __name__ == "__main__":
    run_server()
