#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Mock treestatus server which returns the same response for every request.
# Set the initial response via the STATUS environmental variable - default
# is "open".
#
# If the environmental variable IS_TESTING is set to a true value, the status
# can be updated by PUTing or POSTing the new status to /
# eg. curl -X PUT http://treestatus.example.com/closed

import os

from flask import Flask, jsonify, abort

app = Flask('treestatus')


@app.route('/__heartbeat__')
@app.route('/__lbheartbeat__')
def heartbeat():
    return 'ok'


@app.route('/__version__')
def version():
    with open('/app/version.json') as f:
        return app.response_class(f.read(), mimetype='application/json')


@app.route('/<status>', methods=['PUT', 'POST'])
def set_status(status):
    if not os.getenv('IS_TESTING', ''):
        abort(405)
    os.environ['STATUS'] = status
    return 'treestatus set to: %s\n' % status


@app.route('/', defaults={'path': ''})
@app.route('/<tree>')
def status_open(tree):
    return jsonify({'status': os.getenv('STATUS', 'open')})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
