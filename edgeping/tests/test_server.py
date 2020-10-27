import  threading
import socketserver
import requests
import time
from contextlib import contextmanager
import zlib
import gzip
import json
import io

from edgeping.server import PingHandling


@contextmanager
def server(host="localhost", port=0):
    httpd = socketserver.TCPServer((host, port), PingHandling)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()
    time.sleep(0.01)
    try:
        yield f"http://{httpd.server_address[0]}:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        server_thread.join()


def test_server_status():

    with server() as root_url:
        res = requests.get(root_url + "/status")
        assert res.text  == 'OK'

def zip_content(json_content):
    s = io.BytesIO()
    with gzip.GzipFile(fileobj=s, mode='w') as g:
        g.write(json.dumps(json_content).encode())
    return s.getvalue()


def test_server_data():

    with server() as root_url:
        # posting data
        headers = {'content-encoding' :'gzip'}
        data = {"my": "data"}
        zdata = zip_content(data)
        zlib.decompress(zdata, zlib.MAX_WBITS | 16)

        url = "/submit/<namespace>/<docType>/<docVersion>/<docId>"
        res = requests.post(root_url + url, data=zdata, headers=headers)
        assert res.text  == 'OK'

        # getting it back
        res = requests.get(root_url + "/pings")
        assert res.json()  ==  [data]

        # deleting it
        res = requests.delete(root_url + "/pings")
        assert res.text  == 'OK'

        res = requests.get(root_url + "/pings")
        assert res.json()  == []

