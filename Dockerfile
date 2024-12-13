# syntax=docker/dockerfile:1.10.0

FROM rasa/rasa-pro:3.10.5

USER root
# Optionally install extra system libraries
# RUN apt-get update && \
#     apt-get install -y foo bar
# Optionally install extra python packages
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache -r requirements.txt
COPY actions actions
COPY data data
COPY domain domain
COPY docs docs
#COPY domain.yml domain.yml
#COPY config.yml config.yml
COPY configs configs
COPY credentials.yml credentials.yml
COPY endpoints.yml endpoints.yml
RUN --mount=type=secret,id=RASA_PRO_LICENSE,env=RASA_PRO_LICENSE \
    --mount=type=secret,id=OPENAI_API_KEY,env=OPENAI_API_KEY \
    rasa train -c configs/llm_openai.yml -d domain
