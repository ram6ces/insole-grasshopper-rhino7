FROM python:3.7

WORKDIR /workdir

COPY *.py /workdir/

COPY requirement.txt /workdir/

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN python3 -m pip install -r /workdir/requirement.txt

RUN cd /workdir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
