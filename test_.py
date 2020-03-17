from generate import read_file
from generate import list_files

def test_read_file():
	index_content = ({"title": "My awesome site", "layout": "home.html"}, "blah blah")
	assert read_file('test/source/index.rst') == index_content, 'Empty File'

def test_list_files():
	assert list_files('test/source/') != None, 'No rst files in folder'

def test_type():
	dict_test = dict()
	assert type(read_file('test/source/index.rst')[0]) == type(dict_test), 'Wrong type'
