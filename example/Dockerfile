FROM python:3.11-slim-bullseye
RUN rm -rf /app
COPY . /app
WORKDIR /app    
RUN pip3 install -r requirements.txt
CMD ["python3" , "app.py"]