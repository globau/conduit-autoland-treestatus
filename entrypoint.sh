#!/bin/sh
case "${1:-start}" in
    "start")
        cd /app
        exec gunicorn --bind 0.0.0.0:${PORT:-8000} treestatus:app
        ;;
    *)
        exec $*
        ;;
esac
