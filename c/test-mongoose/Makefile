PREFIX=/usr/local
DESTDIR=
LIBDIR=${PREFIX}/lib
INCDIR=${PREFIX}/include

CFLAGS+=-g -Wall -O2 -DDEBUG -fPIC
LIBS=
AR=ar
AR_FLAGS=rc
RANLIB=ranlib

all: libhttp test test-restful-server

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)

libhttp: libhttp.a

libhttp.a: http.o mongoose.o
	$(AR) $(AR_FLAGS) $@ $^
	$(RANLIB) $@

test-restful-server: restful_server.o libhttp.a
	$(CC) -o $@ $^ $(LIBS)

test: test.o mongoose.o libhttp.a
	$(CC) -o $@ $^ $(LIBS)

clean:
	rm -rf test-* *.dSYM *.o

.PHONY: install clean all test

install:
#	install -m 755 -d ${DESTDIR}${INCDIR}
#	install -m 755 -d ${DESTDIR}${LIBDIR}
#	install -m 755 libnsq.a ${DESTDIR}${LIBDIR}/libnsq.a
#	install -m 755 nsq.h ${DESTDIR}${INCDIR}/nsq.h
