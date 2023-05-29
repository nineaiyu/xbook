FROM python:3.10.11-slim

# Fixes some weird terminal issues such as broken clear / CTRL+L
ARG PIP_MIRROR=https://mirrors.aliyun.com/pypi/simple

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update 

RUN apt-get install libmariadb-dev  -y
RUN apt-get install g++  -y
RUN rm -rf /var/lib/apt/lists/* 


# install pip
COPY requirements.txt /opt/requirements.txt
RUN cd /opt/ && pip install -U setuptools pip -i ${PIP_MIRROR} --ignore-installed && pip install --no-cache-dir -r requirements.txt -i ${PIP_MIRROR}

#RUN rm -rf /var/cache/yum/

WORKDIR /data/robot_server/
RUN addgroup --system --gid 101 nginx \
    && adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 101 nginx 


#ENTRYPOINT ["python", "manage.py", "start", "all","-u","nginx"]
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
