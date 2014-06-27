# -*- encoding: utf-8 -*-
# RaspberryChat© System Expirimental Server
# KD-2 ChatServer-X
# Development Build Version 3.4
# By DathanStone© Software
# Copyright DathanStone Org. 2014-2015


import string, cgi, time, sys, re
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
CWD = os.path.abspath('.')
maintinenceResponses = {'/': 'KD2 ChatServer-X',
                        '/descrip': 'KD2 Expirimental Backend ChatServer for Raspberry Chat System',
                        '/id': 'ChatServer-X',
                        '/status': 'active'}
def isValidChars(string):
    if string != re.compile.search.group():
        ret = False
    else:
        ret = True
    return ret

class Holder(object):
    'Global Data Holder Class'

g = Holder()

#-----------------------------------------------------------------------------------------------------------------------

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            location = self.path
            print location
            data = {}

            if self.path.startswith('/sndmsg'):
                self.send_response(200)
                self.send_header('Content-type',      'text/ascii')
                self.end_headers()
                spltMsg = self.path.split('@')
                try:
                    if g.usrList[spltMsg[1]] == spltMsg[2]:
                        self.wfile.write('Message sent')
                        spltMsg = self.path.split('@')
                        g.msgList[spltMsg[4]].append([spltMsg[1], spltMsg[3]])
                    else:
                        self.wfile.write('Password invalid')
                except KeyError:
                    self.wfile.write('Username invalid')
                return

            if self.path.startswith('/getmsg'):
                self.send_response(200)
		self.send_header('Content-type',	'text/ascii')
                self.end_headers()
                spltMsg = self.path.split('@')
                try:
                    if g.usrList[spltMsg[1]] == spltMsg[2]:
                        allMsg = ''
                        for msg in g.msgList[spltMsg[1]]:
                            allMsg = allMsg + msg[0] + '@' + msg[1] + '$'
                        self.wfile.write(allMsg)
                    else:
                        self.wfile.write('Password invalid')
                except KeyError:
                     self.wfile.write('Username invalid')
                return

            if self.path.startswith('/clrmsg'):
                self.send_response(200)
                self.send_header('Content-type',       'text/ascii')
                self.end_headers()
                spltMsg = self.path.split('@')
                try:
                    if g.usrList[spltMsg[1]] == spltMsg[2]:
                        self.wfile.write('Messages cleared')
                        for i in range(len(g.msgList[spltMsg[1]])):
                            g.msgList[spltMsg[1]].remove(i - 1)
                    else:
                        self.wfile.write('Password invalid')
                except KeyError:
                    self.wfile.write('Username invalid')
                return

            if self.path == '/uptusr':
                self.send_response(200)
                self.send_header('Content-type',      'text/ascii')
                self.end_headers()
                g.usrFile.seek(0)
                g.usrList = eval(usrFile.read())
                return

            if self.path.startswith('/newusr'):
                self.send_response(200)
                self.send_header('Content-type',      'text/ascii')
                self.end_headers()
                spltMsg = self.path.split('@')
                if not spltMsg[1] in g.usrList:
                    if isValidChars(spltMsg[1]) and isValidChars(spltMsg[2]):
                        g.usrList[spltMsg[1]] = spltMsg[2]
                        g.msgList[spltMsg[1]] = []
                        self.wfile.write('User added')
                    else:
                        self.wfile.write('Invalid character found')
                else:
                    self.wfile.write('Username taken')
                return
                        
            if self.path in maintinenceResponses:
                self.send_response(200)
                self.send_header('Content-type',	'text/ascii')
                self.end_headers()
                self.wfile.write(maintinenceResponses[self.path])
                return

            else:
                self.send_response(404)
                self.send_header('Content-type',	'text/ascii')
                self.end_headers()
                self.wfile.write('Command not recognized')
                return        
                
            return
                
        except IOError, e:
            self.send_error(404,"File Not Found: %s\n<BR>%s" % (self.path, e))
     
def main():
    try:
        os.chdir(os.getenv('HOME') + '/server/chat/x/content/')
        g.msgFile = open('msgs.txt', 'r+')
        g.usrFile = open('usrs.txt', 'r+')
        g.msgFile.seek(0)
        g.usrFile.seek(0)
        g.msgList = eval(g.msgFile.read())
        g.usrList = eval(g.usrFile.read())
        server = HTTPServer(('', 7000), MyHandler)
        print 'Started chatserver...'
        sys.stderr.write('Started chatserver...\n')
        server.serve_forever()

    except KeyboardInterrupt:
        print ' received, shutting down chatserver...'
        sys.stderr.write('^C received, shutting down chatserver...\n')
	g.msgFile.seek(0)
	g.msgFile.write(str(g.msgList))
	g.msgFile.truncate()
        g.usrFile.seek(0)
        g.usrFile.write(str(g.usrList))
        g.usrFile.truncate()
        g.msgFile.close()
        g.usrFile.close()
        server.socket.close()

if __name__ == '__main__':
    main()

