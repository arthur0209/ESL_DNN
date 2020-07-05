# docker-keras - Keras in Docker with Python 3 and TensorFlow on CPU
#sudo docker run -d -i -t -p 127.0.0.1:8000:65432   /bin/bash
#docker export 3a1fabcb23e5 > mycontainer_export.tar
#docker exec -it ubuntu bash
#docker cp ./DNN_CLIENT01.py 3a1fabcb23e5:/app/DNN_CLIENT01.py
#docker cp ./DNN_SERVER01.py 3a1fabcb23e5:/app/DNN_SERVER01.py
#sudo docker ps
#df
#docker container ls
#docker export 3a1fabcb23e5 > mycontainer_export.tar
#ls -la
#rm myinterim2_export.tar 
## apt-get install procps  
#docker inspect 6a74deec3511 | grep "IPAddress"



FROM debian:stretch

#MAINTAINER gw0 [http://gw.tnode.com/] <gw.2018@ena.one>

ADD ./app /app

# install debian packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    # install essentials
    build-essential \
    g++ \
    git \
    openssh-client \
    # install python 3
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-virtualenv \
    python3-wheel \
    pkg-config \
    # requirements for numpy
    libopenblas-base \
    python3-numpy \
    python3-scipy \
    # requirements for keras
    python3-h5py \
    python3-yaml \
    python3-pydot \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# manually update numpy
RUN pip3 --no-cache-dir install -U numpy==1.13.3

RUN apt-get update  
RUN apt-get dist-upgrade -y
RUN apt-get install wget
RUN wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp35-none-linux_armv7l.whl
RUN pip3 install tensorflow-1.8.0-cp35-none-linux_armv7l.whl
RUN pip3 install mock
RUN pip3 install keras
#RUN python3 -c 'import keras; print(keras.__version__)'
RUN apt-get install nano
#RUN sudo -H pip3 install pandas
RUN apt-get install net-tools
RUN apt-get install procps -y


EXPOSE 65432
WORKDIR /app
CMD ["python3","DNN_SERVER01.py"]

