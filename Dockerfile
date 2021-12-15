FROM python:3.8-bullseye

WORKDIR /land_mgmt
ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=5000
ENV PORT=5000
COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
# EXPOSE 5000
ENV GOOGLE_APPLICATION_CREDENTIALS="./landmanagementservice-bedfcda2f95d.json"
COPY . .
CMD ["flask", "run","--host=0.0.0.0"]
# CMD ["python","main.py"]