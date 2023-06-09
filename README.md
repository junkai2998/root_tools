# ROOT data analysis helper

This is a collection of packaged functions of frequently used data analysis methods.This tries to make the heavily routined code can be used repeatedly without rewritten (also prone to error), inspired by [^2].
The functions are implemented as wrapper around ROOT (version 6.24, 6.26 expected to behave similarily),
either in python (to be used with PyROOT) or in ROOT macros.

the implementations are in: `ToolsCollection.h (.py)`

the 'tutorial' (actually I tested the functions in the file) are in: `ToolsCollection_TestBench.h (.ipynb)`

note:

you are recommended to use the `ToolsCollection.h`, either with another ROOT macro (or c++ based code) or in the PyROOT codes

currently i was writting in python and translate it into cpp file. if any problem arise in cpp, always check with the py file first.

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

note: this repo is meant to be portable for now, instead of a full package.
so if you import from other path, do something like:
```python
import sys
sys.path.append("path/root_tools/")
from ToolsCollection import *
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
the following code also work. But I still need some times to understand the working of c++ compiler and root interpreter[^3]
```python
r.gInterpreter.Declare('# include "path/to/ToolsCollection.h"') // is path/to/* a good practice ?
# r.gROOT.ProcessLine('# include "ToolsCollection.h"') # also work. but which one is more easy to move to compiled version ?
```

# 3. known issues
1. now the fft, residual only support TH1D. tried to use TH1 but got `calling a protected constructor of class 'TH1'` error
   maybe can overload the functions ?

[^1]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
[^2]: https://github.com/heymanwasup/OmegaFitting/blob/main/Fitter/functions.h
[^3]: https://root.cern.ch/root/htmldoc/guides/users-guide/ROOTUsersGuide.html#the-c-interpreter-cling
