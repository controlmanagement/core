#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
------------------------------------------------
[Detail Description]

    operator_skydip:
        role: sky_dip観測を実行する
    



------------------------------------------------
"""

import pylab
import time
import numpy
# import file_manager
import operator
import obs_param_modifier

class skydip(operator.operator):
    """
    skydip観測を行う
    
    [メソッド]
    _fit - 1次元フィッティング
    _plot - 図の出力
    start - 観測開始
    
    """
    def _fit(self, fits_params, obs_params):
        """
        1次元でフィッティングする
        """
        import numpy, scipy.optimize
        
        data = numpy.array([fitsp["DATA"] for fitsp in fits_params])
        rdata = numpy.array(numpy.sum(data[0]))
        offdata = numpy.array([numpy.sum(d) for d in data[1:]])
        
        hot_sky = numpy.log((rdata - offdata)/rdata)
        sec_el = 1./numpy.cos(numpy.radians(90. - numpy.array(obs_params["elevation"])))
        
        fitfunc = lambda p, x: p[0]*x + p[1]
        errfunc = lambda p, x, y: fitfunc(p, x) - y
        p0 = [1,1]
        p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(sec_el, hot_sky))
        fit = fitfunc(p1, sec_el)
        
        tau = -1 * p1[0]
        #分母が0に近いときは処理を中段させるか、tsysになにか別の値をいれておかないと、DBで弾かれる
        tsys = (offdata[-1] * fits_params[-1]["THOT"])/(rdata - offdata[-1]) #coefficient of determination
        r2 = 1 - sum((hot_sky - fit)**2) / sum((hot_sky - numpy.average(hot_sky))**2)
        
        return tau, tsys, r2, sec_el, fit, hot_sky

    def _plot(self, fits_params, tau, tsys, r2, sec_el, fit, hot_sky, path):
        """
        図の出力、保存
        """
        fig = pylab.figure()
        pylab.grid()
        pylab.ylabel("log((Phot-Psky)/Phot)")
        pylab.xlabel("secZ")
        
        pylab.plot(sec_el, hot_sky, "o", markersize = 7)
        pylab.plot(sec_el, fit)
        pylab.annotate("tau = %.2f, Tsys* = %.2f, R^2 = %.3f" %(tau, tsys,r2), xy = (0.6,0.9), xycoords = 'axes fraction', size = 'small')
        
        #if (fits_params[0]["BACKEND"])[-1]=="1" : direction="H"
        #elif (fits_params[0]["BACKEND"])[-1]=="2" : direction="V"
        #else : pass
        #figure_name = str(fits_params[0]["MOLECULE"])+direction+".png"
        figure_name = str(fits_params[0]["MOLECULE"])+".png"
        #file_manager.mkdir(path)
        pylab.savefig(path+figure_name)
        #file_manager.mkdir('/home/1.85m/data/Qlook/skydip/' + path.split('/')[-1])
        #pylab.savefig('/home/1.85m/data/Qlook/skydip/'+ path.split('/')[-1] + '/' + figure_name)
        
        """ 
        # Q look
        pylab.savefig('/home/1.85m/soft/monitor/uploader/fig_tmp/obs_skydip.png')
        pylab.close(fig)
        return

    def _qlook(self, data, fit):
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.grid()
        ax.set_title('Skydip :: %s'%(time.strftime('%Y/%m/%d %H:%M:%S')))
        ax.set_ylabel('log((Phot-Psky)/Phot)')
        ax.set_xlabel('secZ')
        color = {'12CO': 'b', '13CO': 'g', 'C18O': 'r'}
        style = {'H': '-', 'V': '--'}
        an_y = {'12COH': 0.96, '12COV': 0.92, '13COH': 0.88, '13COV': 0.84, 'C18OH': 0.80, 'C18OV': 0.76} 
        for i, (_d, _f) in enumerate(zip(data, fit)):
            tau, tsys, r2, sec_el, f, hot_sky = _f
            if (_d[0]['BACKEND'])[-1]=='1': pol = 'H'
            elif (_d[0]['BACKEND'])[-1]=='2': pol = 'V'
            mol = str(_d[0]['MOLECULE'])
            ax.plot(sec_el, hot_sky, 'o', markersize=7, color=color[mol])
            ax.plot(sec_el, f, color=color[mol], linestyle=style[pol])
            ax.annotate('%s(%s) : tau=%.2f, Tsys*=%.2f, R^2=%.3f' %(mol, pol, tau, tsys, r2), \
                            xy=(0.5, an_y[mol+pol]), xycoords='axes fraction',  size='x-small')
            continue
        ax.set_xlim(0.5, 3.5)
        fig.savefig('/home/1.85m/soft/monitor/uploader/fig_tmp/obs_skydip.png')
        pylab.close(fig)
        return
    """

    def start(self, params):
        """
        skydip観測を行う
        
        [引数]
        params - 観測パラメータ。managerが設定する。
        
        [返り値]
        各ラインの、
        tau - τ
        tsys - Tsys
        r2 - フィッティング精度
        """
        import time
        
        params['tau'] = {'1':0.0, '2':0.0}
        params['beameff'] = {'1':0.0, '2':0.0}
                             
        #try:
        elevation = params["elevation"]
        exposure = params["exposure"]
        #observer = self.db_observer.get()
        #params["observer"] = observer
        path = "/home/amigos/maruyama/NECST_n/skydip"
            
        data = []
        condition = []

        ##self.ctrl.intialize_observation()
        
        con = self.ctrl.get_status()
        
        #azimuth = con["az"]
        azimuth = 0
        el = 0

        #--- get R data ---
        ##self.ctrl.move_hotload("r")
        print(azimuth, elevation[0])
        ##self.ctrl.move_anntena(azimuth, elevation[0], "HORIZONTAL", 0., 0., 0., "SAME")
        #vobsr, vidffr, fdiffr = self.ctrl.callibrate_doppler(azimuth, elevation[0], "HORIZONTAL")
        tmp_data = self.ctrl.oneshot(exposure=exposure)
        tmp_condition = self.ctrl.get_status()
        tmp_condition["mode"] = "HOT"
        tmp_condition["az"] = azimuth
        tmp_condition["el"] = el
        #tmp_condition["vobs"] = vobsr
        condition.append(tmp_condition)
        data.append(tmp_data)
        
        r_timestamp = time.time()
        
        for el in elevation:
            # --- get OFF data ---
            ##self.ctrl.move_hotload("sky")
            ##self.ctrl.move_anntenna(azimuth, el, "HORIZONTAL", 0., 0., 0., "SAME")
            tmp_data = self.ctrl.oneshot(exposure=exposure)
            tmp_condition = self.ctrl.get_status()
            tmp_condition["mode"] = "OFF"
            tmp_condition["az"] = azimuth
            tmp_condition["el"] = el
            condition.append(tmp_condition)
            data.append(tmp_data)
            continue
        
        ##self.ctrl.finalize()
        
        start_timestamp = time.strftime("%Y%m%d-%H.%M.%S" ,time.localtime(condition[0]["timestamp"]))
        print(data)
        print(condition)
        fits_params_dic = obs_param_modifier.modify_skydip(params, data, condition)
        fits_params_list = [fits_params_dic[key] for key in fits_params_dic.keys()]

        ret = [self._fit(fitsp, params) for fitsp in fits_params_list] # tau, tsys*, R2 の算出
        print(ret)
        [self._plot(fitsp, _r[0], _r[1], _r[2], _r[3], _r[4], _r[5], path+'/'+start_timestamp) for fitsp, _r in zip(fits_params_list, ret)] #図の生成、保存
        #self._qlook(fits_params_list, ret)
        
        tau = [row[0] for row in ret]
        tsys = [row[1] for row in ret]
        r2 = [row[2] for row in ret]
        db_items = [azimuth] + tau +tsys + r2 + [path+'/'+start_timestamp+'/']
        print(db_items)
        #obs_id = self.fm.insert_record("skydip", db_items)

        """
        except operator.PllError:
            self.ctrl.finalize()
            #DBのアップデート
            start_timestamp = time.strftime('%Y%m%d-%H.%M.%S' ,time.localtime(condition[0]['timestamp']))
            self.fm.update_record('skydip', obs_id, 'error', 'PllError')

            #fitsを途中生成
            #fits_params = self.modifier.modify_skydip(params, data, condition)
            fits_params_dic = obs_param_modifier.modify_skydip(params, data, condition)
            self.fm.save_fits(fits_params, params['path']+'/'+start_timestamp+'_error'+'/')

            raise operator.OperatorError #managerクラスにあるexceptが捕捉。

        except KeyboardInterrupt:
            self.ctrl.finalize()
            #DBのアップデート
            start_timestamp = time.strftime('%Y%m%d-%H.%M.%S' ,time.localtime(condition[0]['timestamp']))
            self.fm.update_record('skydip', obs_id, 'error', 'KeyboardInterrupt')

            # fitsを途中生成
            #fits_params = self.modifier.modify_skydip(params, data, condition)
            fits_params_dic = obs_param_modifier.modify_skydip(params, data, condition)
            self.fm.save_fits(fits_params, params['path']+'/'+start_timestamp+'_error'+'/')

            raise KeyboardInterrupt
        """

        dictdict = [dict(zip(['tau','tsys','r2'], _ret)) for _ret in ret]
        #return obs_id, dict(zip(['12', '13'], dictdict))
        return dict(zip(['12', '13'], dictdict))
