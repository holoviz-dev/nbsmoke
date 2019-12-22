"""Mainly code copied in from datashader's examples/nb, which itself
was copied straight from bokeh? Would be great to coordinate that a
bit better...

"""

import traceback
import warnings
import io
import nbformat
import nbconvert
import sys
import ast
import re

import pytest

class VerifyNb(pytest.Item):
    def runtest(self):

        ###################################################
        # quick hacks to handle missing optional modules
        _missing = []
        if BeautifulSoup is None:
            _missing.append("  * BeautifulSoup not available - please install beautifulsoup4")
        if requests is None:
            _missing.append("  * requests not available - please install requests")
        if _missing:
            raise Exception("nbsmoke verify failed to execute because of missing modules:\n"+"\n".join(_missing))
        ###################################################        
        
        filename = self.name

        bad_modules = check_modules(filename)
        try:
            bad_links = check_urls(filename, name='a', attribute='href')
        except requests.exceptions.ConnectionError:
            bad_links = traceback.format_exc(1)

        bad_images = check_urls(filename, name='img', attribute='src')

        if bad_modules or bad_links or bad_images:
            warnings.warn("%s:\n***** invalid modules: %s\n\n***** bad links: %s\n\n***** bad images: %s\n\n"%(filename,bad_modules,bad_links,bad_images) + "-"*20)


# TODO: capture or log the import errors
try:
    import requests, requests.exceptions
except:
    requests = None

try:
    from bs4 import BeautifulSoup
except:
    BeautifulSoup = None
            
###################################################
###################################################
# rest of this file is quickly copied in code from datashader
# examples/nb (which itself came from bokeh). Need to check it works
# as expected. Takes a while to run so must be doing something :) But
# fails to run properly for various projects other than datashader
# (e.g. for geoviews, gives spurious errors about notebook syntax,
# complains that
# https://www.earthsystemcog.org/projects/esmf/regridding is a bad
# link).

def export_as_html(filename):
    html_exporter = nbconvert.HTMLExporter()
    html_exporter.template_file = 'basic'
    body, _ = html_exporter.from_filename(filename)
    return body

def export_as_python(filename):
    with io.open(filename,encoding='utf8') as nbfile:
        nb = nbformat.read(nbfile, as_version=4)
        output, _ = nbconvert.PythonExporter().from_notebook_node(nb)
        if sys.version_info[0]==2:
            # notebooks will start with "coding: utf-8", but output already unicode
            # (alternative hack would be to find the coding line and remove it)
            output = output.encode('utf8')
        return output


def module_exists(name):
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True


def url_exists(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # dummy user agent for security filters
    response = requests.head(url, headers=headers)
    if not response.ok:
        response = requests.get(url, headers=headers)
    return response.ok


def check_modules(notebook):
    class ModuleReader(ast.NodeVisitor):
        def __init__(self):
            self.imports = set()

        def generic_visit(self, node):
            ast.NodeVisitor.generic_visit(self, node)
            return list(self.imports)

        def visit_Import(self, node):
            for alias in node.names:
                self.imports.add(alias.name)

        def visit_ImportFrom(self, node):
            self.imports.add(node.module)

    def get_ipython_modules(s):
        root = ast.parse(s)
        return ModuleReader().visit(root)

    bad_modules = set()

    for module in get_ipython_modules(export_as_python(notebook)):
        m = re.sub(r'\..*', '', module) if '.' in module else module
        if not module_exists(m):
            bad_modules.add(m)

    return bad_modules


def check_urls(notebook, name, attribute):
    REGEX_URL = re.compile('^(http|https):.+')

    bad_urls = set()

    html = export_as_html(notebook)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(name):
        url = tag.get(attribute)
        if REGEX_URL.match(url) and not url_exists(url):
            bad_urls.add(url)

    return bad_urls

