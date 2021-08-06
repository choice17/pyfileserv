#########################################################################################
# example usage
# client side
# - download file
# curl -o <filename> http://<ip>:<port>/download?name=<filename>
# - upload file
# curl -F "data=@<file-location>"" -X POST http://<ip>:<port>/upload?name=<filename>
########################################################################################

from flask import Flask, Response, request, jsonify, send_file
import argparse
import os
from collections import defaultdict
import datetime
import sys
import io

DOWNLOAD_DIR = "download"
UPLOAD_DIR = "upload"

class FLASK_APP(object):
    def __init__(self, *args, **kwargs):
        self.thread = None
        self.thread = None
        super(FLASK_APP, self).__init__(*args, **kwargs)
        self.args = defaultdict(int)
        self.models = defaultdict(lambda: None)
        self.log = {'server':
                                {'methods': defaultdict(lambda: [0, defaultdict(int)]),
                                 'visitor':defaultdict(int)}}
        self.start_time = str(datetime.datetime.now())
        self.app = Flask(__name__)
        self.add_url_rules()
        if not os.path.exists(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)
        if not os.path.exists(UPLOAD_DIR):
            os.mkdir(UPLOAD_DIR)
    def add_url_rules(self):
        #self.app.url_map.converters['regex'] = RegexConverter
        self.app.add_url_rule('/upload', 'upload', self.upload, methods=["POST"])
        self.app.add_url_rule('/download', 'download', self.download, methods=["GET"])
        self.app.add_url_rule('/get', 'get', self.get, methods=["GET"])


    def update_stat(self, method, ip):
        self.log['server']['methods'][method][0] += 1
        self.log['server']['visitor'][ip] += 1

    def get(self):
        self.update_stat(sys._getframe().f_code.co_name, str(request.remote_addr))
        data = {"success": True, "Message": "File server starttime: %s"%self.start_time}
        return jsonify(data)

    def download(self):
        fname = request.args.get('name')
        self.update_stat(sys._getframe().f_code.co_name, str(request.remote_addr))
        req_file = DOWNLOAD_DIR + "/" + fname
        if not os.path.exists(req_file):
            return jsonify({"message":f"fail to open file {fname}!!"})
        f = open(req_file, "rb")
        data = io.BytesIO(f.read())
        f.close()
        return send_file(data, mimetype="application/octet-stream")
    
    def upload(self):
        fname = request.args.get('name')
        self.update_stat(sys._getframe().f_code.co_name, str(request.remote_addr))
        data = request.files["data"].read()
        f = open(UPLOAD_DIR + "/" + fname, "wb")
        f.write(data)
        f.close()
        return jsonify({"message":f"succeed to upload file {fname}!!"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='192.168.10.243', action='store', help='server ip')
    parser.add_argument('--port', type=int, default=80, action='store', help='server port')
    args = parser.parse_args()
    print('[INFO] Please wait until server has fully started')
    flask_app = FLASK_APP()
    flask_app.app.run(host=args.host, port=args.port)

