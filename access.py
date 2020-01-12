import json
import urlparse, urllib
import argparse
import requests
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

REQUEST_TOKEN_URL = "https://www.strava.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.strava.com/oauth/token"

client_id = None
client_secret_key = None

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global client_id
        global client_secret_key
        request = urlparse.urlparse(self.path)
        qs = urlparse.parse_qs(request.query)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if qs['code']:
            # Exchange a request code for an access token.
            code = qs['code'][0]
            params = {
                'client_id': client_id,
                'client_secret': client_secret_key,
                'code': code
            }
            r = requests.post(ACCESS_TOKEN_URL, params=params)
            response = r.text
            try:
                response = json.loads(response)
            except: pass

            if 'access_token' in response:
                print 'Access token: %s' % response['access_token']
                self.wfile.write('Access token: %s<br /><br />Copy the access token and supply it when running strava.py' % response['access_token'])
            else:
                self.wfile.write("Failed to get access token.")

            # Kill the HTTP server
            killer = threading.Thread(target=http_server.shutdown)
            killer.daemon = True
            killer.start()

        self.wfile.close()

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Acquire an access token for Strava API.')
    parser.add_argument('--client_id', dest='client_id')
    parser.add_argument('--secret_key', dest='secret_key')
    parser.add_argument('--port', dest='port', default=15642)
    args = parser.parse_args()

    if not args.client_id:
        print "client_id not specified"
        exit()

    if not args.secret_key:
        print "secret_key not specified"
        exit()

    client_id = args.client_id
    client_secret_key = args.secret_key

    try:
        args.port = int(args.port)
    except: pass

    if not isinstance(args.port, int):
        print "port must be integer"
        exit()

    # Point to the authorization page on strava.com.
    params = {
        'client_id': args.client_id,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:' + str(args.port),
        'scope': 'activity:write'
    }
    request_token_url = REQUEST_TOKEN_URL + "?" + urllib.urlencode(params)

    print "Visit the following URL and follow the instructions: %s" % request_token_url

    # Start an HTTP server to capture the 'code' parameter when
    # the user returns from strava.com.
    http_server = HTTPServer(('0.0.0.0', args.port), RequestHandler)
    try:
        http_server.serve_forever()

    except KeyboardInterrupt: pass
    http_server.server_close()
