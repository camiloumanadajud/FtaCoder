# FtaCoder

## Overview

This python package automatically determines if a topic is covered by a Free Trade Agreement (FTA) and whether the topic is excluded from dispute settlement mechanisms.

It generates both a html file with the analysis that you can open in any browser and a csv file for quantitative analysis.

The package includes the [TOTA full text machine-readable corpus of preferential trade agreements](https://github.com/mappingtreaties/tota). The corpus is distributed under Creative Commons Attribution-NonCommercial 4.0 International license. The corpus should be cited as: Wolfgang Alschner, Julia Seiermann & Dmitriy Skougarevskiy (2017): Text-as-data analysis of preferential trade agreements: Mapping the PTA landscape, UNCTAD Research Paper No. 5, UNCTAD/SER.RP/2017/5.

## Requirements
- Python 3.6 or higher
- The following Python packages:
    - os
    - termcolor
    - xml.etree.ElementTree
    - re
    - csv

## Installation

1. Download or code the package from this repository

2. Add the following code at the top of your Python script
```
import sys
import os
sys.path.append([Add here the path to the folder with the FtaCoderPackage])
from FtaCoder import *
```

## Instructions
The FtaCoder has two functions:
1. AnalizeSingleFtas to analyze one FTA.

It follows the following syntax. '[]' indicates optional arguments.

AnalizeSingleFta(TOPIC , FTA NUMBER, LIST OF KEYWORDS, OUTPUT FOLDER, [LIST OF KEYWORDS FOR COOPERATION CHAPTERS])

2. AnalizeAllFtas to analyze all the FTAs.

It follows the following syntax. '[]' indicates optional arguments.

AnalizeAllFtas(TOPIC, LIST OF KEYWORDS, OUTPUT FOLDER, [LIST OF KEYWORDS FOR COOPERATION CHAPTERS])


## Examples

### For a single FTA
AnalizeSingleFta('Mining','35', ['mining[a-zA-Z]*'],'Tests/Temp')

### For all FTAs
AnalizeAllFtas('Mining', ['mining[a-zA-Z]*'], 'Tests/Temp/')

## Licence
This package is distributed under the GNU General Public License Version 3.
