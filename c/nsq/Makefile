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

lib: libnsqex.a

libnsqex.a:
	$(AR) x /usr/local/lib/libev.a
	$(AR) x /usr/local/lib/libevbuffsock.a
	$(AR) x /usr/local/lib/libjson-c.a
	$(AR) x /usr/local/lib/libnsq.a
	$(AR) $(AR_FLAGS) $@ *.o
	$(RANLIB) $@

test: test-hello

test-nsqd.o: test.c
	$(CC) -o $@ -c $< $(CFLAGS) -DNSQD_STANDALONE

test-hello: test.o 
	#$(CC) -o $@ $^ -Wl,-Bdynamic -lev -Wl,-Bstatic -levbuffsock -Wl,-Bdynamic -ljson-c -Wl,-Bstatic -lnsq -Wl,-Bdynamic -lcurl 
	$(CC) -o $@ $^ -lcurl -lm -lnsqex

clean:
	rm -rf lib*.a test-* *.dSYM *.o

.PHONY: install clean all test

install:
	install -m 755 libnsqex.a ${DESTDIR}${LIBDIR}/libnsqex.a
