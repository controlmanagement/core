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

2015/12/17 maruyama

------------------------------------------------
"""
import time

class beam(object):
    
    def hot_in(self):
        pass
    
    def hot_out(self):
        pass
    
    def hot_stop(self):
        pass

    def m4_in(self):
        pass
    
    def m4_out(self):
        pass
    
    def m4_stop(self):
        pass

    def get_status(self):
        pass


class antenna(object):

    def drive_on(self):
        pass
     
    def drive_off(self):
        pass
    
    def azel_move(self):
        pass

    def radec_move(self):
        pass
    
    def planet_move(self):
        pass
    
    def tracking_end(self):
        pass
    
    def clear_error(self):
        pass
    
    def start_limit_check(self):
        pass
    
    def stop_limit_check(self):
        pass

class receiver(object):
        
    def oneshot_dfs01(self):
        pass
    
    def oneshot_dfs02(self):
        pass

class condition(object):
    
    def get_status(self):
        pass


#class doppler(object):

class controller(object):
    
    def __init__(self):
        
        import telescope_nanten.antenna_nanten
        #import telescope_nanten.beam_nanten
        import telescope_nanten.receiver_nanten
        #import telescope_nanten.condition_nanten
        # import telescope_nanten.doppler_nanten
        
        self.ant = telescope_nanten.antenna_nanten.antenna_nanten()
        #self.beam = telescope_nanten.beam_nanten.beam_nanten()
        self.rx = telescope_nanten.receiver_nanten.receiver_nanten()
        #self.condition = telescope_nanten.condition_nanten.condition_nanten()
        # self.doppler = telescope_nanten.doppler_nanten.doppler_nanten()
        return
    
    def initialize_observation(self):
        """
        観測の初期化を行う。
        実行項目は、
        ・アンテナ指向性能の大気屈折補正
        ・黒体スライダを R に
        """
        #self.correct_atmosphere()
        self.move_hot("r")
        return

    def move_hot(self, position):
        """hotloadを動かす("in"or"out")"""
        if position == "in": self.beam.hot_in()
        elif position == "out": self.beam.hot_out()
        return
    
    def move_m4(self, position):
        """mirror4を動かす("in"or"out")"""
        if position == "in": self.beam.m4_in()
        elif position == "out": self.beam.m4_out()
        return
    
    def oneshot(self, repeat=1, exposure=1.0, stime=0.0):
        #分光計oneshotのcount値を配列で出力
        dfs01 = self.rx.oneshot_dfs01(repeat, exposure ,stime)
        dfs02 = self.rx.oneshot_dfs02(repeat, exposure ,stime)
        return {"dfs1":dfs01,
                "dfs2":dfs02}
    
    def get_status(self):
        #現在の機器and天気のステータスを取得
        timestamp = time.time()
        # ant_status = self.ant.get_status()
        #beam_status = self.beam.get_status()
        # sg_status = self.doppler.get_status()
        # gps_status = 
        status = { "timestamp" : timestamp,
                   #"m4" : beam_status[1],
                   #"hot" : beam_status[0],
                   }
        return status

class read_status(object):
    
    def __init__(self):
        
        import telescope_nanten.equipment_nanten
        self.status = telescope_nanten.equipment_nanten.read_status()

    def read_status(self):
        """機器and天気のステータスを取得_"""
        timestamp = time.strftime('%Y/%m/%d %H:%M:%S',time.gmtime())
        ant_status = self.status.get_antenna()
        #beam_status = self.status.get_beam()
        # sg_status = self.doppler.get_status()
        ret = self.status.get_weather()
        # condition['az'] = ant_status[0]
        # condition['el'] = ant_status[1]
        # condition['sg'] = sg_status
        """
        status = { "time" : timestamp,
                   "Year" : ret[0],
                   "Month" : ret[1],
                   "Day" : ret[2],
                   "Hour" : ret[3],
                   "Min" : ret[4],
                   "Sec" : ret[5],
                   "InTemp" : ret[6],
                   "OutTemp" : ret[7],
                   "InHumi" : ret[8],
                   "OutHumi" : ret[9],
                   "WindDir" : ret[10],
                   "WindSp" : ret[11],
                   "Press" : ret[12],
                   "Rain" : ret[13],
                   "CabinTemp1" : ret[14],
                   "CabinTemp2" :ret[15],
                   "DomeTemp1" : ret[16],
                   "DomeTemp2" : ret[17],
                   "GenTemp1" : ret[18],
                   "GenTemp2" : ret[19],
                   "m4" : beam_status[1],
                   "hot" : beam_status[0],
                   }
        """
        status = { "time" : timestamp,
                   "current_az" : ant_status[0],
                   "current_el" : ant_status[1],
                   "command_az" : ant_status[2],
                   "command_el" : ant_status[3],
                   "Year" : ret[0],
                   "Month" : ret[1],
                   "Day" : ret[2],
                   "Hour" : ret[3],
                   "Min" : ret[4],
                   "Sec" : ret[5],
                   "InTemp" : ret[6],
                   "OutTemp" : ret[7],
                   "InHumi" : ret[8],
                   "OutHumi" : ret[9],
                   "WindDir" : ret[10],
                   "WindSp" : ret[11],
                   "Press" : ret[12],
                   "Rain" : ret[13],
                   "CabinTemp1" : ret[14],
                   "CabinTemp2" :ret[15],
                   "DomeTemp1" : ret[16],
                   "DomeTemp2" : ret[17],
                   "GenTemp1" : ret[18],
                   "GenTemp2" : ret[19],
                   }
                   
        return status
