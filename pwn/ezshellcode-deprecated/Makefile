.POSIX:
.DEFAULT_GOAL := 32
CFLAGS = -Wall -O0 -no-pie -fno-stack-protector -z execstack -z norelro
gcc_docker=docker run -v $(shell pwd)/src:/src -it utils_gcc:latest

32:
	$(gcc_docker) gcc -m32 $(CFLAGS) -o /src/bin/vuln /src/src/vuln.c

64:
	$(gcc_docker) gcc -m64 $(CFLAGS) -o /src/bin/vuln /src/src/vuln.c

test:
	$(gcc_docker) gcc -m32 $(CFLAGS) -o /dist/test /src/test.c

clean:
	$(RM) dist/*