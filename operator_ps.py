import time

import operator

class ps(operator.operator):
	"""
    Position Switch観測を行うクラス

    [メソッド]
      start - 観測開始
    """
    def start(self, params):
        """
        Position Switch観測を開始する

        [引数]
          params - 観測パラメータ。QueueもしくはSSで設定される。
        """
        p = lambda key: params.get(key.lower(), operator.DEFAULT_PARAMS[key.lower()])
        status = 'successfully'
        stime = time.localtime()
        path = p('path')
        stime_path = time.strftime
        file_path = path+'/'+stime_path+'/'
        file1 = file_path+'IF1_'+stime_path+'.log'
        file2 = file_path+'IF2_'+stime_path+'.log'

        # Configure Parameters
        #========================
        print('(operator) loading parameters...')
        #  Target Parameters
        # --------------------
        object = p('object')
        on_x = p('on_x')
        on_y = p('on_y')
        on_coord = p('on_coord')
        off_name = p('off_name')
        #offlist = self.off.get(off_name)
        #off_x = float(offlist['x'])
        #off_y = float(offlist['y'])
        #off_coord = offlist['coord']
        off_x = p('off_x')
        off_y = p('off_y')
        off_coord = p('off_coord')
        offset_on_x = p('offset_on_x')
        offset_on_y = p('offset_on_y')
        offset_on_dcos = p('offset_on_dcos')
        offset_on_coord = p('offset_on_coord')
        offset_off_x = p('offset_on_x')
        offset_off_y = p('offset_on_y')
        offset_off_dcos = p('offset_on_dcos')
        offset_off_coord = p('offset_on_coord')

        print('(target) %s (%s:%.3f,%.3f) off:%s'%(object,on_coord,on_x,on_y,off_name))

        params['off_x'] = off_x
        params['off_y'] = off_y
        params['off_coord'] = off_coord
        #params['observer'] = self.db_observer.get()
        #observer = params['observer']

        #  Observation Parameters
        # -------------------------
        repeat = p('repeat')
        exposure = p('exposure')
        r_interval = p('r_interval')
        hosei = p('hosei')

        #self.fm.add_log('(observation)'+'repeat:%d exposure:%.1f Rinterval:%.1f'%(repeat, exposure, r_interval))

        #  Configure Database
        # ----------------------
        # DBへパラメータ保存

        # Configure Arguments
        #======================
        #  OFF Position
        # ---------------
        #off_position = (off_x, off_y, off_coord, offset_off_x, offset_off_y, offset_off_dcos, offset_off_coord)
        off_position = (off_x, off_y, off_coord, offset_off_x, offset_off_y, hosei, offset_off_coord)
        args_off_position = off_position
        #args_off_position = off_position + (planet, )
        #args_off_doppler = off_position + (vlsr, )

        #  ON Position
        # ---------------
        #on_position = (on_x, on_y, on_coord, offset_on_x, offset_on_y, offset_on_dcos, offset_on_coord)
        on_position = (on_x, on_y, on_coord, offset_on_x, offset_on_y, hosei, offset_on_coord)
        args_on_position = on_position
        #args_on_position = on_position + (planet, )
        #args_on_doppler = on_position + (vlsr, )

        #  Others
        # ---------------
        off_to_on_time = exposure
        hotload_keeper = operator.timekeeper(r_interval)
        data = []
        condition = []

        #
        # Initialize Observation
        #=========================
        print('(operator) initializing telescope...')

        #  System Initialize 
        # --------------------
        #self.ctrl.initialize_observation()
        self.ctrl.move_m4('in')
        self.ctrl.dome_track()

        #  Status Check
        # --------------
        status = self.ctrl.read_status()
        thot = status['CabinTemp1']
        self.ctrl.write_text(thot, file1)
        self.ctrl.write_text(thot, file2)

        # Observation Start
        #====================
        print('(operator) Observation START ----')
        
        #  Observe First HOT Data
        # -------------------------
        print('(operator) <<<<<< HOT >>>>>>')
        hotload_keeper.check()
        self.ctrl.move_hot('in')
        print('(antenna) moving...')
        self.ctrl.move_radec(*args_off_position)
        _d = self.ctrl.oneshot(1, exposure)
        self.ctrl.write_text(_d['dfs1'][0], file1)
        self.ctrl.write_text(_d['dfs2'][0], file2)

        # (Start) Position Switching Loop
        # ---------------------------------
        for count in range(repeat):
            #  Status Check
            # ----------------
            #self.ctrl.check_condition() 

            #  Observe HOT Data
            # -------------------
            if hotload_keeper.check():
                print('(operator) <<<<<< HOT >>>>>>')
                self.ctrl.move_hot('in')
                print('(antenna) moving...')
                self.ctrl.move_radec(*args_off_position)
                _d = self.ctrl.oneshot(1, exposure)
                self.ctrl.write_text(_d['dfs1'][0], file1)
                self.ctrl.write_text(_d['dfs2'][0], file2)
            else: pass

            #  Observe OFF Data
            # -------------------
            print('(operator) <<<<<< OFF >>>>>>')
            self.ctrl.move_hot('out')
            print('(antenna) moving...')
            self.ctrl.move_radec(*args_off_position)
            _d = self.ctrl.oneshot(1, exposure)
            self.ctrl.write_text(_d['dfs1'][0], file1)
            self.ctrl.write_text(_d['dfs2'][0], file2)

            #  Observe ON Data
            # ------------------
            self.fm.add_log('(operator) <<<<<< ON >>>>>>')
            self.ctrl.move_hot('out')
            print('(antenna) moving...')
            self.ctrl.move_radec(*args_on_position)
            _d = self.ctrl.oneshot(1, exposure)
            self.ctrl.write_text(_d['dfs1'][0], file1)
            self.ctrl.write_text(_d['dfs2'][0], file2)

            #  (End) Position Switching Loop
            # --------------------------------
            continue

        #
        # Error Trap
        #=============

        #
        # Finalize
        #===========
        print('(operator) observation END')
        print('(operator) finalizing...')
        self.ctrl.tracking_end()
        self.dome_track_end()

        #  Configure Parameters
        # -----------------------

        #  Write Observation Log to Database
        # ------------------------------------

        #  Save FITS file
        # -----------------

        # Error Trap
        #=============

        # (End) Position Switching Observation
        #=======================================
        print('(operater) operation END ----')
        return file_path




