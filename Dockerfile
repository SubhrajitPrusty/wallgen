FROM python:3.7-slim
RUN mkdir -p /wallgen
COPY app.py /wallgen/
COPY requirements.txt /wallgen/
COPY wallgen.py /wallgen/
COPY static /wallgen/static
COPY templates /wallgen/templates
COPY tools /wallgen/tools
WORKDIR /wallgen
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "app.py"]
