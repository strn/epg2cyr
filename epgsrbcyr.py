#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from   datetime import timedelta
import html
from   http.server import SimpleHTTPRequestHandler
import logging
import os.path
import urllib.request, urllib.error
import socketserver
import sys
import time
import xml.parsers.expat

logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='utf-8',
    handlers=[
        logging.FileHandler(os.path.join(os.path.expanduser('~'), 'sys', 'log', f"{sys.argv[0].replace('.py', '')}.log")),
        logging.StreamHandler(sys.stdout)
    ])

# Program-specific modules
from srbcirilizator import SrbCirilizator
from epgconfig import Config


# Parser for EPG file, replacing some elements
# with Cyrillic values
class EpgParser():

    def __init__(self):
        self.parser = xml.parsers.expat.ParserCreate()
        self.cir = SrbCirilizator()
        self.parser.StartElementHandler = self.start_element
        self.parser.EndElementHandler = self.end_element
        self.parser.CharacterDataHandler = self.char_data
        self.parser.XmlDeclHandler = self.xml_dec
        self.translit = False
        self.channel = ''

    # 3 handler functions
    def start_element(self, name, attrs):
        attrstr = ""
        if name in ('title', 'desc'):
            self.translit = True
        elif name == 'programme':
            if 'channel' in attrs.keys():
                self.channel = attrs['channel']
            else:
                self.channel = ''
        for key, value in attrs.items():
            attrstr = f'{attrstr} {key}="{value}"'
        self.outfile.write(f"<{name}{attrstr}>".encode('utf-8'))


    def end_element(self, name):
        self.outfile.write(f"</{name}>".encode('utf-8'))
        if name in ('channel', 'programme',):
            self.outfile.write(b"")
        self.translit = False

    def char_data(self, data):
        escaped = html.escape(data)
        if self.translit and self.channel in self.config['channels']:
            self.outfile.write(self.cir.text_to_cyrillic(escaped).encode('utf-8'))
        else:
            self.outfile.write(escaped.encode('utf-8'))

    def xml_dec(self, version, encoding, standalone):
        self.outfile.write(f'<?xml version="{version}" encoding="{encoding}" ?>'.encode('utf-8'))
        self.outfile.write(b"")

    def parse(self, config, infile, outfile):
        self.outfile = outfile
        self.config = config
        self.parser.ParseFile(infile)


class HttProxy(SimpleHTTPRequestHandler):

    def do_GET(self):
        url = self.path[1:]
        if not url in conf.config['epg'].keys():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"URL key '{url}' not found in configuration file\n".encode('utf-8'))
            return
        self.send_response(200)
        self.end_headers()
        try:
            cfg = conf.config['epg'][url]
            print(f"INFO: Key={url}, URL={conf.config['epg'][url]['url']}")
            start_time = time.time()
            parser.parse(cfg, urllib.request.urlopen(conf.config['epg'][url]['url']), self.wfile)
            end_time = time.time()
            time_elapsed = end_time - start_time
            print(f"INFO: Processing URL '{conf.config['epg'][url]['url']}' took {str(timedelta(seconds=time_elapsed))}")
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            print(f"ERROR: URL={url}, error: {err}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        conf = Config(sys.argv[1], sys.argv[0].replace('.py', ''))
    else:
        conf = Config()
    parser = EpgParser()
    port = conf.getkey('port')

    httpd = socketserver.ForkingTCPServer(('', port), HttProxy)
    print(f"INFO: Serving at port {port}")
    httpd.serve_forever()
