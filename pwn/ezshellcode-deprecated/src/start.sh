#!/bin/bash

cd /home/ctf || exit
exec socat TCP-LISTEN:9999,reuseaddr,fork \
EXEC:"su -s /bin/bash ctf",pty,stderr,setsid,sigint,sane

