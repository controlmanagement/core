#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
------------------------------------------------
[Detail Description]

    operator:
        role: 各種観測を実行する
    


------------------------------------------------

"""

import time
import numpy
import math
import controller
#import file_manager
import os
import pylab
import datetime
#import ephem
#from Scientific.IO.FortranFormat import FortranFormat, FortranLine

def init():
    
    #import operator_ps
    #import operator_ss
    #import operator_otf
    #import operator_otf_quick
    #import operator_rotscan
    #import operator_radiop
    import operator_skydip
    #global ps
    #global standard_source
    global skydip
    #global otf
    #global otf_quick
    #global rotation_scan
    #global radio_pointing
    #ps = operator_ps.ps
    #standard_source = operator_ss.standard_source
    #otf = operator_otf.otf
    #otf_quick = operator_otf_quick.otf
    #rotation_scan = operator_rotscan.rotation_scan
    #radio_pointing = operator_radiop.radio_pointing
    
    skydip = operator_skydip.skydip
    
    return

#SS_EXPOSURE = 30. #標準天体のexposure

TIMESTAMP_PATH = '%Y%m%d-%H.%M.%S'
TIMESTAMP_DB = '%Y-%m-%d %H:%M:%S'
TIMESTAMP_DEFAULT = '0000-00-00 00:00:00'

DEFAULT_PARAMS = {'object': 'NO-NAME',
                  'on_x': 0.,
                  'on_y': 0.,
                  'on_coord': 'J2000',
                  'off_name': 'Dummy',
                  'offset_on_x': 0.,
                  'offset_on_y': 0.,
                  'offset_on_dcos': 0,
                  'offset_on_coord': 'SAME',
                  'vlsr': [0.,0.,0.],
                  'repeat': 1,
                  'exposure': 1.,
                  'r_interval': 5.,
                  'off_interval': 10.,
                  'path': '/home/1.85m/data/FITS/no_name',
                  'planet': None,
                  'planet_offset_off_x': 0.,
                  'planet_offset_off_y': 0.,
                  'planet_offset_off_dcos': 0,
                  'planet_offset_off_coord': 'HORIZONTAL',
                  'is_standardsource_id': None,
                  'num_x': 1,
                  'num_y': 1,
                  'delta_x': 1./60.,
                  'delta_y': 1./60.,
                  'delta_t': 1.,
                  'start_x': 0./60.,
                  'start_y': 0./60.,
                  'ramp': 3.,
                  'delay': 0.5,
                  'direction': 'H',
                  'scan_coord': 'SAME',
                  'scan_dcos': 0,
                  'degree': [0,],
                  }

class PllError(Exception): pass

class timekeeper(object):
    interval = 10.   # min.
    last_timestamp = 0.
    
    def __init__(self, interval_min):
        self.interval = self.min2sec(interval_min)
        pass
    
    def check(self):
        now = time.time()
        if self.interval <= (now - self.last_timestamp):
            self.last_timestamp = now
            return True
        return False
    
    def min2sec(self, minut):
        return minut * 60.

class operator(object):
    """
    すべての観測クラスの親クラス

    [メソッド]
      _motor_check - 観測前にAzをチェックする

    """
    
    def __init__(self):
        self.ctrl = controller.controller()
        #self.fm = file_manager.file_manager()
        #self.ss = file_manager.db_standard()
        #self.off = file_manager.db_offsource()
        #self.db_observer = file_manager.db_observer()
        return

"""
    def _motor_check(self, az, el):                                             
        #'''
        現在のazをチェックし、ソフトリミットがかかりそうな状態なら360度回転させる。
        #'''
        if -40<az<400: return
        elif 400.<az:
            new_az = az - 250
        elif az<-40.:
            new_az = az + 250
        else: pass
        self.fm.insert_record('error_log', [1, 'motor error az=%.2f'%az])
        self.ctrl.move_antenna(new_az, el, 'HORIZONTAL')
"""


init()

