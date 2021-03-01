#!/bin/bash
cd server/newenv
source Scripts/activate
cd ..
FLASK_APP=app.py FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 flask run
