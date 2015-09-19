#coding=utf-8
import urllib2
import json
import urllib
import sys
import os

def send_http_post(url, param):
  print url
  print param
  if param:
    data = json.dumps(param)
    request = urllib2.Request(url, data = data)
  else:
    request = urllib2.Request(url)
    
  f = urllib2.urlopen(request, timeout = 120)
  print f.read()

  
def test_api_ipconfig(host, port):
  url = "http://%s:%s/"%(host, port)
  param = {
          'vrrp_interface': 'eth0',
          'virtual_router_id': 254,
          'vrrp_priority': 100,
          'virtual_ipaddress': [
                ('192.168.0.248/24', 'eth0'),
                ('192.168.0.247/24', 'eth0'),
          ],
          'local_address': [
                '10.0.1.10-200',
                '10.0.1.250',
                '10.0.1.251',
                '10.0.1.252',
          ],
  }
  
  send_http_post(url, param)
  
if __name__ == '__main__':
  import sys
  host, port = sys.argv[1], sys.argv[2]
  test_api_ipconfig(host, port)
