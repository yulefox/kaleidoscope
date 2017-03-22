PREFIX=/usr/local
DESTDIR=
LIBDIR=${PREFIX}/lib
INCDIR=${PREFIX}/include

CFLAGS+=-g -Wall -O2 -DDEBUG -fPIC
AR=ar
AR_FLAGS=rc
RANLIB=ranlib

all: lib test

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)

lib:

libnsq.a: command.o reader.o nsqd_connection.o http.o message.o nsqlookupd.o json.o
	$(AR) $(AR_FLAGS) $@ $^
	$(RANLIB) $@

test: test-hello

test-nsqd.o: test.c
	$(CC) -o $@ -c $< $(CFLAGS) -DNSQD_STANDALONE

test-hello: test.o 
	$(CC) -o $@ $^ -lev -levbuffsock -ljson-c -lcurl -lnsq

clean:
	rm -rf lib*.a test-* *.dSYM *.o

.PHONY: install clean all test

install:
#	install -m 755 -d ${DESTDIR}${INCDIR}
#	install -m 755 -d ${DESTDIR}${LIBDIR}
#	install -m 755 libnsq.a ${DESTDIR}${LIBDIR}/libnsq.a
#	install -m 755 nsq.h ${DESTDIR}${INCDIR}/nsq.h
