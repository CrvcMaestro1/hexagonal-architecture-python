FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/code
COPY requirements.txt /opt/code/
RUN pip install -r requirements.txt

COPY ./setup.sh .
RUN sed -i 's/\r$//g' /opt/code/setup.sh
RUN chmod +x /opt/code/setup.sh

COPY . /opt/code/

CMD ["/opt/code/setup.sh"]