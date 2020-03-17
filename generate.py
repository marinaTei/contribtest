# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import sys
import json
import unittest

log = logging.getLogger(__name__)


def list_files(folder_path):
	# gets path for all .rst files from folder_path
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
	# read files as raw_metadata and content
    with open(file_path, 'r') as f:
    	# metadata ends with ---
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        # content starts where metadat ends
        content = ""
        for line in f:
            content += line.strip('\n')
    
    return json.loads(raw_metadata), content

def write_output(name, html):
    with open(os.path.join('test', name+'.html'), 'w') as f:
        f.write(html)

def generate_site(folder_path, output_path):
	# first it creates an enviroment to load templates from the file system
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder_path + '/layout'), trim_blocks=True)
    # then for every file in the folder with path = folder_path
    for file_path in list_files(folder_path):
    	# first, it separates the file's metadata and content
        metadata, content = read_file(file_path)
        # gets the template from the metadata' layout
        template_name = metadata['layout']
        # creates the template
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        # html will be what we insert in the new file
        html = template.render(data).replace('\n\n', '\n')
        # check if output_path folder exists, if not create it
        if not os.path.exists(os.path.join('test', output_path)):
        	os.mkdir(os.path.join('test', output_path))
        # gets the name of the new file
        name = os.path.join(output_path, os.path.split(file_path)[1][:-4])
        
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig() 
    main()
