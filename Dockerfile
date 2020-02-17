FROM python:3.7-stretch
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN curl -sL https://raw.githubusercontent.com/stephencelis/ghi/master/ghi > ghi && chmod 755 ghi && mv ghi /usr/local/bin
RUN apt update && apt install -y ruby
RUN ghi --version
ENTRYPOINT ["python", "5kgenerator.py"]