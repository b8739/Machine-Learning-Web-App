#!/bin/bash
cd server/env37
source bin/activate
cd ..
FLASK_APP=app.py FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python3 -m flask run