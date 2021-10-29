def RestrCopy():
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
    c=2
    while(c<21):
        d=a+str(c)
        e=b+str(c)
        c+=1
        mdb.models['Model-1'].Constraint(name=d, 
            objectToCopy=mdb.models['Model-1'].constraints['A1'])
        mdb.models['Model-1'].Constraint(name=e, 
            objectToCopy=mdb.models['Model-1'].constraints['P1'])
