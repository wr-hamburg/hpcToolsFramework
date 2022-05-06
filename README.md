# Framework for automated HPC software analysis

## Build and Install Package locally

```
pip install build
python -m build
pip install .\dist\hpc_tools_framework-0.1.0.tar.gz
```

Install Package in Editable Mode so that Any changes to the original package would be reflected directly in your environment.

```
pip install -e .
```

### Run framework

Execute following commands in separate shell.

```
python -m hpc_tools_framework.webapp.worker
```

```
python -m hpc_tools_framework.webapp.app
```
