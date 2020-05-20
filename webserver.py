'''Python Webserver with a random picture display and upload feature'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import random
import cgi

image_dir = 'html/images'


def upload_image(header  , rfile):
    """Uploads a file if it ends with .jpeg """
    ctype= cgi.parse_header(header.get('Content-Type'))[0]

    if ctype == 'multipart/form-data':   

        form = cgi.FieldStorage(fp=rfile, 
                                headers=header, 
                                #keep_blank_values=1,
                                environ={'REQUEST_METHOD':'POST',
                               'CONTENT_TYPE':ctype,})

        file_name = generate_image_name(image_dir)

        file_content = form['file'].file.read()
        print(file_content)

        file_pointer = open(image_dir + "/" + file_name, "wb")   
        file_pointer.write(file_content)
        file_pointer.close()

        return 1
    else:
        return -1

def generate_image_name(path):
    '''generates a random filename'''
    value = 0
    while value < 1234567 :
        value = value + random.randint(12345,123456)
        if not os.path.isfile(path + str(value)):
            return str(value) + ".jpeg"

    #exception raise
   
def get_random_image(image_dir_path):
    '''choosing random image in a given folder'''

    image_path_list = [image for image in os.listdir(image_dir_path)
                       if not os.path.isdir(image_dir_path+image)]
    
    if not image_path_list:
        return -1
    else:
        return image_dir_path + "/" + random.choice(image_path_list)

def list_dir(root_dir, dir_path):
    '''creating html-webpage with a list of non hidden content'''
    full_path = root_dir + dir_path
    print(dir_path)
    listing = ['<li><a href="{0}/{1}">{1}</a></li>'.format(dir_path, directory)
               for directory in os.listdir(full_path)
               if not directory.startswith('.')]
    return '<html><body><ul>' + ''.join(listing) + '</ul></body><html>'

class MyRequestHandler(BaseHTTPRequestHandler):
    '''Handle HTTP requests '''
    def do_GET(self):
        '''implementation of the do_GET method'''
        try:

            #current/working/directory
            root = os.getcwd()
            print(root)
            full_path = root + self.path

            #path ends with /random

            if self.path.endswith('/random'):
                image_path = get_random_image(root +"/"+ image_dir)
                self.send_path_content(image_path, "image/jpg")

            #check if path exists

            elif not os.path.exists(full_path):
                msg = "File {} not found".format(self.path)
                self.send_error(404, msg)

            #path leads to a file

            elif os.path.isfile(full_path):
                self.send_path_content(full_path, None)

            #path leads to a dir


            elif os.path.isdir(full_path):

                #if there is a index.html in this directory open it.

                if os.path.exists(full_path + '/index.html'):
                    full_path = full_path + '/index.html'
                    self.send_path_content(full_path, "text/html")

                # if there is no index.html you should do a listing of all files in the directory

                else:
                    site = list_dir(root, self.path)
                    self.send_content(site.encode(), "text/html")

        except IOError as err:
            self.send_error(404, err)

    def do_POST(self):
        '''implementation of the do_POST method'''
        try:
            
            if upload_image(self.headers,self.rfile):
                post_body = "File received and uploaded suscessfully"
            else:
                post_body = "This is not an .jpeg file"

            msg = "received post request:{}\n".format(post_body)
            self.send_content(msg.encode(), "text/plain; charset=utf-8")

        except IOError as err:
            self.send_error(404, err)


    def send_content(self, content, content_type):
        '''Sends the content to client with appropiate headers'''
        try:

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()

            self.wfile.write(content)

        except IOError as err:
            self.send_error(404, err)



    def send_path_content(self, path, content_type):
        '''Sends the content of a file to client with appropiate headers'''
        try:
            statinfo = os.stat(path)
            size = statinfo.st_size

            self.send_response(200)
            if content_type is not None:
                self.send_header("Content-type", content_type)
            self.send_header("Content-Length", size)
            self.end_headers()

            site = open(path, 'rb')
            content = site.read()
            self.wfile.write(content)
            site.close()

        except IOError as err:
            self.send_error(404, err)


def main():
    '''Starts Server at port 8000 and closes it after a keyboardinterrupt'''
    try:
        port = 8080
        my_server = HTTPServer(('', port), MyRequestHandler)
        print("webserver running on port %s" % port)
        my_server.serve_forever()

    except KeyboardInterrupt:
        my_server.socket.close()

if __name__ == "__main__":
    main()
