from . import *

from flask import render_template


@app.route('/u/<path:filename>')
def list_characters(filename):
    ...
