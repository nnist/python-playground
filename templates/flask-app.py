#!/usr/bin/env python3

import time
from flask import Flask 
app = Flask(__name__) 

# TODO Use templates to show a page

@app.route("/") 
def hello():
    app.logger.info('verbose')
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    
    text = str(time.time())
    return "<b>{}</b>".format(text)

if __name__ == "__main__":
    app.debug = True
    app.run()
