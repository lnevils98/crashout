FROM python:3.13.2


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

# Set python path for all import requests
ENV PYTHONPATH=/code 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]