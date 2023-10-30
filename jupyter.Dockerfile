FROM jupyter/scipy-notebook
COPY requirements.txt requirements.txt
RUN pip install neo4j
EXPOSE 8888
