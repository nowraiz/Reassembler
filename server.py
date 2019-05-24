import binascii
import hashlib
import hmac
import io
import os
import pickle
import tempfile
import traceback

import pymongo
from bson import ObjectId
from flask import Flask, jsonify, request, abort, after_this_request

import ReassemblerEngine

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
windows = os.name == 'nt'
SECRET_KEY = binascii.unhexlify('8a5e271d56033e75f12171993c267d57013adc1bc07bc8672bbf726b')
client = pymongo.MongoClient(
    
)
db = client[os.environ.get('DATABASE_NAME', 'coogledb')]


@app.errorhandler(Exception)
def on_error(exception):
    traceback.print_exc()
    response = jsonify(error=str(exception))
    response.status_code = 500
    return response


def _compute_checksum(f):
    auth = hmac.new(SECRET_KEY, digestmod=hashlib.sha256)
    for chunk in iter(lambda: f.read(4096), b''):
        auth.update(chunk)
    f.seek(0)
    return auth.hexdigest()


def runRamblr(file):
    try:
        labels = ReassemblerEngine.run(file)
    except Exception as E:
        print(E)
        return None
    return labels

@app.route('/',methods=['POST'])
def handle():
    request_file = request.files['file']
    computed_checksum = _compute_checksum(request_file)
    checksum = request.headers.get('Checksum', '')
    if not hmac.compare_digest(checksum, computed_checksum):
        abort(400)

    with tempfile.NamedTemporaryFile(delete=not windows) as f:
        @after_this_request
        def clean_up(resp):
            if windows:
                os.remove(f.name)
            return resp

        request_file.save(f.name)

        labels = runRamblr(f.name)
        if labels:
            resp = {'name' : f.name, 'addrToLabel' : labels }
            return jsonify(resp)
    abort(400)
if __name__ == '__main__':
    app.run()
