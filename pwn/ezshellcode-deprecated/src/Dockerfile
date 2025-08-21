FROM ubuntu:16.04

RUN sed -i "s|http://archive.ubuntu.com|http://mirrors.tuna.tsinghua.edu.cn|g" /etc/apt/sources.list && \
    apt-get update && apt install -y socat xinetd && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd

# 创建ctf用户(uid=1000)和angel用户
RUN useradd -m -u 1000 -s /bin/bash ctf && \
    useradd -m -u 1001 -s /bin/bash angel

WORKDIR /home/ctf


RUN mkdir -p /home/ctf/bin /home/ctf/lib /home/ctf/lib64 /home/ctf/dev && \
    cp /bin/bash /home/ctf/bin/ && \
    cp /bin/ls /home/ctf/bin/ && \
    cp /bin/cat /home/ctf/bin/ && \
    cp /usr/bin/id /home/ctf/bin/ && \
    cp -v /lib/x86_64-linux-gnu/libtinfo.so.5 /home/ctf/lib/ && \
    cp -v /lib/x86_64-linux-gnu/libdl.so.2 /home/ctf/lib/ && \
    cp -v /lib/x86_64-linux-gnu/libc.so.6 /home/ctf/lib/ && \
    cp -v /lib64/ld-linux-x86-64.so.2 /home/ctf/lib64/


RUN mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*


COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN chmod +x /start.sh && echo "Blocked by ctf_xinetd" > /etc/banner_fail
RUN echo "kernel.randomize_va_space = 0" >> /etc/sysctl.conf
# 拷贝挑战文件并设置权限
COPY ./bin/ /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chown angel:angel /home/ctf/flag.txt && \
    chmod 600 /home/ctf/flag.txt && \
    chown root:root /home/ctf/vuln && \
    chmod 6755 /home/ctf/vuln

CMD ["/start.sh"]

EXPOSE 9999
