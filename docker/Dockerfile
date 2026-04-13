FROM quay.io/jupyter/pyspark-notebook:latest

WORKDIR /home/jovyan/work

COPY . /home/jovyan/work

USER root
RUN chown -R jovyan:users /home/jovyan/work

USER jovyan

RUN pip install --no-cache-dir  \
                pyyaml  \
                pandas  \
                matplotlib  \
                seaborn  \
                plotly && \
    pip install --no-cache-dir -e .

CMD ["bash"]