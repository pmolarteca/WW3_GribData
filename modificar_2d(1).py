                                                           
#!/usr/bin/python

import pygrib
import numpy as np
import os


# ============================================================= Directorios y otras cosas =================================

ruta0 = '/home/mzapata/twrf/pros/'
ruta2 = '/home/mzapata/twrf/base/2D/'
ruta1 = '/home/mzapata/twrf/ceros/'
ruta3 = '/home/mzapata/twrf/luisa/2D/'

nam = np.loadtxt(ruta0+'var_2d.txt',delimiter=',',usecols=(0,),dtype='str') 
poi = np.loadtxt(ruta0+'var_2d.txt',delimiter=',',usecols=(1,),dtype='int')

hh = ['00','06','12','18']
mm = ['11']
dd = ['01','02','03','04','05','06','07','08','09','10','11']



for j in range(len(mm)):
        for k in range(len(dd)):
                for h in range(len(hh)):
                                anom = np.loadtxt(ruta1+'1999-'+mm[j]+'-'+dd[k]+'_'+hh[h]+'.txt',dtype='float')
                                anom[120:129,209:222] = anom[120:129,209:222] + 272.15
                                for i in range(len(poi)):
                                        grbs = pygrib.open(ruta2+'ei.oper.an.sfc.regn128sc.1999'+mm[j]+dd[k]+hh[h])
                                        grb = grbs.select(indicatorOfParameter=poi[i])[0]
                                        if poi[i]==34:
                                                var = np.copy(grb.values)
                                                var[120:129,209:222] = anom[120:129,209:222]
                                        if poi[i]!=34:
                                                var = grb.values
                                        grbs.close()
                                        grbs = pygrib.open(ruta2+'ei.oper.an.sfc.regn128sc.1999'+mm[j]+dd[k]+hh[h])
                                        grb = grbs.select(indicatorOfParameter=poi[i])[0]
                                        grb.values = var
                                        if poi[i] == 151 or poi[i]==34 or poi[i]==134:
                                                grb.level = 0
                                        grb.dataDate = int('1999'+mm[j]+dd[k])
                                        grb.hour = int(hh[h])
                                        grb.minute = int(0)
                                        grb.second = int(0)
                                        grb.month = int(mm[j])
                                        grb.day = int(dd[k])
                                        msg = grb.tostring()
                                        grbs.close()
                                        name = str(ruta3+'luisa'+'-SFC_1999'+mm[j]+dd[k]+hh[h]+'.grb')
                                        grbout = open(name,'ab+')
                                        grbout.write(msg)
                                        grbout.close()

                                print '1999-'+mm[j]+'-'+dd[k]+'_'+hh[h]


