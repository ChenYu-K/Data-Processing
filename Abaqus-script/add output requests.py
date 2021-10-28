# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def rireki():
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
    a='A'
    b='P'
    c=1
    while(c<21):
        d=a+str(c)
        e=b+str(c)
        c=c+1
        mdb.models['Model-1'].HistoryOutputRequest(name=d, createStepName='Step-1', 
            variables=('SOF', ), integratedOutputSection=d, 
            sectionPoints=DEFAULT, rebar=EXCLUDE)
        mdb.models['Model-1'].HistoryOutputRequest(name=e, createStepName='Step-1', 
            variables=('SOF', ), integratedOutputSection=e, 
            sectionPoints=DEFAULT, rebar=EXCLUDE)


