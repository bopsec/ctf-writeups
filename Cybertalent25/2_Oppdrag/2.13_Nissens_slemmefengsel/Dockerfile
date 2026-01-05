FROM dustingram/vintage-python:0.9.1@sha256:6ba6bc925fc2b12214de791c9d779c07dc077603ec90a2344ae774457ce09c7b

RUN apt-get install -y socat

WORKDIR /app

COPY --chmod=755 src/challenge /app/challenge
COPY --chmod=555 src/init.sh /app/init.sh

CMD ["/app/init.sh"]
