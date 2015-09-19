#coding=utf-8

import subprocess
import time
import logging
import os
import traceback
import urllib2
import urllib
import json


def excute_cmd(args, timeout=5):
    status, output = -1, "excute cmd(%s) fail" % args;
    p = subprocess.Popen(args, stdin=subprocess.PIPE,
      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.stdout.read()
    while 1:
      status = p.poll() 
      if status is not None:
        break
      timeout -= 1
      if timeout <= 0:
        break
      time.sleep(1)

    if status is None:
      p.terminate()
      status = -1
    return status, output
