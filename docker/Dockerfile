FROM supervisely/base-py-sdk:6.72.106

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y git ffmpeg libsm6 libxext6 ninja-build

RUN pip3 install torch==1.8.2 torchvision==0.9.2 --extra-index-url https://download.pytorch.org/whl/lts/1.8/cu111

RUN apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U openmim
RUN mim install mmengine
RUN mim install 'mmcv>=2.0.0rc1'
RUN pip install 'mmdet>=3.0.0rc0'
RUN git clone https://github.com/open-mmlab/mmocr.git /mmocr
WORKDIR /mmocr
ENV FORCE_CUDA="1"
RUN pip install -r requirements.txt
RUN pip install .
RUN pip install -r requirements/albu.txt
