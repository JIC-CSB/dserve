# dserve

Tool to serve a dataset over HTTP.

## Installation

```
pip install dserve
```

## Usage

The command below serves the dataset located in ``/path/to/dataset``
on port 8080.

```
dserve -d path/to/dataset -p 8080
```

The default port is 5000.

The dataset can also be specified using the ``DSERVE_DATASET_PATH``
environment variable.

```
export DSERVE_DATASET_PATH=path/to/dataset
dserve
```

## Dataset creation

Datasets can be created using the related Python tools:

- dtoolcore
- dtool
