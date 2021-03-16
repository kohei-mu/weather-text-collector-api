FROM continuumio/anaconda3:2020.11

RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y vim \
                      sudo \
                      iputils-ping \
                      net-tools \
                      cron \
                      libpq-dev \
                      postgresql-common \
                      build-essential \
                      mecab \
                      libmecab-dev \
                      mecab-ipadic-utf8 \
                      git \
                      make \
                      xz-utils \
                      file \
&& pip install -U pip \
&& pip install fastapi  \
               uvicorn \
               changefinder \
               pyyaml \
               psycopg2-binary \
               pygeohash \
               mecab-python3 \
               ginza \
               spacy \
               oseti \
&& python -m spacy download en_core_web_md \
&& python -m spacy download fr_core_news_md \
&& python -m spacy download zh_core_web_md \
&& git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
&& echo yes | mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -a \
&& ln -s /etc/mecabrc /usr/local/etc/mecabrc

WORKDIR /projects
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]