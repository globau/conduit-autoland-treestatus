#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Mock treestatus server which returns the same response for every request.
# Set the response via the STATUS environmental variable - default is "open".

import os
from flask import Flask, jsonify
app = Flask('treestatus')


# mozilla-services/Dockerflow


@app.route('/__heartbeat__')
@app.route('/__lbheartbeat__')
def heartbeat():
    return 'ok'


@app.route('/__version__')
def version():
    with open('version.json') as f:
        return app.response_class(f.read(), mimetype='application/json')

# treestatus


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def status_open(path):
    return jsonify({'status': os.getenv('STATUS', 'open')})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 80)))
