# ROOT data analysis helper

this is a collection of packaged functions of frequently used data analysis methods
the functions are implemented as wrapper around ROOT (version 6.24, 6.26 expected to be similar),
either in python (to be used with PyROOT) or in ROOT macros.

the implementations are in: ToolsCollection.h (.py)
the 'tutorial' (actually I tested the functions in the file) are in: ToolsCollection_TestBench.h (.ipynb)
note: currently i was writting in python and translate it into cpp file. if any problem arise in cpp, always check with the py file first.

# 1. to use with PyROOT,run for example:
```python
from root_tools.ToolsCollection import fft
from root_tools.ToolsCollection import cut_th1d
from root_tools.ToolsCollection import identify_hist_peaks
```

## 1.1 if you want to import the whole collection (and plan to reload), use:
```python
import importlib
tools = importlib.import_module("root_tools.ToolsCollection")
importlib.reload(tools)
```

## 1.2 if you do not plan to reload
```python
import root_tools.ToolsCollection
```
so the function should be called in this way:
```python
root_tools.ToolsCollection.fft(kwargs)
```

## 1.3 or using alias: 
```python
import root_tools.ToolsCollection as tools
tools.fft(kwargs)
```

# 2. for the ROOT macro, you can use it in two ways:
## 2.1 included in another ROOT macro (ROOT-based program file not yet tested)
just put: 
```c++
#include "ToolsCollection.h"
```
in the program file

## 2.2 use with pyROOT (recommended over the python file import)
```python
import ROOT
ROOT.gROOT.ProcessLine(".L ./ToolsCollection.h")
ROOT.fft(kwargs)
```

[^1]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
