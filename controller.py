#! /usr/bin/env python
# coding:utf-8

"""
------------------------------------------------
[Detail Description]

------------------------------------------------
[History]


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

    def read_error(self):
        pass

    def start_domestatus_check(self):
        pass

    def stop_domestatus_check(self):
        pass

    def dome_open(self):
        pass

    def dome_close(self):
        pass

    def memb_open(self):
        pass

    def memb_close(self):
        pass

    def dome_move(self):
        pass

    def dome_stop(self):
        pass

    def dome_track(self):
        pass

    def dome_track_end(self):
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
        import telescope_nanten.beam_nanten
        import telescope_nanten.receiver_nanten
        #import telescope_nanten.condition_nanten
        #import telescope_nanten.doppler_nanten
        
        self.ant = telescope_nanten.antenna_nanten.antenna_nanten()
        self.beam = telescope_nanten.beam_nanten.beam_nanten()
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

    #for antenna

    def drive_on(self):
        """drive_on"""
        self.ant.drive_on()
        return

    def drive_off(self):
        """drive_off"""
        self.ant.drive_off()
        return

    def azel_move(self, az_arcsec, el_arcsec, az_rate = 12000, el_rate = 12000):
        """望遠鏡を(Az, El)に動かす"""
        self.ant.azel_move(az_arcsec, el_arcsec, az_rate, el_rate)    
        return
    
    def radec_move(self, ra, dec, code_mode, off_x = 0, off_y = 0, hosei = 'hosei_230.txt', offcoord = 'HORIZONTAL'):
        """望遠鏡を(Ra, Dec)に動かす"""
        self.ant.radec_move(ra, dec, code_mode, off_x, off_y, hosei, offcoord)
        return

    def galactic_move(self, l, b, off_x = 0, off_y = 0, hosei = 'hosei_230.txt', offcoord = 'HORIZONTAL'):
        """望遠鏡を(l, b)に動かす"""
        self.ant.galactic_move(l, b, off_x, off_y, hosei, offcoord)
        return

    def planet_move(self, number, off_x = 0, off_y = 0, hosei = 'hosei_230.txt', offcoord = 'HORIZONTAL'):
        """望遠鏡をplanetに動かす
        1.Mercury 2.Venus 3. 4.Mars 5.Jupiter 6.Saturn 7.Uranus 8.Neptune, 9.Pluto, 10.Moon, 11.Sun"""
        self.ant.planet_move(number, off_x, off_y, hosei, offcoord)
        return

    def tracking_end(self):
        """trackingの終了"""
        self.ant.tracking_end()
        return

    def clear_error(self):
        """errorのclear"""
        self.ant.clear_error()
        return

    def dome_open(self):
        """Domeのopen"""
        self.ant.dome_open()
        return

    def dome_close(self):
        """Domeのclose"""
        self.ant.dome_close()
        return

    def memb_open(self):
        """メンブレンのopen"""
        self.ant.memb_open()
        return

    def memb_close(self):
        """メンブレンのopenclose"""
        self.ant.memb_close()
        return

    def dome_move(self, dome_az):
        """Domeを(dome_az)に動作"""
        self.ant.dome_move(dome_az)
        return

    def dome_stop(self):
        """Domeのclose動作を停止"""
        self.dome_track_end()
        self.ant.dome_stop()
        return

    def dome_track(self):
        """Domeと望遠鏡のsync"""
        self.ant.dome_track()
        return

    def dome_track_end(self):
        """Domeと望遠鏡のsyncの終了"""
        self.ant.dome_track_end()
        return

    # for mirror
    
    def move_m4(self, position):
        """mirror4を動かす("in"or"out")"""
        if position == "in": self.beam.m4_in()
        elif position == "out": self.beam.m4_out()
        else : print('set m4position error')
        return
    
    def move_hot(self, position):
        """hotloadを動かす("in"or"out")"""
        if position == "in": self.beam.hot_in()
        elif position == "out": self.beam.hot_out()
        else : print('set hotposition error')
        return

    # for receiber

    def oneshot(self, repeat=1, exposure=1.0, stime=0.0):
        #分光計oneshotのcount値を配列で出力
        dfs01 = self.rx.oneshot_dfs01(repeat, exposure ,stime)
        dfs02 = self.rx.oneshot_dfs02(repeat, exposure ,stime)
        return {"dfs1":dfs01,
                "dfs2":dfs02}

    # for status

    def write_text(self, array, txtname):
        #データをtxtに書き込み
        f=open(txtname, 'a+')
        for x in array:
            f.write(str(x)+' ')
        f.write('\n')
        f.close()
        return 

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
        ant_status = self.status.read_antenna()
        beam_status = self.status.read_beam()
        # sg_status = self.doppler.get_status()
        ret = self.status.read_weather()
        
        if ant_status[1][0] & ant_status[1][1] == 1:
            drive_ready_az = 'ON'
        else:
            drive_ready_az = 'OFF'

        if ant_status[1][2] & ant_status[1][3] == 1:
            drive_ready_el = 'ON'
        else:
            drive_ready_el = 'OFF'

        if ant_status[1][24] == 1:
            emergency = 'ON'
        else:
            emergency = 'OFF'

        if ant_status[5][1][1] == 'OPEN' and ant_status[5][1][3] == 'OPEN':
            door_dome = 'OPEN'
        elif ant_status[5][1][1] == 'MOVE' or ant_status[5][1][3] == 'MOVE':
            door_dome = 'MOVE'
        elif ant_status[5][1][1] == 'CLOSE' and ant_status[5][1][3] == 'CLOSE':
            door_dome = 'CLOSE'
        else:
            door_dome = 'ERROR'

        status = { "Time" : timestamp,
                   "Limit" : ant_status[0],
                   "Current_Az" : ant_status[4][0]/3600.,
                   "Current_El" : ant_status[4][1]/3600.,
                   "Command_Az" : ant_status[3][2]/3600.,
                   "Command_El" : ant_status[3][3]/3600.,
                   "Deviation_Az" : ant_status[3][4],
                   "Deviation_El" : ant_status[3][5],
                   "Drive_ready_Az" : drive_ready_az,
                   "Drive_ready_El": drive_ready_el,
                   "Authority" : ant_status[2],
                   "Emergency" : emergency,
                   "Current_Dome" : ant_status[6],
                   "Door_Dome" : door_dome,
                   "Door_Membrane" : ant_status[5][2][1],
                   "Door_Authority" : ant_status[5][3],
                   "Current_M4" : beam_status[1],
                   "Current_Hot" : beam_status[0],
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
