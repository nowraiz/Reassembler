import angr


def runRamblr(binary):
    project = angr.Project(binary, auto_load_libs=False, main_opts={'base_addr' : 0})
    analysis = project.analyses.Reassembler()
    return analysis

def mapLabelType(label):
    ty = type(label)
    typeName = None
    if ty == angr.analyses.reassembler.FunctionLabel:
        typeName = "FunctionLabel"
    elif ty == angr.analyses.reassembler.DataLabel:
        typeName = "DataLabel"
    elif ty == angr.analyses.reassembler.NotypeLabel:
        ty = "NotypeLabel"
    elif ty == angr.analyses.reassembler.ObjectLabel:
        ty = "ObjectLabel"
    elif ty == angr.analyses.reassembler.Label:
        ty = "Label"
    else:
        ty = "Unknown"
    return ty

def createLabels(analysis):
    addrToLabel = { k : f(k[0]) for k,v in analysis.symbol_manager.addr_to_label if len(v) > 0 }

    return addrToLabel

def run(name):
    analysis = runRamblr(name)
    return createLabels(analysis)
