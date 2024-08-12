FROM python:3.12-slim

WORKDIR /chronos

COPY ./app /chronos/app

RUN apt-get update && apt-get install -y --no-install-recommends git

RUN pip install git+https://github.com/amazon-science/chronos-forecasting.git

RUN pip install pandas fastapi uvicorn pydantic

EXPOSE 8000

ARG UID=1001
ARG GID=1001

RUN groupadd -g "${GID}" sas \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" sas

USER python

ENV CHRONOS_MODEL "amazon/chronos-t5-small"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]