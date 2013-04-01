#!/bin/bash

uwsgi --plugins python32 -s /tmp/uwsgi.sock -w brailleconverter \
"$@"
