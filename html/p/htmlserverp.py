import string, cgi, time, sys
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
CWD = os.path.abspath('.')
UPLOAD_PAGE = 'upload.html'
fileTypes = [['.html', 'text/html'], ['.txt', 'text/ascii'], ['.png', 'image/png'], ['.ico', 'image/ico'],
['.jpg', 'image/jpeg'], ['.css', 'text/css']]
maintinenceResponses = {'/descrip': 'KD2 HTML Playground Webserver',
                        '/id': 'HTMLServer-P',
                        '/status': 'active'}

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

            if location == '/download':
                self.send_response(200)
                f = open('%s' %(data['downfile']))
                self.send_header('Content-type',        'binary/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return    

            if self.path.endswith('/'):
                self.send_response(200)
                f = open(curdir + sep + self.path + 'index.html') 
                self.send_header('Content-type',        'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()            
                return

            if self.path in maintinenceResponses:
                self.send_response(200)
                self.send_header('Content-type',        'text/ascii')
                self.end_headers()
                self.wfile.write(maintinenceResponses[self.path])
                return

            if self.path.endswith('.htpy'):
                self.send_response(200)
                os.system('touch ' + curdir + sep +  self.path + 'o')
                os.system('python2.7 ' + curdir + sep + self.path + ' > ' + curdir + sep + self.path + 'o')
                f = open(curdir + sep + self.path + 'o')
                self.send_header('Content-type',         'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                os.system('rm ' + curdir + sep + self.path + 'o')
                return
                            

            for fileType in fileTypes:
                if self.path.endswith(fileType[0]):
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type',         fileType[1])
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return

            else:
                self.send_error(404, "File Not Found: %s\n<BR>" % (self.path))                
            return
                
        except IOError, e:
            self.send_error(404, "File Not Found: %s\n<BR>" % (self.path))
     
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
        os.chdir(os.getenv('HOME') + '/dev/webserver/html/p/content')
        server = HTTPServer(('', 8888), MyHandler)
        print 'Started webserver...'
        sys.stderr.write('Started webserver...\n')
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down webserver...'
        sys.stderr.write('^C received, shutting down webserver...\n')
        server.socket.close()

if __name__ == '__main__':
    main()

