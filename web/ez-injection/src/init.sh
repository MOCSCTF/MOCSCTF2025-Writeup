#!/bin/bash
chmod 400 /flag.txt

chmod u+s /bin/date

service apache2 start

tail -f /dev/null