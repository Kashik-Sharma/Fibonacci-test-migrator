#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!//anaconda/bin/python
#!flask/bin/python
from app import app
from logger_config import logger

if __name__ == "__main__":
    logger.info("Starting Flask application.")
    app.run(debug=True)