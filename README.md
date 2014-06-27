KX2-Server
==========

A prototype, multi purpose, extensible server utilizing Python's BaseHTTPServer Library. It is being tested for use as an HTML hosting server and a backend for applications, but is still exetremely expirimental. An online game server implemented in lisp is also being developed.


Usage
=====

To install the server system, simply put this repository in a suitable directory.

Each server has its own identifier. This is usually four letters describing the server type, followed by one letter representing the server classification. The classifications are as follows:

N - Normal, the production server
X - Expirimental, the server to test new, unstable ideas
P - Playground, the server to put proofs of concept, or to test new software

The corrosponding server types are as follows:

html - Webhosting server
chat - Raspberry Chat backend
game - Lisp online game server (not operational)

To run a specific server, use the run command followed by the servers full identifier. To launch the HTML Playground server, use this command in the server directory.

```
./run htmlp
```

To view the logs for a specific server, you use the log command.

```
./log htmlp
```

Each server also has a dedicated 4-digit port. For every server type, there is a single number betwesn 1 and 9, and for each classification there is a number layout. The layout formats are as follows:

x represents the respective number for the server type

N - x0x0
X - x000
P - xxxx

The number for each server type are as follows:

chat - 7
html - 8
game - 9


