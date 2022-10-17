FROM node:16.15.0 AS builder
ADD ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN yarn install
ADD ./frontend /frontend
RUN yarn build --base="/routes/segmenter-ext/web/"

FROM python:3.8-slim
EXPOSE 8080
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 poppler-utils -y
ADD ./requirements.lock /
RUN pip install -r /requirements.lock
COPY --from=builder /frontend/dist /frontend/dist
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ENV PYTHONBUFFERED=1
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
CMD python -u services.py
