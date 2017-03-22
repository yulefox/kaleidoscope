PREFIX=/usr/local
DESTDIR=
LIBDIR=${PREFIX}/lib
INCDIR=${PREFIX}/include

CFLAGS+=-g -Wall -O2 -DDEBUG -fPIC
AR=ar
AR_FLAGS=rc
RANLIB=ranlib

all: test

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)

test: test.o mongoose.o
	$(CC) -o $@ $^

clean:
	rm -rf test-* *.dSYM *.o

.PHONY: install clean all test

install:
#	install -m 755 -d ${DESTDIR}${INCDIR}
#	install -m 755 -d ${DESTDIR}${LIBDIR}
#	install -m 755 libnsq.a ${DESTDIR}${LIBDIR}/libnsq.a
#	install -m 755 nsq.h ${DESTDIR}${INCDIR}/nsq.h
