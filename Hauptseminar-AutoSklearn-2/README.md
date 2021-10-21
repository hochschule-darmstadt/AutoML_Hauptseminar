# Sub Repo for AutoSklearn Student 2

This AutoML does not work on windows. See [here](https://automl.github.io/auto-sklearn/master/installation.html#windows-osx-compatibility) for more information. It is recommended to execute a Docker container within windows, or install a virtual machine. In addition, at least python >= 3.7 is needed.

tl;dr for Docker + Notebook:

```bash
docker pull mfeurer/auto-sklearn:master
docker run -it -v ${PWD}:/opt/nb -p 8888:8888 mfeurer/auto-sklearn:master /bin/bash -c "mkdir -p /opt/nb && jupyter notebook --notebook-dir=/opt/nb --ip='0.0.0.0' --port=8888 --no-browser --allow-root"
```

Since in this case Jupyter Notebook was used, the according notebook was included as source file.
