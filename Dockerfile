FROM nvcr.io/nvidia/pytorch:23.09-py3

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
      xcb \ 
      libglib2.0-0 \
      libgl1-mesa-glx && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

WORKDIR /workspace
COPY . /workspace

RUN pip install -r requirements.txt


# RUN pip install --no-cache-dir opencv-python==4.8.0.74
