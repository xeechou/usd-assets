## How to add/update new tests
This folder contains a set of MaterialX files that cover commonly used Prism materials in Autodesk products. 
There are two steps required to "generate" the test files. This generation steps is not required to run the tests. New test files need to generated only when new mtlx files are added or the usd template changes. 

#### 1. Generate a usd file to reference the mtlx file.
This requires MaterialX and USD python support enabled.

```
run authorUSDfilesforSubset.py 
```
See comments in the script for details. This script will generate usda files for each of the mtlx files in the python script. See `PRISM_PRESETS` to take a look at the list of Prism mtlx files that are used.

#### 2. Generate Base files
This requires USD built with --tests and --materialx enabled.
```
run testUsdImagingGLBasicDrawing -lighting -sceneLights -shading smooth -complexity 1.3 -offscreen -camera /Camera -stage Prism_002.usda -write baseline\Prism_002.png
```
This will generate a base file. 
A helper script `generatebase.*` is available that can generate this for all the prism subset.

#### 3. Commit the usd + mtlx files.
