all: injectError

injectError: injectError.c
	gcc -Wall -o injectError injectError.c

clean:
	rm injectError
