# -*- coding: utf-8 -*-
"""
Created on Thu Feb 08 17:53:25 2018

@author: Unalmed
"""

#con este codigo descargo archivos fpt desde la consola 


for i in range (1979,2010):
    for j in ('01','02','03','04','05','06','07','08','09','10','11','12'):
        print ('ftp://polar.ncep.noaa.gov/pub/history/nopp-phase2/' +str(i) +j+'/gribs/multi_reanal.ecg_10m.hs.'+str(i)+ j+'.grb2')
        
        

            
        
        


