#!/bin/bash
ulimit -t 55 #max cpu using
ulimit -m 524288 #max memory
ulimit -u 1500 #max process

export FLAG="MOCSCTF{n0t_a_bug_just_a_f3ature}"
echo $FLAG >./flag
exec ./pwn
