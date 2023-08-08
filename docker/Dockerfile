FROM --platform=amd64 ubuntu:18.04
COPY requirements.txt .
ENV DEBIAN_FRONTEND noninteractive
RUN useradd -ms /bin/bash --uid 1000 jupyter\
 && apt update\
 && apt install -y python3.8-dev python3.8-distutils gnupg wget software-properties-common curl wget\
 && ln -s /usr/bin/python3.8 /usr/local/bin/python3\
 && curl https://bootstrap.pypa.io/get-pip.py | python3
ENV LD_LIBRARY_PATH \
/usr/local/cuda-11.2/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64 && \
apt-get update &&\
 apt-get install -y -q xserver-xorg-core wget &&\
 wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin -O \
/etc/apt/preferences.d/cuda-repository-pin-600 &&\
 apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub &&\
 add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /" &&\
 apt-get update &&\
 apt-get -y install libnvidia-common-450 cuda-drivers-450 nvidia-driver-450 &&\
 apt-get -y install cuda-11-2 libcudnn8=8.1.1.33-1+cuda11.2 cuda-toolkit-11-2 &&\
apt install ncdu && \
apt clean && apt autoremove --yes \
&& rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN  pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
