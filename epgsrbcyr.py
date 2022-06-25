#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from   datetime import date, datetime, timedelta
import gzip
import html
from   http.server import SimpleHTTPRequestHandler
import io
import logging
import re
import socketserver
import sys
import time
import unicodedata
import urllib.request, urllib.error
import xml.parsers.expat


logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='utf-8',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

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
        self.invalid_tag = False

    # Removes "foreign" (non-alphanumeric) characters
    def remove_foreign(self, word):
        tt = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8')
        return re.sub(r"[\s\(\)\/\&\!:\*\_\+,'\-]", '', tt)

    # 3 handler functions
    def start_element(self, name, attrs):
        attrstr = ""
        if name in ('title', 'desc'):
            self.translit = True
        elif name in self.config['invalid-tags']:
            self.invalid_tag = True
            return
        elif name == 'tv':
            if 'date' in attrs.keys():
                tvdate = attrs['date']
            else:
                tvdate = datetime.now().strftime("%Y%m%d")
            attrs = dict()
            attrs['date'] = tvdate
        elif name == 'programme':
            if 'channel' in attrs.keys():
                self.channel = self.remove_foreign(attrs['channel'].strip().lower())
            else:
                self.channel = ''
        elif name == 'channel':
            if 'id' in attrs.keys():
                attrs['id'] = self.remove_foreign(attrs['id'].strip().lower())
                if attrs['id'] in self.config['channel-map'].keys():
                    attrs['id'] = self.config['channel-map'][attrs['id']]
        for key, value in attrs.items():
            if key == 'channel':
                # Result of this will be in self.channel
                self.get_channel_name()
                attrstr = f'{attrstr} {key}="{self.channel}"'
            else:
                attrstr = f'{attrstr} {key}="{value}"'
        self.outfile.write(f"<{name}{attrstr}>".encode('utf-8'))

    def end_element(self, name):
        if name in self.config['invalid-tags']:
            self.invalid_tag = False
            return
        self.outfile.write(f"</{name}>".encode('utf-8'))
        if name in ('channel', 'programme', 'tv'):
            self.outfile.write(b"\n")
        self.translit = False

    def char_data(self, data):
        if self.invalid_tag:
            return
        escaped = html.escape(data.strip())
        if self.translit and self.channel in self.config['channel-translit']:
            self.outfile.write(self.cir.text_to_cyrillic(escaped).encode('utf-8'))
        else:
            self.outfile.write(escaped.encode('utf-8'))

    def xml_dec(self, version, encoding, standalone):
        self.outfile.write(f'<?xml version="{version}" encoding="{encoding}" ?>\n'.encode('utf-8'))
        self.outfile.write(b"")

    """
    Determine NEW channel 'name' based on existing one:

    - If channel name is found in map "channel-translit" it is left untouched; 'title' and 'desc' are converted to Cyrrilic
    - If channel name is found in list "dummy" it is replaced with "dummy"
    - If channel name is found in map "channel-map" it is replaced with lookup value
    """
    def get_channel_name(self):
        if self.channel in self.config['channel-map'].keys():
            self.channel = self.config['channel-map'][self.channel].lower()
        elif self.channel in self.config['dummy']:
            self.channel = f"dummy ({self.channel})".lower()

    def parse(self, config, infile, outfile):
        self.outfile = outfile
        self.config = config
        # Make all channel names in 'channel-translit' lowercase
        if 'channel-translit' in self.config.keys():
            self.config['channel-translit'] = [x.lower() for x in self.config['channel-translit']]
        if 'channel-map' in self.config.keys():
            self.config['channel-map'] = dict((k.lower(), v) for k,v in self.config['channel-map'].items())
        logging.info(f"Configuration={self.config}")
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
            epgurl = cfg['url']
            logging.info(f"Key={url}, URL={epgurl}")
            start_time = time.time()
            if epgurl[-3:] == 'xml':
                parser.parse(cfg, urllib.request.urlopen(epgurl), self.wfile)
            elif epgurl[-2:] == 'gz':
                infile = urllib.request.urlopen(epgurl)
                parser.parse(cfg, io.BytesIO(gzip.decompress(infile.read())), self.wfile)
            else:
                pass
            end_time = time.time()
            time_elapsed = end_time - start_time
            logging.info(f"Processed URL={epgurl} in time: {str(timedelta(seconds=time_elapsed))}")
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            logging.error(f"URL={url}, error: {err}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        conf = Config(sys.argv[1], sys.argv[0].replace('.py', ''))
    else:
        conf = Config()
    parser = EpgParser()
    port = conf.getkey('port')

    httpd = socketserver.ForkingTCPServer(('', port), HttProxy)
    logging.info(f"Serving at port {port}")
    httpd.serve_forever()
