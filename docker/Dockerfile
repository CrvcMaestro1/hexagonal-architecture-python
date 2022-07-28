FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/code
COPY requirements.txt /opt/code/

COPY . /opt/code/

RUN sed -i 's/\r$//g' /opt/code/setup.sh
RUN chmod +x /opt/code/setup.sh
RUN bash -c "/opt/code/setup.sh"