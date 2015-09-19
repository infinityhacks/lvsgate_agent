#coding=utf-8
import datetime

import util
import config
import tenjin

class Keepalived:
  def __init__(self):
    pass

  def update_conf(self, param):
    engine = tenjin.Engine()
    output = engine.render(config.KEEPALIVED_TEMPLATE_PATH, param)
    main_log.debug(output)

    f = open(config.tmp_path, 'w')
    f.write(output)
    f.close()

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    shutil.copyfile(config.KEEPALIVED_CONF_PATH,
        "%s-%s"%(config.KEEPALIVED_CONF_PATH, timestamp))
    shutil.copyfile(config.KEEPALIVED_TMP_PATH, self.KEEPALIVED_CONF_PATH)

  def reload(self):
    util.execute_cmd(["service", "keepalived", "reload"]) 

  def restart(self):
    util.execute_cmd(["service", "keepalived", "restart"])
     
  def stop(self):
    util.execute_cmd(["service", "keepalived", "stop"])

        
