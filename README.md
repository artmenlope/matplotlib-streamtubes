[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/artmenlope/matplotlib-streamtubes/blob/master/LICENSE.md)
![Last Commit](https://img.shields.io/github/last-commit/artmenlope/matplotlib-streamtubes)

# matplotlib-streamtubes
MATLAB-like streamtubes in Matplotlib.

In this repository you will find a script ([`streamtubes.py`](streamtubes.py)) that can be used as module for plotting streamtubes in Matplotlib.

## Examples

In this section you will find a couple of examples on how to use [`streamtubes.py`](streamtubes.py) to generate the streamtubes.

The module can be used by placing [`streamtubes.py`](streamtubes.py) in your working directory and importing it using

```python
import streamtubes as st
```

Then, it can be used, for example, running a code line that looks like this:

```python
st.plot_streamtube(ax, x, y, z, r)
```

The following two images are the result of running the scripts [`streamtube_examples_1.py`](streamtube_examples_1.py) and [`streamtube_examples_2.py`](streamtube_examples_2.py) respectively.


![](https://github.com/artmenlope/matplotlib-streamtubes/blob/master/images/example_1.svg) |  ![](https://github.com/artmenlope/matplotlib-streamtubes/blob/master/images/example_2.svg)
| :-------------: | :-------------: |


## To do:

- [ ] Comment the code better.
- [ ] Document the process of creation of the streamtubes in this readme.
- [ ] Improve this readme in general.
