#!/usr/bin/env python
'''
Helper Script that reads in PrismSubset list (it's hard coded for now)
For each preset in the list, we load the corresponding mtlx file and deterimine the surfacematerial node
Then we author an usd file that references this mtlx file and the surfacematerial so that it can be rendered by usdrecord
'''

from pxr import Sdf, Usd, UsdGeom, UsdShade
import sys, os, argparse
import MaterialX as mx
from pathlib import Path

# get the material node from the materialx file
def _getMaterialName(mtlxdocumentFile):
    doc = mx.createDocument()
    try: 
        mx.readFromXmlFile(doc, mtlxdocumentFile)
    except mx.ExceptionFileMissing as err:
        print(err)
        sys.exit(0)

    materials = doc.getMaterialNodes()
    materialname = materials[0].getName()
    #print ("Material Name: %s" %(materialname))
    return materialname

# bind the materialx file to the template usd and save it as a new preset
def _addMaterialXRefToUsd(materialXBaseFile, surfaceMaterialName, outputUSDFilePath):
    # open template file
    stage = Usd.Stage.Open('_template.usda')
    mtlxScope = stage.DefinePrim('/MaterialX', 'Scope')
    mtlxScope.GetReferences().AddReference(materialXBaseFile, '/MaterialX')

    # prim in template file we need to update
    meshPrim = stage.GetPrimAtPath('/TestMaterial/Scenes/scene/Preview_Mesh/submesh')
    bindingapi = UsdShade.MaterialBindingAPI.Apply(meshPrim)
    materialBinding = UsdShade.Material.Define(stage, "/MaterialX/Materials/"+surfaceMaterialName)
    bindingapi.Bind(materialBinding)

    # export the modified stage 
    stage.GetRootLayer().Export(str(outputUSDFilePath))

def main():

    PRISM_PRESETS = [
        "Prism-119", "Prism-253", "Prism-105", "Prism-132", "Prism-414",
        "Prism-247", "Prism-399", "Prism-360", "Prism-397", "Prism-152",
        "Prism-171", "Prism-159", "Prism-207", "Prism-198", "Prism-042",
        "Prism-334", "Prism-066", "Prism-026", "Prism-227", "Prism-048",
        "Prism-005", "Prism-002", "Prism-013", "Prism-134", "Prism-2023",
        "Prism-2000", "Prism-2004", "Prism-2011", "Prism-2013", "Prism-2016",
        "Prism-2022"
    ]

    # Strips the newline character
    for preset in PRISM_PRESETS:
        # assemble mtlx filename
        materialXBaseFileName = preset.replace("-", "_")+".mtlx"
        materialXFileName = "./"+materialXBaseFileName
        defaultSurfaceMaterial = _getMaterialName(materialXFileName)

        # create output usd file name based on mtlx filename 
        outputUSDFile = Path(materialXBaseFileName)
        outputUSDFile = outputUSDFile.with_suffix('.usda')
        print ("Mtlx File: %s Material: %s OutputUSD: %s" % (materialXBaseFileName, defaultSurfaceMaterial, outputUSDFile))
        _addMaterialXRefToUsd(materialXFileName, defaultSurfaceMaterial, outputUSDFile)

if __name__ == '__main__':
    main()
