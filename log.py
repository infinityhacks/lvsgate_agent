#coding=utf-8
import os
import logging
from logging import handlers
import time

g_log_inited = False
FORMAT_FULL = "tm=%(asctime)s`th=%(threadName)s`level=%(levelname)s`m=%(module)s`f=%(funcName)s`%(message)s" 
FORMAT = "tm=%(asctime)s`%(module)s`%(funcName)s`%(message)s"
FORMAT_ERR = "tm=%(asctime)s`level=%(levelname)s`%(message)s"
DATEFMT = '%Y-%m-%d %H:%M:%S'

def get_stream_logger(name, level):
  logger = logging.getLogger(name)

  [x.close() for x in logger.handlers]
  del logger.handlers[:]

  logger.setLevel(level)

  hstream = logging.StreamHandler()
  hstream.setLevel(level)
  hstream.setFormatter(logging.Formatter(FORMAT_FULL, datefmt=DATEFMT))
  logger.addHandler(hstream)
  return logger

def align_rolloverat(h):
  t = list(time.localtime(h.rolloverAt))
  mask = [0,0,0,0,0,0,0,0,-1]
  p = {'S':6, 'M':5, 'H':4, 'D':3, 'W':3, 'MIDNIGHT':3}.get(h.when, 0)
  h.rolloverAt =  time.mktime(t[:p] + mask[p:])

def initlog(logdir, prefix, suffix='', level=logging.DEBUG, when='MIDNIGHT',
  backupCount=14):
  global g_log_inited
    
  if g_log_inited:
    return
 
  get_stream_logger("", level) 
  err_log = logging.getLogger("error")
  main_log = logging.getLogger("main")
  profile_log = logging.getLogger("profile")
  statis_log = logging.getLogger("statis")

  if not os.path.exists(logdir):
    os.makedirs(logdir)
  if suffix:
    logfile = os.path.join(logdir, "%s.log.%s"%(prefix, suffix))
  else:
    logfile = os.path.join(logdir, "%s.log"%(prefix))
  errfile = "%s.err"%logfile
  profile = "%s.profile"%logfile
  statisfile = "%s.statis"%logfile

  main_log.setLevel(level)
  err_log.setLevel(logging.WARNING)
  profile_log.setLevel(logging.DEBUG)
  statis_log.setLevel(logging.INFO)

  hlog = handlers.TimedRotatingFileHandler(logfile, when=when,
    backupCount=backupCount)
  align_rolloverat(hlog) 
  hlog.setLevel(level)
  hlog.setFormatter(logging.Formatter(FORMAT, datefmt=DATEFMT))
  main_log.addHandler(hlog)
  
  herr = handlers.TimedRotatingFileHandler(errfile, when=when,
    backupCount=backupCount)
  align_rolloverat(herr)
  herr.setLevel(logging.WARNING)
  herr.setFormatter(logging.Formatter(FORMAT_ERR ,datefmt=DATEFMT))
  err_log.addHandler(herr)

  hpro = handlers.TimedRotatingFileHandler(profile, when=when,
    backupCount=backupCount)
  align_rolloverat(hpro) 
  hpro.setLevel(logging.DEBUG)
  hpro.setFormatter(logging.Formatter(FORMAT, datefmt=DATEFMT))
  profile_log.addHandler(hpro) 

  hstatis = handlers.TimedRotatingFileHandler(statisfile, when=when,
      backupCount=backupCount)
  align_rolloverat(hstatis)
  hstatis.setLevel(logging.INFO)
  hstatis.setFormatter(logging.Formatter(FORMAT_FULL, datefmt=DATEFMT))
  statis_log.addHandler(hstatis)

  g_log_inited = True

