FROM ubuntu:22.04

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y socat

RUN useradd -m ctf
WORKDIR /home/ctf

COPY dist/chall /home/ctf/chall
COPY flag.txt /home/ctf/flag.txt

RUN chown root:ctf /home/ctf/chall && \
    chmod 750 /home/ctf/chall && \
    chmod 440 /home/ctf/flag.txt && \
    chown root:ctf /home/ctf/flag.txt

EXPOSE 9999

USER ctf

CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/home/ctf/chall",stderr