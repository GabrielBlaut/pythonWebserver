import webserver
import os
image_dir = "html/images"

def test_generate_image_name():
    result = webserver.generate_image_name(image_dir)
    assert type(result) is str
    result = result.replace(image_dir,"")
    result = int(result.replace(".jpeg",""))
    assert result < 1234567
    assert result > 12345

def test_get_random_image(tmpdir):
    path = os.getcwd() + "/" + image_dir
    result = webserver.get_random_image(path)
    assert os.path.isdir(path) is True
    assert type(result) is str
    path = tmpdir.mkdir("sub")
    result = webserver.get_random_image(path)
    assert result == -1
    fp = path.join("hello.txt")
    fp.write("Hello World")
    result = webserver.get_random_image(path)
    assert result == fp

def test_list_dir(tmpdir):
    root_dir = tmpdir
    sub_dir = tmpdir.mkdir("sub")
    result = webserver.list_dir(root_dir,"/sub")
    assert result == '<html><body><ul></ul></body><html>'

    fp = sub_dir.join(".hidden.txt")
    fp.write("some hidden text")
    result = webserver.list_dir(root_dir,"/sub")
    assert result == '<html><body><ul></ul></body><html>'

    fp = sub_dir.join("hello.txt")
    fp.write("some text")
    result = webserver.list_dir(root_dir,"/sub")
    assert result == '<html><body><ul><li><a href="/sub/hello.txt">hello.txt</a></li></ul></body><html>'

    fp = sub_dir.join("hello2.txt")
    fp.write("some other text")
    result = webserver.list_dir(root_dir,"/sub")
    assert result == '<html><body><ul><li><a href="/sub/hello.txt">hello.txt</a></li><li><a href="/sub/hello2.txt">hello2.txt</a></li></ul></body><html>'
    
    fp = sub_dir.join(".hidden2.txt")
    fp.write("some new hidden text")
    result = webserver.list_dir(root_dir,"/sub")
    assert result == '<html><body><ul><li><a href="/sub/hello.txt">hello.txt</a></li><li><a href="/sub/hello2.txt">hello2.txt</a></li></ul></body><html>'




