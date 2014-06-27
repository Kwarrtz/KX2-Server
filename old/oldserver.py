import string, cgi, time, sys
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
CWD = os.path.abspath('.')
UPLOAD_PAGE = 'upload.html'
fileTypes = [['.html', 'text/html'], ['.txt', 'text/ascii'], ['.png', 'image/png'], ['.ico', 'image/ico'],
['.jpg', 'image/jpeg'], ['.css', 'text/css']]
msgFile = open('msgs.txt', 'r+')
usrFile = open('usrs.txt', 'r+')
msgFile.seek(0)
usrFile.seek(0)      
msgList = eval(msgFile.read())
usrList = eval(usrFile.read())
def make_index( relpath ):     
    nabspath = os.path.abspath(relpath)
    flist = os.listdir( abspath )
    rellist = []    
    for fname in flist :     
        relname = os.path.join(relpath, fname)
        rellist.append(relname)
    inslist = []     
    for r in rellist :     
        inslist.append( '<a href="%s">%s</a><br>' % (r,r) )
    page_tpl = "<html><head></head><body>%s</body></html>"     
    ret = page_tpl % ( '\n'.join(inslist) , )
    return ret

#-----------------------------------------------------------

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global usrList
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
                    if usrList[spltMsg[1]] == spltMsg[2]:
                        self.wfile.write('Message sent')
                        spltMsg = self.path.split('@')
                        msgList[spltMsg[4]].append([spltMsg[1], spltMsg[3]])
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
                    if usrList[spltMsg[1]] == spltMsg[2]:
                        allMsg = ''
                        for msg in msgList[spltMsg[1]]:
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
                    if usrList[spltMsg[1]] == spltMsg[2]:
                        self.wfile.write('Messages cleared')
                        for i in range(len(msgList[spltMsg[1]])):
                            msgList[spltMsg[1]].remove(i - 1)
                    else:
                        self.wfile.write('Password invalid')
                except KeyError:
                    self.wfile.write('Username invalid')
                return

            if self.path == '/uptusr':
                self.send_response(200)
                self.send_headers('Content-type',      'text/ascii')
                self.end_headers()
                usrFile.seek(0)
                usrList = eval(usrFile.read())
                return         
 
            if location == '/test1':
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write('Welcome, %s %s' % (data['fname'], data['lname']))
                return

            if location == '/download':
                self.send_response(200)
                f = open('%s' %(data['downfile']))
                self.send_header('Content-type',        'binary/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return    

            if location == '/':
                self.send_response(200)
                f = open('redirect.html')
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            
            if self.path == "td":  
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write("Time and date:" + '<br>' + time.ctime())
                return
            
            if self.path.endswith("test2"):   
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write('''Hello world! "<BR>\n"''')
                self.wfile.write("Goodbye world!")
                return           
            
            for fileType in fileTypes:
                if self.path.endswith(fileType[0]):
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type',        fileType[1])
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return

            else:
                self.send_response(404)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write('The page: "' + self.path + '" has not been found' + "<BR>\n")
                self.wfile.write('location = ' + location + "<BR>\n")
                self.wfile.write('data = ' + str(data) + "<BR>\n")
                self.wfile.write(dir(self))
                return        
                
            return
                
        except IOError, e:
            self.send_error(404,"File Not Found: %s\n<BR>%s" % (self.path, e))
     
    def do_POST(self):
        #global rootnode
        print "posting..."
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     
            if ctype == 'multipart/form-data' :     
                # using cgi.FieldStorage instead, see 
                # http://stackoverflow.com/questions/1417918/time-out-error-while-creating-cgi-fieldstorage-object     
                fs = cgi.FieldStorage( fp = self.rfile, 
                                       headers = self.headers, # headers_, 
                                       environ={ 'REQUEST_METHOD':'POST' } # all the rest will come from the 'headers' object,     
                                       # but as the FieldStorage object was designed for CGI, absense of 'POST' value in environ     
                                       # will prevent the object from using the 'fp' argument !     
                                     )
             
            else: raise Exception("Unexpected POST request")
            fs_up = fs['upfile']
            filename = os.path.split(fs_up.filename)[1] # strip the path, if it presents     
            fullname = os.path.join(CWD, filename)
            # check for copies :     
            if os.path.exists( fullname ):     
                fullname_test = fullname + '.copy'
                i = 0
                while os.path.exists( fullname_test ):
                    fullname_test = "%s.copy(%d)" % (fullname, i)
                    i += 1
                fullname = fullname_test
            
            if not os.path.exists(fullname):
                with open(fullname, 'wb') as o:
                    # self.copyfile(fs['upfile'].file, o)
                    o.write( fs_up.file.read() )     
            
            self.send_response(200)
            self.send_header('Content-type',        'text/html')
            self.end_headers()
            f = open("x/new/x_aftrupld1.html")
            self.wfile.write(f.read())
            f.close()
            #self.wfile.write("<HTML><HEAD></HEAD><BODY>POST OK.<BR><BR>");
            #self.wfile.write( "File uploaded under name: " + os.path.split(fullname)[1] );
            #self.wfile.write(  '<BR><A HREF=%s>back</A>' % ( UPLOAD_PAGE, )  )
            #self.wfile.write("</BODY></HTML>");
        
        except Exception as e:
            # pass
            print e
            self.send_error(404,'POST to "%s" failed: %s' % (self.path, str(e)) )
 


def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'Started webserver...'
        sys.stderr.write('Started webserver...\n')
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down webserver...'
        sys.stderr.write('^C received, shutting down webserver...\n')
	msgFile.seek(0)
	msgFile.write(str(msgList))
	msgFile.truncate()
        msgFile.close()
        usrFile.close()
        server.socket.close()

if __name__ == '__main__':
    main()

