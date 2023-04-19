# ROOT data analysis helper

this is a collection of packaged functions of frequently used data analysis methods
the functions are implemented as wrapper around ROOT (version 6.24, 6.26 expected to be similar),
either in python (to be used with PyROOT) or in ROOT macros.

# 1. to use with PyROOT,run for example:
```
from root_tools.ToolsCollection import fft
from root_tools.ToolsCollection import cut_th1d
from root_tools.ToolsCollection import identify_hist_peaks
```

## 1.1 if you want to import the whole collection (and plan to reload), use:
```
import importlib
tools = importlib.import_module("root_tools.ToolsCollection")
importlib.reload(tools)
```

## 1.2 if you do not plan to reload
`import root_tools.ToolsCollection `
so the function should be called in this way:
`root_tools.ToolsCollection.fft`

## 1.3 or using alias: 
```
import root_tools.ToolsCollection as tools
tools.fft(kwargs)
```

# 2. for the ROOT macro, you can use it in two ways:
## 2.1 included in another ROOT macro (c++ program file not yet tested)
just put:
`#include "ToolsCollection.h"`

## 2.2 use with pyROOT (recommended over the python file import)
```
import ROOT as r
r.gROOT.ProcessLine(".L ./ToolsCollection.h")
r.fft(kwargs)
```
