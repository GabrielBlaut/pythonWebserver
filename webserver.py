
from http.server import HTTPServer,BaseHTTPRequestHandler
import os
import random

#choosing random image in a given folder

def get_random_image(imageDirPath):
    print(imageDirPath)
    image_path_list = ['/' + image for image in os.listdir(imageDirPath)
                if not os.path.isdir(imageDirPath+image)]
    print(image_path_list)           
    return imageDirPath + random.choice(image_path_list)

class myRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            
            #current/working/directory
            root= os.getcwd()
            full_path = root + self.path

            #path ends with /random 

            if self.path.endswith("/random"):
                image_path = get_random_image(root + '/html/images')
                print(image_path)
                statinfo = os.stat(image_path)
                img_size = statinfo.st_size
                print(img_size)

                self.send_response(200)
                self.send_header("Content-type", "image/jpg")
                self.send_header("Content-length", img_size)
                self.end_headers()


                img=open(image_path, 'rb')
                self.wfile.write(img.read())
                img.close()

            #check if path exists 
               
            elif not os.path.exists(full_path):
                msg = "File {} not found".format(self.path)
                self.send_error(404,msg)

            
            #path leads to a file

            elif os.path.isfile(full_path):
                statinfo = os.stat(full_path)
                site_size = statinfo.st_size

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length",site_size)
                self.end_headers()


                site=open(full_path,'rb')
                content=site.read()
                self.wfile.write(content)
                site.close()

            #path leads to a dir
            
            elif os.path.isdir(full_path):

                #if there is a index.html in this directory open it. 

                if os.path.exists(full_path + '/index.html'):
                    full_path = full_path + '/index.html'
                    statinfo = os.stat(full_path)
                    site_size = statinfo.st_size
    
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Content-Length",site_size)
                    self.end_headers()
    
    
                    site=open(full_path,'rb')
                    content=site.read()
                    self.wfile.write(content)
                    site.close()
                 

        except IOError as err :
            self.send_error(404,err)




def main():
    try:
        port=8000
        myServer=HTTPServer(('',port),myRequestHandler)
        print ("webserver running on %s" % port)
        myServer.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()

if __name__ == "__main__":
    main()