#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Mock treestatus server which returns the same response for every request.
# Set the response via the STATUS environmental variable - default is "open".

import json
import os
import sys

from flask import Flask, jsonify

app = Flask('treestatus')


@app.route('/__heartbeat__')
@app.route('/__lbheartbeat__')
def heartbeat():
    return 'ok'


@app.route('/__version__')
def version():
    with open('/app/version.json') as f:
        return app.response_class(f.read(), mimetype='application/json')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def status_open(path):
    return jsonify({'status': os.getenv('STATUS', 'open')})


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'version':
        # Generate version.json for Dockerflow
        version = {
            'commit': os.getenv('CIRCLE_SHA1', None),
            'version': os.getenv('CIRCLE_SHA1', None),
            'source': 'https://github.com/globau/conduit-autoland-treestatus',
            'build': os.getenv('CIRCLE_BUILD_URL', None)
        }
        print(json.dumps(version))

    else:
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
