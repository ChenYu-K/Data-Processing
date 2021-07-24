# -*- coding: mbcs -*-
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
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
import csv
import pprint

##data of beam~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
data_path='D:\\sugimoto\\tips\\data'
odb_path='D:\\sugimoto\\tips\\check'
this_path='D:\\sugimoto\\tips'
total_case_number=int(2)
for case_number in range(total_case_number):#code to handle multiple cases in the future
    with open(str(this_path)+'/case.csv') as f:
        reader=csv.reader(f)
        l = [row for row in reader]
        b_height=float(l[case_number+1][1])#height mm
        b_width=float(l[case_number+1][2])#width mm
        f_thickness=float(l[case_number+1][4])#thickness of flange
        w_thickness=float(l[case_number+1][3])#thickness of web
    span_length=float(6000)#span mm
    b_load=fload=float(100)#Load N
    model_type=int(1)#1:solid, 2:shell, 3:wire
    #variables depending on the model type
    if model_type==1:#solid
        element_size=int(20)#size of element
        div_ele_thic=int(3)#the number of element division in thickness direction 
    elif model_type==2:#shell
        #Please define variables needed to your model.
        element_size=int(20)
    elif model_type==3:#wire
        #Please define variables needed to your model.
        element_size=int(50)
    ##data of beam~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##create models and submit jobs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    myModel=mdb.Model(modelType=STANDARD_EXPLICIT, name='case'+str(case_number+1))#create a model
    #material======
    myMaterial=myModel.Material(name='steel')
    myMaterial.Elastic(table=((float(200000.0), float(0.3)), ))
    #solid
    myModel.HomogeneousSolidSection(material='steel', name='solid', thickness=None)    
    #shell web
    myModel.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='steel', name='shell web', numIntPts=5, 
        poissonDefinition=DEFAULT, preIntegrate=OFF, temperature=GRADIENT, 
        thickness=w_thickness, thicknessField='', thicknessModulus=None, thicknessType=
        UNIFORM, useDensity=OFF)    
    #shell flange
    myModel.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='steel', name='shell flange', numIntPts=5, 
        poissonDefinition=DEFAULT, preIntegrate=OFF, temperature=GRADIENT, 
        thickness=f_thickness, thicknessField='', thicknessModulus=None, thicknessType=
        UNIFORM, useDensity=OFF)      
    #wire
    myModel.IProfile(b1=b_width, b2=b_width, h=b_height, l=b_height/2, name=
        'beam-cross-section', t1=f_thickness, t2=f_thickness, t3=w_thickness) 
    myModel.BeamSection(consistentMassMatrix=False, integration=
        DURING_ANALYSIS, material='steel', name='wire', poissonRatio=0.0, 
        profile='beam-cross-section', temperatureVar=LINEAR)
    #material======

    #part=====
    mySketch=myModel.ConstrainedSketch(name='beam', sheetSize=4000.0)
    if model_type==1:

        xyCoords=(
            (0,0),
            (b_width/2,0),
            (b_width/2,f_thickness),
            (w_thickness/2,f_thickness),
            (w_thickness/2,b_height-f_thickness),
            (b_width/2,b_height-f_thickness),            
            (b_width/2,b_height),  
            (0,b_height),  
            (-b_width/2,b_height), 
            (-b_width/2,b_height-f_thickness),  
            (-w_thickness/2,b_height-f_thickness),
            (-w_thickness/2,f_thickness),
            (-b_width/2,f_thickness), 
            (-b_width/2,0), 
            (0,0),          
            )
        for ii in range(len(xyCoords)-1):
            mySketch.Line(point1=xyCoords[ii],point2=xyCoords[ii+1])        
        
        myPart=myModel.Part(dimensionality=THREE_D, name='beam', type=DEFORMABLE_BODY)
        myPart.BaseSolidExtrude(depth=span_length, sketch=mySketch)        

        myPart.SectionAssignment(offset=0.0, 
            offsetField='', offsetType=MIDDLE_SURFACE,
            region=Region(
            cells=myPart.cells.getSequenceFromMask(mask=('[#1 ]', ), )),
            sectionName='solid', thicknessAssignment=FROM_SECTION
            )

        myPart.PartitionCellByPlanePointNormal(
            cells=myPart.cells.findAt((
            (1, 1, 1), 
            )),
            normal=myPart.edges.findAt(
            (w_thickness/2,f_thickness+1,0),
            ),
            point=(w_thickness/2,f_thickness,0)
            )

        myPart.PartitionCellByPlanePointNormal(
            cells=myPart.cells.findAt((
            (1, f_thickness+1, 1), 
            )),
            normal=myPart.edges.findAt(
            (w_thickness/2,f_thickness+1,0),
            ),
            point=(w_thickness/2,b_height-f_thickness,0)
            )

        total_cell=[]
        for iii in range(len(myPart.cells)):
            total_cell.append(myPart.cells[iii])
        myPart.PartitionCellByPlanePointNormal(
            cells=total_cell,
            normal=myPart.edges.findAt(
            (w_thickness/2+1,f_thickness,0),
            ),
            point=(w_thickness/2,f_thickness,0)
            )

        total_cell=[]
        for iii in range(len(myPart.cells)):
            total_cell.append(myPart.cells[iii])
        myPart.PartitionCellByPlanePointNormal(
            cells=total_cell,
            normal=myPart.edges.findAt(
            (-w_thickness/2-1,f_thickness,0),
            ),
            point=(-w_thickness/2,f_thickness,0)
            )

        total_cell=[]
        for iii in range(len(myPart.cells)):
            total_cell.append(myPart.cells[iii])
        myPart.PartitionCellByPlanePointNormal(
            cells=total_cell,
            normal=myPart.edges.findAt(
            (-b_width/2,f_thickness,span_length/2),
            ),
            point=(-b_width/2,f_thickness,span_length/2)
            )

        total_cell=[]
        for iii in range(len(myPart.cells)):
            total_cell.append(myPart.cells[iii])
        myPart.PartitionCellByPlanePointNormal(
            cells=total_cell,
            normal=myPart.edges.findAt(
            (-w_thickness/4,f_thickness,0),
            ),
            point=(0,f_thickness,0)
            )

        myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=element_size)

        myPart.generateMesh()

    elif model_type==2:
        mySketch.Line(point1=(-b_width/2, f_thickness), point2=(b_width/2, f_thickness))
        mySketch.Line(point1=(0, f_thickness), point2=(0, b_height-f_thickness))
        mySketch.Line(point1=(-b_width/2, b_height-f_thickness), point2=(b_width/2, b_height-f_thickness))

        myPart=myModel.Part(dimensionality=THREE_D, name='beam', type=DEFORMABLE_BODY)
        myPart.BaseShellExtrude(depth=span_length, sketch=mySketch)  

        myPart.SectionAssignment(offset=0.0, offsetField='', 
            offsetType=BOTTOM_SURFACE, region=Region(
            faces=myPart.faces.findAt((
            (-b_width/4, b_height-f_thickness, span_length/2),(0.0, -1.0, 0.0)),
            ((b_width/4, b_height-f_thickness, span_length/2), (0.0, -1.0, 0.0)), )
            ), sectionName='shell flange', thicknessAssignment=FROM_SECTION)        

        myPart.SectionAssignment(offset=0.0, offsetField='', 
            offsetType=MIDDLE_SURFACE, region=Region(
            faces=myPart.faces.findAt(
            ((0, b_height/2, span_length/2), (1.0, 0.0, 0.0)), )
            ), sectionName='shell web', 
            thicknessAssignment=FROM_SECTION)

        myPart.SectionAssignment(offset=0.0, offsetField='', 
            offsetType=TOP_SURFACE, region=Region(
            faces=myPart.faces.findAt((
            (-b_width/4, f_thickness, span_length/2),(0.0, -1.0, 0.0)),
            ((b_width/4, f_thickness, span_length/2), (0.0, -1.0, 0.0)), )
            ), sectionName='shell flange', thicknessAssignment=FROM_SECTION)   

        myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=element_size)

        myPart.generateMesh()

    elif model_type==3:
        mySketch.Line(point1=(-span_length/2, 0), point2=(span_length/2, 0))
        
        myPart=myModel.Part(dimensionality=THREE_D, name='beam', type=DEFORMABLE_BODY)
        myPart.BaseWire(sketch=mySketch)

        myPart.assignBeamSectionOrientation(method=
            N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
            edges=myPart.edges.findAt((
            (-1500.0, 0.0, 0.0), 
            ), )))

        myPart.SectionAssignment(offset=0.0, offsetField='', 
            offsetType=MIDDLE_SURFACE, region=Region(
            edges=myPart.edges.findAt(((-10, 0.0, 0.0), 
            ), )), sectionName='wire', thicknessAssignment=FROM_SECTION)

        #partition at center point
        myPart.PartitionEdgeByPoint(edge=
            myPart.edges.findAt((10, 0.0, 0.0), ), 
            point=myPart.InterestingPoint(
            myPart.edges.findAt((10, 0.0, 0.0), ), MIDDLE))        

        myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=element_size)

        myPart.generateMesh()

    del mySketch   
    #part=====
    #assembly=====
    myAssembly=myModel.rootAssembly
    #myInstance=myAssembly.Instance(dependent=ON, name='beam-1', part=myPart)
    myInstance=myModel.rootAssembly.Instance(dependent=ON, name='beam-1', part=myPart)

    myModel.StaticStep(initialInc=0.1, maxInc=0.1, name='Step-1', nlgeom=ON, previous='Initial')
    
    if model_type==1:
        myAssembly.Set(name='Load', vertices=myInstance.vertices.findAt(((0, b_height, span_length/2), )))

        myAssembly.Set(edges=
            myInstance.edges.findAt(
            ((-b_width/2+1, 0.0, span_length), ), 
            ((-w_thickness/2+1, 0.0, span_length), ), 
            ((w_thickness/2-1, 0.0, span_length), ), 
            ((b_width/2-1, 0.0, span_length), ),
            ), name='Fix')

        myAssembly.Set(edges=
            myInstance.edges.findAt(
            ((-b_width/2+1, 0.0, 0), ), 
            ((-w_thickness/2+1, 0.0, 0), ), 
            ((w_thickness/2-1, 0.0, 0), ), 
            ((b_width/2-1, 0.0, 0), ),
            ), name='Mov')

        myModel.HistoryOutputRequest(createStepName='Step-1', name='force-1', rebar=EXCLUDE, region=
            myAssembly.sets['Fix'], sectionPoints=DEFAULT, variables=('RF2', ))
        myModel.HistoryOutputRequest(createStepName='Step-1', name='force-2', rebar=EXCLUDE, region=
            myAssembly.sets['Mov'], sectionPoints=DEFAULT, variables=('RF2', ))
        myModel.HistoryOutputRequest(createStepName='Step-1', name='displacement', rebar=EXCLUDE, region=
            myAssembly.sets['Load'], sectionPoints=DEFAULT, variables=('U2', ))

    elif  model_type==2:
        aa=1
        #ここ！！
    elif  model_type==3:
        aa=1
        #ここ！！
    #assembly=====
    #boundary and load conditions=====
    if model_type==1:
        myModel.DisplacementBC(amplitude=UNSET, createStepName='Initial', 
            distributionType=UNIFORM, fieldName='', localCsys=None, name='fix', region=
            myAssembly.sets['Fix'], u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
        myModel.DisplacementBC(amplitude=UNSET, createStepName='Initial', 
            distributionType=UNIFORM, fieldName='', localCsys=None, name='mov', region=
            myAssembly.sets['Mov'], u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
        myModel.ConcentratedForce(cf2=-b_load, createStepName='Step-1', 
            distributionType=UNIFORM, field='', localCsys=None, name='Load-1', region=
            myAssembly.sets['Load'])
    elif  model_type==2:
        aa=1
        #ここ！！
    elif  model_type==3:
        aa=1
        #ここ！！

    #boundary and load conditions=====
    #subbit a job=====
    myJob=mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model=myModel, modelPrint=OFF, 
        multiprocessingMode=DEFAULT,name='case'+str(case_number+1),
        nodalOutputPrecision=SINGLE, 
        numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
        ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    #myJob.submit(consistencyChecking=OFF)
    myJob.submit(consistencyChecking=OFF, datacheckJob=True)
    myJob.waitForCompletion() 

    #subbit a job=====
##create models and submit jobs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


