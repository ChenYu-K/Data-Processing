# -*- coding: mbcs -*-
##↓座標合わせ（詳細はよくわからない）
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
#↓初めにインポートするコード
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior                            
import odbAccess

####################################################################################
odb_name="PCagouseiketa"
odb_path="G:\\sugimoto\\Tips_odb\\asano"
data_path="G:\\sugimoto\\Tips_odb\\asano\\data"

m_size_web=float(20)
m_size_con=float(20)
height_web=float(1000)
width_con=float(900)

###################################################################################

##odbファイルを開く
odb=session.openOdb(str(odb_path)+'\\'+str(odb_name)+'.odb')
step1=odb.steps["Step-1"]
kk=step1.historyRegions.keys()
####################################################################################

#モデルをビューポートに投影
session.viewports['Viewport: 1'].setValues(displayedObject=odb)
####################################################################################

#メッシュサイズは20mm
#ウェブ幅は1000mm
#支点部の座標は(0,-140,6400)

#webのpathの作成
path_2400_web=[]
path_1500_web=[]

for i in range(int(height_web/m_size_web)+1):
    path_2400_web.append((0,-140+float(i*m_size_web),6400-2400))
    path_1500_web.append((0,-140+float(i*m_size_web),6400-1500))

session.Path(name="web_2400",type=POINT_LIST,expression=(path_2400_web))
session.Path(name="web_1500",type=POINT_LIST,expression=(path_1500_web))

#コンクリートのpath
path_2400_con=[]
for i in range(int(width_con/m_size_con)+1):
    path_2400_con.append((float(i*m_size_con)-450,1105,6400-2400))

session.Path(name="con_2400",type=POINT_LIST,expression=(path_2400_con))







