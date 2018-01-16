#!/bin/sh
case "${1:-start}" in
    "start")
        exec /app/treestatus.py
        ;;
    *)
        exec $*
        ;;
esac
