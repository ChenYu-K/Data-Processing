def restraint():
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
    a1='A'
    a2='Nut'
    b1='P'
    b2='Ws'
    c=2
    while(c<21):
        d1=a1+str(c)+a2
        d2=a1+str(c)+b2
        e1=b1+str(c)+a2
        e2=b1+str(c)+b2
        f1=a1+str(c)
        f2=b1+str(c)
        c+=1
        a = mdb.models['Model-1'].rootAssembly
        region1=a.surfaces[d1]
        a = mdb.models['Model-1'].rootAssembly
        region2=a.surfaces[d2]
        mdb.models['Model-1'].constraints[f1].setValues(master=region1, 
            slave=region2)
        a = mdb.models['Model-1'].rootAssembly
        region1=a.surfaces[e1]
        a = mdb.models['Model-1'].rootAssembly
        region2=a.surfaces[e2]
        mdb.models['Model-1'].constraints[f2].setValues(master=region1, 
            slave=region2)
