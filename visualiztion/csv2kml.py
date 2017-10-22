import numpy as np
import pandas as pd
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import pymap3d as pm
import os

'''
 mainDir - Dir where train/test data is
 data2WorkOn - Name of the data CSV file
 class2show - Which class in CSV file to draw, or (-1) if using test set or lines2show parameter
 lines2show - Which lines in CSV file to draw
 nedOrigin - Geo coordinates where XYZ = 0
 openFileWhenDone - Open KML after it is ready (KML files have to be associated with Google Earth)
'''

mainDir = 'D:\\DataHack2017\\'
#data2WorkOn = 'test'
data2WorkOn = 'train'
class2show = -1  #for 'train' only
lines2show = range(0,300) #for 'test' (or 'train if class2show == -1)
nedOrigin = (31.784491,35.214245,0)
openFileWhenDone = True


def addPlacemark(doc,name,folderName,lla_str,clr_str):
    doc.Document.Folder[folderName].append(
        KML.Placemark(
            KML.name(name),
            KML.Style(
                KML.LineStyle(
                    KML.color(clr_str),#"ff00FF40") ,
                    KML.width("4")
                )
            ),
            KML.LineString(
                KML.altitudeMode("absolute"),
                KML.coordinates(
                  lla_str
                )
            )
        )    
    )
    return doc

def ned2geodetic2String(csvSet,line):
    lla_str = ''
    for iii in range(0,15):
        northCoor = csvSet.iloc[line]['posX_'+str(iii)]
        eastCoor = csvSet.iloc[line]['posY_'+str(iii)]
        downCoor = -csvSet.iloc[line]['posZ_'+str(iii)]
        if np.isnan(northCoor):
            continue
        lla = pm.ned2geodetic(northCoor,eastCoor,downCoor,nedOrigin[0],nedOrigin[1],nedOrigin[2])
        lla_str = lla_str+str(lla[1])+","+str(lla[0])+","+str(lla[2])+" "
    return lla_str
    
name = 'Rocket_Data_Science'
if class2show > 0:
    name = name+'_'+str(class2show)
doc = KML.kml(
        KML.Document(
            KML.name(name),
            KML.Folder(
                KML.name('UP')
            ),
            KML.Folder(
                KML.name('DOWN')
            )
            
        )
    )
    
print 'Loading...'
csvSet = pd.read_csv(mainDir+data2WorkOn  + '.csv')

print 'Working...'
if data2WorkOn.find('train') and class2show > 0:
    csvSubSet = csvSet[csvSet.iloc[:]['class'] == class2show]
    lines2show = csvSubSet.index
for line in lines2show:
    lla_str = ned2geodetic2String(csvSet,line)
    velColor = hex(int(round(np.linalg.norm( ( csvSet.iloc[line]['velX_0']  ,  csvSet.iloc[line]['velY_0'] , csvSet.iloc[line]['velZ_0']  ) ) / 1500 * 255)))[-2:]    
    if csvSet.iloc[line]['velZ_0'] > 0:    
        clr_str = "FF"+velColor+"0000"
        folderName = 0
    else:
        clr_str = "FF0000"+velColor
        folderName = 1
    addPlacemark(doc,'line_'+str(line),folderName,lla_str,clr_str)

print 'Saving...'
#print etree.tostring(doc, pretty_print=True)
outfile = file(mainDir+name+'.kml','w')
outfile.write(etree.tostring(doc, pretty_print=True))

print 'Done!'
if openFileWhenDone:
    os.startfile(mainDir+name+'.kml')