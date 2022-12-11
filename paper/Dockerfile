FROM python:3.9
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt && pip3 install --upgrade protobuf==3.20.0 && pip3 install --upgrade streamlit==1.11.1
EXPOSE 8501
COPY . /app
ENTRYPOINT ["streamlit", "run"]
CMD ["src/app.py"]