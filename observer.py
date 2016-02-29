#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

#import file_manager
import operator

class observer(object):
    def __init__(self):
        #self.fm = file_manager.file_manager()
        pass

    def operate_skydip(self, params):
        skydip = operator.skydip()
        #id = self.insert_log('skydip', 'skydip')
        obs_id, evaluation_results = skydip.start(params)
        #self.update_log(id, obs_id)
        return evaluation_results

    def operate_ps(self, params):
        ps = operator.ps()
        #id = self.insert_log('ps', 'obs_ps')
        path = ps.start(params)
        #self.update_log(id, obs_id)
        return path
    
