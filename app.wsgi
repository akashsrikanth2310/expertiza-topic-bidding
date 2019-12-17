#!/home/ubuntu/expertiza-topic-bidding/venv/bin/python3
#-*- coding: utf-8 -*-

import sys, logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/expertiza-topic-bidding/")
sys.path.insert(0, "/home/ubuntu/expertiza-topic-bidding/venv/bin")
sys.path.insert(0, "/home/ubuntu/expertiza-topic-bidding/venv/lib/python3.6")
sys.path.insert(0, "/home/ubuntu/expertiza-topic-bidding/venv/lib/python3.6/site-packages")
sys.path.insert(0, "/usr/lib/python3/site-packages")

from main import app as application
