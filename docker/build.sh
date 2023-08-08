#!/bin/bash
# docker build --no-cache -f ./Dockerfile-nogpu -t marts2007/basic-ml-3-8:nogpu .
docker build --no-cache -f ./Dockerfile-nogpu -t marts2007/basic-ml-3-8:nogpu .
#docker push marts2007/basic-ml-3-8:nogpu

# docker build -f ./Dockerfile -t marts2007/basic-ml-3-8:gpu .
# docker push marts2007/basic-ml-3-8:gpu