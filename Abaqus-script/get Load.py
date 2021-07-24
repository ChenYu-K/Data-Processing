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
odb_name="brb-45-pol-hippari"
odb_path="D:\\sugimoto\\Tips_odb\\nakamoto"
data_path="D:\\sugimoto\\Tips_odb\\nakamoto\\data"
image_path="D:\\sugimoto\\Tips_odb\\nakamoto\\image"
###################################################################################

##odbファイルを開く
odb=session.openOdb(str(odb_path)+'\\'+str(odb_name)+'.odb')
step1=odb.steps["Step-2"]
kk=step1.historyRegions.keys()
######################################################################################
#CFN2の取り出し
#CFS1は同じ方法で取り出せます。
xy_result = session.XYDataFromHistory(
    name='CFN2_R-BOBAN-1_BBOB-TEN', 
    odb=odb, 
    outputVariableName='CFN2: CFN2     ASSEMBLY_TEN-BOB/ASSEMBLY_R-BOBAN-1_BBOB-TEN', 
    steps=('Step-1', 'Step-2', ), __linkedVpName__='Viewport: 1')
#↓ここからはXYデータをテキストデータで出力するコード　コピペで大丈夫
aa=session.xyDataObjects.keys()
aa_temp=[s for s in aa if "temp" in s]
for te_num in range(len(aa_temp)):
    del session.xyDataObjects[aa_temp[te_num]]
##csvファイルへ保存
aa=session.xyDataObjects.keys()
aa_x_data=[]
for i_num in range(len(aa)):
    x=session.xyDataObjects[aa[i_num]]
    aa_x_data.append(x)
session.writeXYReport(
    fileName=str(data_path)+'\\CFN2_R-BOBAN-1_BBOB-TEN.csv', 
    xyData=(aa_x_data))
##削除
#for i_num in range(len(aa)):
del session.xyDataObjects[aa[i_num]]  
######################################################################################

######################################################################################
#RF1のデータ取り出し
# RF1, RF2, U1, U2中本君頑張ってください。
xy_tuple_load=[]
kk=step1.historyRegions.keys()
for tt in range(len(kk)):
    if "Node" in kk[tt]:
        if "R-BOBAN-1" in kk[tt]:
            new_kk=kk[tt].replace("Node ","").replace("."," Node ")
            try:
                xy = xyPlot.XYDataFromHistory(odb=odb, 
                    outputVariableName='Reaction force: RF1 PI: '+ str(new_kk), 
                    steps=('Step-1', 'Step-2', ),
                    suppressQuery=True) 
            except XypError:
                print("e")
            else:
                xy_tuple_load.append(xy) 

xy_sum = sum(xy_tuple_load)
session.XYData(name='load', objectToCopy=xy_sum ) 
#↓ここからはXYデータをテキストデータで出力するコード　コピペで大丈夫
aa=session.xyDataObjects.keys()
aa_temp=[s for s in aa if "temp" in s]
for te_num in range(len(aa_temp)):
    del session.xyDataObjects[aa_temp[te_num]]
##csvファイルへ保存
aa=session.xyDataObjects.keys()
aa_x_data=[]
for i_num in range(len(aa)):
    x=session.xyDataObjects[aa[i_num]]
    aa_x_data.append(x)
session.writeXYReport(
    fileName=str(data_path)+'\\LOAD.csv', 
    xyData=(aa_x_data))
##削除
#for i_num in range(len(aa)):
del session.xyDataObjects[aa[i_num]]  
######################################################################################

######################################################################################
session.viewports['Viewport: 1'].setValues(displayedObject=odb)
session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
leaf = dgo.LeafFromPartInstance(partInstanceName=("R-BOBAN-1", ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].view.setValues(session.views['Bottom'])
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Step-2')
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='CPRESS', outputPosition=ELEMENT_NODAL, )
session.viewports['Viewport: 1'].odbDisplay.display.setValues(
    plotState=CONTOURS_ON_DEF)
session.printToFile(fileName=str(image_path)+"\\"+str(odb_name), format=PNG, canvasObjects=(
    session.viewports['Viewport: 1'], ))
######################################################################################


odb.close()
