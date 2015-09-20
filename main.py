#coding=utf-8
import os
import sys
import logging
import signal
import time
import BaseHTTPServer
import json
import threading
import urllib2
import traceback
import BaseHTTPServer
import socket

import log
import daemonize
from keepalived import Keepalived

__VERSION__ = '1.0'

slog = log.get_stream_logger("main", logging.DEBUG)
main_log = logging.getLogger("main")

keepalived = Keepalived()

class LVSRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
        client_address, server) 

  def address_string(self):
    host, port = self.client_address[:2]
    return host
  
  def log_message(self, format, *args):
    main_log.info("%s - - %s\n" % (self.address_string(), format%args))

  def send_normal_response(self, code, msg):
    main_log.info("response status:%d body:%s" % (code, msg)) 
    self.send_response(code)
    self.send_header('content-length', len(msg))
    self.end_headers()
    self.wfile.write(msg)

  def do_GET(self):
    self.log_message("request GET %s" % self.path)
    self.send_error(404)

  def do_POST(self):
    self.log_message("request POST %s" % self.path)
    body_len = self.headers.getheader('content-length')
    try:
      body_len = int(body_len)
    except:
      body_len = 0
    if body_len <= 0:
      raise ValueError, "content-length<0"
      return

    post = self.rfile.read(body_len)
    self.log_message("POST DATA:%s"%post)
    param = json.loads(post)
    
    if self.path == '/update_base':
      keepalived.update_base_conf(param)
    elif self.path == '/update_vs':
      keepalived.update_vs_conf(param)
    elif self.path == '/update_snat':
      keepalived.update_snat_conf(param)
    else:
      self.send_error(404)
      return

    keepalived.reload()

    resp = {'status': 0, 'msg': 'OK'}
    self.send_normal_response(200, json.dumps(resp))


class LVSHTTPServer(BaseHTTPServer.HTTPServer):
  def __init__(self, server_address, RequestHandlerClass):
    BaseHTTPServer.HTTPServer.allow_reuse_address = True
    BaseHTTPServer.HTTPServer.__init__(self, server_address,
        RequestHandlerClass)
    self.stop = False

if __name__ == '__main__':
  import optparse
  
  socket.setdefaulttimeout(10)
  usage = "python main.py [-s host] -p port [-D] [-d]"
  optparser = optparse.OptionParser(usage=usage, version=__VERSION__)
  optparser.add_option("-s", "--host", action="store", dest="host", \
                        type="string", default="0.0.0.0", \
                        help="ip address or host to bind, default is 0.0.0.0")
  optparser.add_option("-p", "--port", action="store", dest="port", \
                        type="int", help="port to listen")
                        
  optparser.add_option("-d", "--daemon", action="store_true", \
                        dest="daemonize", default=False, help="daemonize")
                        
  optparser.add_option("-D", "--debug", action="store_true", dest="debug", \
                       default=False, help="Print debug info")
                        

  options, args = optparser.parse_args(None)
  if not options.port:
    optparser.print_help()
    sys.exit(0)

  httpd = LVSHTTPServer((options.host, int(options.port)), LVSRequestHandler)
  while not httpd.stop:
    httpd.handle_request()
