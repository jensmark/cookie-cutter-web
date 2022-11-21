FROM cadquery/cadquery:latest AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt
RUN pip install --user gunicorn

FROM cadquery/cadquery:latest
WORKDIR /code

COPY --from=builder /home/cq/.local/lib/python3.8/site-packages/ .
COPY ./src .

CMD [ "python", "-m", "gunicorn", "server:server" ] 