
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
import numpy as np
import pandas as pd

grib='multi_reanal.ecg_10m.hs.197901.grb2';
grbs=pygrib.open(grib)
grb = grbs.select(name='Significant height of combined wind waves and swell')

##############get the latitudes and longitudes of the grid:######################

lat,lon = grb[0].latlons()
lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max()

###################se recorta lat y lon para el punto 1##########################

lat1=np.where(lat==12.9999160000004)
lon1=np.where(lon==278.83333333333547)
##grb.keys()  ##para ver las variables que trae el archivo por ejemplo 'name', 'level', 'forecastTime'
#por ejemplo para buscar una hora determinada >> time = grbs.select(forecastTime=744)

############Ciclo para leer todos los datos y el tiempo########################


tiempo=[]
meses=['01','02','03','04','05','06','07','08','09',10,11,12]
for i in range(1979,2010):
	for j in meses:
		tiempo.append(int(str(i)+str(j)))



Time=[]

for Fechas in tiempo:
    
	grib='multi_reanal.ecg_10m.hs.'+str(Fechas)+'.grb2';
	grbs=pygrib.open(grib)
	grb = grbs.select(name='Significant height of combined wind waves and swell')
	

	for j in range(0,len(grb)): 
		data=grb[j].values # The data is returned as a numpy array, or if missing values or a bitmap are present, a 						numpy masked array
		data=np.array(data)
		MatrizA=data[np.newaxis,:]
		hours=grb[j]['forecastTime']
		
		if Fechas == 197901:
			Time.append(hours)
		elif j ==0:
			Time.append(Time[-1])
		else:
			Time.append(Time[-1]+3)

		if j==0:
			DatosGrib=MatrizA
		else:
			DatosGrib=np.concatenate([DatosGrib,MatrizA])
		Punto1=DatosGrib[:,lat1[0][0],lon1[1][0]]


		
	if Fechas == 197901:
        
        	WWW3data = Punto1
           
    	else:
        
      	 	WWW3data = np.concatenate([WWW3data,Punto1])



fecha = np.array([datetime.datetime(1979,01,01,0000)+\
datetime.timedelta(hours = Time[i]) for i in range(len(Time))])


############extract data and get lat/lon values for a subset over SAI:###########
#dataSAI, latsSAI, lonsSAI = grb.data(lat1=11,lat2=13,lon1=278,lon2=281)
#dataSAI.shape, latsSAI.min(), latsSAI.max(), lonsSAI.min(), lonsSAI.max()



#ciclo anual con pandas

Waves=pd.Series(index=fecha[-1], data=WWW3data[-1])

WavesM=Waves.resample('M').mean()
WavesD=Waves.resample('D').mean()

WM=np.array(WavesM)
WM=np.reshape(WM,(-1,12))
WMM=np.mean(WM,axis=0)
WMS=np.std(WM, axis=0)

plt.plot(WMM)



CicloAnual= np.zeros([12]) * np.NaN

Meses = np.array([fecha[i].month for i in range(len(fecha))])
for k in range(1,13):
    tmpp = np.where(Meses == k)[0]
   
    tmp= WWW3data[tmpp]
    CicloAnual[k-1]= np.mean(tmp)





    




##plot#####
plt.figure()

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
  urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
  resolution='c')

x, y = m(lon,lat)

cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])


plt.colorbar(cs,orientation='vertical')
plt.title('Example 2: NWW3 Significant Wave Height from GRiB')
plt.show()



