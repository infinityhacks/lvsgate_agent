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
  url = "http://%s:%s/update_base"%(host, port)
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

def test_api_vsconfig(host, port):
  url = "http://%s:%s/update_vs"%(host, port)
  param = {
          'virtual_server': [
                {
                        'name': 'vs1',
                        'syn_proxy': 1,
                        'lb_kind': 'NAT',
                        'protocol': 'TCP',
                        'lb_algo': 'rr',
                        'persistence_timeout': 10,
                        'rise': 2,
                        'fall': 3,
                        'delay_loop': 10,
                        'listen_address': [
                                ('192.168.0.249', 9923),
                                ('192.168.200.1', 9923),
                                ('100.84.81.254', 9923),
                        ],
                        'real_server': [
                                {
                                        'address': ('10.0.0.3', 22),
                                        'weight': 1,
                                        'health_check': {
                                                'type': 'TCP_CHECK',
                                                'connect_timeout': 5
                                        }
                                },
                        ]
                },
                {
                        'name': 'vs2',
                        'syn_proxy': 1,
                        'lb_kind': 'FNAT',
                        'protocol': 'TCP',
                        'lb_algo': 'rr',
                        'persistence_timeout': 10,
                        'rise': 2,
                        'fall': 3,
                        'delay_loop': 10,
                        'listen_address': [
                                ('192.168.200.2', 80),
                                ('192.168.200.1', 80),
                                ('192.168.200.3', 80),
                        ],
                        'real_server': [
                                {
                                        'address': ('10.0.0.3', 80),
                                        'weight': 1,
                                        'health_check': {
                                                'type': 'TCP_CHECK',
                                                'connect_timeout': 5
                                        }
                                },
                                {
                                        'address': ('10.0.0.3', 8080),
                                        'weight': 1,
                                        'health_check': {
                                                'type': 'TCP_CHECK',
                                                'connect_timeout': 5
                                        }
                                },
                        ]
                },

                {
                        'name': 'vs_udp',
                        'syn_proxy': 1,
                        'lb_kind': 'NAT',
                        'protocol': 'UDP',
                        'lb_algo': 'rr',
                        'persistence_timeout': 10,
                        'rise': 2,
                        'fall': 3,
                        'delay_loop': 10,
                        'listen_address': [
                                ('192.168.200.1', 53),
                        ],
                        'real_server': [
                                {
                                        'address': ('10.0.0.3', 53),
                                        'weight': 1,
                                        'health_check': {
                                                'type': 'TCP_CHECK',
                                                'connect_timeout': 5
                                        }
                                },
                        ]
                },
          ]
  }
  send_http_post(url, param)
  
if __name__ == '__main__':
  import sys
  host, port = sys.argv[1], sys.argv[2]
  test_api_ipconfig(host, port)
  test_api_vsconfig(host, port)
