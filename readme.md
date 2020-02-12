# About
Syspy is a convient library for spinning up command line tools in python

[on test pypi](https://test.pypi.org/project/syspy/)

[on github](https://github.com/mrgarelli/PySys)

# Testing
> python3 -m pytest

# Installation

### new install from test-pypi
> python3 -m pip install -i https://test.pypi.org/simple/ syspy

### upgrade the python package
> python3 -m pip install --upgrade -i https://test.pypi.org/simple/ syspy

# Usage
simply run the following in any python3 script:

```
from syspy import Shell
from syspy.tools import getInputs, parseOptions
```
