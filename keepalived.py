#coding=utf-8
import datetime
import logging
import shutil
import os

import util
import config
import log

import tenjin
from tenjin.helpers import *

main_log = logging.getLogger("main")

class Keepalived:
  def __init__(self):
    pass

  def __update_conf(self, template_path, conf_path, param):
    engine = tenjin.Engine()
    output = engine.render(template_path, param)
    main_log.debug(output)

    basename = os.path.basename(conf_path)
    tmp_path = os.path.join(config.KEEPALIVED_TMP_DIR, basename) 

    f = open(tmp_path, 'w')
    f.write(output)
    f.close()

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    shutil.copyfile(conf_path, "%s-%s"%(conf_path, timestamp))
    shutil.copyfile(tmp_path, conf_path)


  def update_base_conf(self, param):
    self.__update_conf(config.KEEPALIVED_TEMPLATE_PATH,
        config.KEEPALIVED_CONF_PATH, param)

  def update_vs_conf(self, param):
    self.__update_conf(config.KEEPALIVED_TEMPLATE_VS_PATH,
        config.KEEPALIVED_CONF_VS_PATH, param)

  def update_snat_conf(self, param):
    self.__update_conf(config.KEEPALIVED_TEMPLATE_SNAT_PATH,
        config.KEEPALIVED_CONF_SNAT_PATH, param)

  def reload(self):
    util.execute_cmd(["service", "keepalived", "reload"]) 

  def restart(self):
    util.execute_cmd(["service", "keepalived", "restart"])
     
  def stop(self):
    util.execute_cmd(["service", "keepalived", "stop"])

        
