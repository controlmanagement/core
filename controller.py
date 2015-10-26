#! /usr/bin/env python
# coding:utf-8

"""
------------------------------------------------
[Detail Description]

    controller:
        move_hotload
        move_m4
        get_condition


    time.gmtime()
------------------------------------------------
[History]

2015/10/26 maruyama

------------------------------------------------
"""
import time

class beam(object):
    
    def set_r(self):
        pass
    
    def set_sky(self):
        pass
    
    def m4_in(self):
        pass
    
    def m4_out(self):
        pass
    
    def get_status(self):
        pass


# class antenna(object):

# class receiver(object):


class condition(object):
    
    def get_status(self):
        pass


#class doppler(object):


class controller(object):
    
    def __init__(self):
        
        # import telescope_nanten.antenna_nanten
        import telescope_nanten.beam_nanten
        # import telescope_nanten.receiver_nanten
        import telescope_nanten.condition_nanten
        # import telescope_nanten.doppler_nanten
        
        # self.ant = telescope_nanten.antenna_nanten.antenna_nanten()
        self.beam = telescope_nanten.beam_nanten.beam_nanten()
        # self.rx = telescope_nanten.receiver_nanten.receiver_nanten()
        self.condition = telescope_nanten.condition_nanten.condition_nanten()
        # self.doppler = telescope_nanten.doppler_nanten.doppler_nanten()
        return
    
    def move_hotload(self, position):
        """hotloadを動かす"""
        if position == "r": self.beam.set_r()
        elif position == "sky": self.beam.set_sky()
        return
    
    def move_m4(self, position):
        """mirror4を動かす"""
        if position == "in": self.beam.m4_in()
        elif position == "out": self.beam.m4_out()
        return
    
    def get_condition(self):
        """現在の機器and天気のステータスを取得"""
        timestamp = time.time()
        # ant_status = self.ant.get_status()
        beam_status = self.beam.get_status()
        # sg_status = self.doppler.get_status()
        condition = self.condition.get_status()
        # gps_status = 
        condition['timestamp'] = timestamp
        # condition['az'] = ant_status[0]
        # condition['el'] = ant_status[1]
        condition['beam'] = beam_status
        # condition['sg'] = sg_status
        return condition
    
