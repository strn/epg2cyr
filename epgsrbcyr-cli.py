#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from   datetime import datetime
import html
import logging
import os.path
import re
import sys
import unicodedata
# Program-specific modules
sys.path.insert(0, os.path.join(os.environ['HOME'], 'project', 'python', 'py2srbcyr'))
import py2srbcyr
import epgconfig

logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='utf-8',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Parser for EPG file, replacing some elements
# with Cyrillic values
class EpgParser():

    def __init__(self):
        self.cir = py2srbcyr.SerbCyr()
        self.translit = False
        self.ch_count = 0

    # Removes "foreign" (non-alphanumeric) characters
    def remove_foreign(self, word):
        tt = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8')
        return re.sub(r"[\s\(\)\/\&\!:\*\_\+,'\-]", '', tt)

    def get_text(self, ch_id, data):
        data = data.replace('_', '-')
        if ch_id in self.config['channel-translit']:
            return self.cir.text_to_cyrillic(data)
        else:
            return data

    def process_channels(self):
        for line in self.channels.readlines():
            l = line.strip().decode('utf-8')
            if l in ('', None,):
                continue
            self.ch_count += 1
            ch_id, ch_display_name = l.split('|')
            ch_id = self.get_channel_id(ch_id)
            if ch_display_name in ('', None,):
                disp_str = '<display-name/>'
            else:
                disp_str = f"<display-name>{html.escape(ch_display_name)}</display-name>"
            self.outfile.write(f"<channel id=\"{ch_id}\">{disp_str}</channel>\n".encode('utf-8'))

    def process_programmes(self):
        for line in self.programmes.readlines():
            l = line.strip().decode('utf-8')
            if l in ('', None,):
                continue
            ch_id, start, stop, title, desc = l.split('|')
            ch_id = self.get_channel_id(ch_id)
            title = html.escape(self.get_text(ch_id, title))
            if desc in ('', None,):
                desc_str = '<desc/>'
            else:
                desc_str = f"<desc>{html.escape(self.get_text(ch_id, desc))}</desc>"
            self.outfile.write(f"<programme start=\"{start}\" stop=\"{stop}\" channel=\"{ch_id}\"><title>{title}</title>{desc_str}</programme>\n".encode('utf-8'))

    def xml_start(self, version, encoding):
        self.outfile.write(f'<?xml version="{version}" encoding="{encoding}" standalone="yes" ?>\n'.encode('utf-8'))
        self.outfile.write(b"")
        self.outfile.write(f"<!-- EPG partially transliterated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')} -->\n".encode('utf-8'))
        self.outfile.write("<tv>\n".encode('utf-8'))

    def xml_end(self):
        self.outfile.write("</tv>\n".encode('utf-8'))
        logging.info(f"Processed {self.ch_count} channels")

    """
    Determine NEW channel 'name' based on existing one:

    - If channel name is found in map "channel-translit" it is left untouched; 'title' and 'desc' are converted to Cyrrilic
    - If channel name is found in list "dummy" it is replaced with "dummy"
    - If channel name is found in map "channel-map" it is replaced with lookup value
    """
    def get_channel_id(self, ch_id):
        if ch_id in self.config['channel-map'].keys():
            return self.config['channel-map'][ch_id].lower()
        if ch_id in self.config['dummy']:
            return f"dummy ({ch_id})".lower()
        return ch_id

    def parse(self, config, channels, programmes, outfile):
        self.outfile = outfile
        self.config = config
        self.channels = channels
        self.programmes = programmes
        # Make all channel names in 'channel-translit' lowercase
        if 'channel-translit' in self.config.keys():
            self.config['channel-translit'] = [x.lower() for x in self.config['channel-translit']]
        if 'channel-map' in self.config.keys():
            self.config['channel-map'] = dict((k.lower(), v) for k,v in self.config['channel-map'].items())
        #logging.info(f"Configuration={self.config}")
        self.create_epg()

    def create_epg(self):
        self.xml_start('1.0', 'UTF-8')
        self.process_channels()
        self.process_programmes()
        self.xml_end()
        self.channels.close()
        self.programmes.close()
        self.outfile.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog='EPG Serbian Cyrillic Transliterator',
        description='Program transliterates EPG guide from Croatian Latin into Serbian Cyrillic alphabet',
        epilog='Text at the bottom of help')
    argparser.add_argument('-c', '--configuration', required=True)
    argparser.add_argument('-p', '--programmes', required=True)
    argparser.add_argument('-a', '--channels', required=True)
    argparser.add_argument('-o', '--output-file', required=True)
    args = argparser.parse_args()

    # Check parameters
    if not os.path.exists(args.configuration):
        print(f"ERROR: Configuration file '{args.configuration}' does not exist, aborting...")
        exit(1)
    if not os.path.exists(args.programmes):
        print(f"ERROR: Input file with programmes '{args.programmes}' does not exist, aborting...")
        exit(1)
    if not os.path.exists(args.channels):
        print(f"ERROR: Input file with channels '{args.channels}' does not exist, aborting...")
        exit(1)
    parser = EpgParser()
    conf = epgconfig.Config(args.configuration, sys.argv[0].replace('.py', ''))

    parser.parse(
        conf.config['epg']['iptv-org-rs-mts'],
        open(args.channels, 'rb'),
        open(args.programmes, 'rb'),
        open(args.output_file, 'wb'))
