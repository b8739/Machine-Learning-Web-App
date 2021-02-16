#!/bin/bash
cd server/env
source Scripts/activate
cd ..
FLASK_APP=app.py FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 flask run
