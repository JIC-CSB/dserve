#!/bin/bash
DATASET_PATH=$1
echo "Dataset path: $DATASET_PATH"

docker run -it --rm -v $DATASET_PATH:/dataset:ro -v $DATASET_PATH/.dtool/overlays:/dataset/.dtool/overlays -e "DSERVE_DATASET_PATH=/dataset" -p 5000:5000 jicscicomp/dserve
