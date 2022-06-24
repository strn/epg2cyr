#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, os.path, sys

from epgconfig import Config
from multireplace import StringReplacer


def parse_args():
    parser = argparse.ArgumentParser(description="Parses text file, replacing multiple strings along the way")
    parser.add_argument('-c', '--config-file', help="Configuration file", required=True)
    parser.add_argument('-i', '--input-file', help="Input file", required=True)
    parser.add_argument('-o', '--output-file', help="Output file", required=True)
    return parser.parse_args()


def check_args(args):
    if not os.path.exists(args.input_file):
        print(f"ERROR: Input file '{args.input_file}' does not exist", file=sys.stderr)
        exit(1)
    if not os.path.exists(args.config_file):
        print(f"ERROR: Configuration file '{args.config_file}' does not exist", file=sys.stderr)
        exit(1)


def main(args):
    conf = Config(args.config_file)
    srepl = StringReplacer(conf.get())

    with open(args.output_file, "wb") as outf:
        with open(args.input_file) as inf:
            for index, line in enumerate(inf):
                outf.write(f"{srepl.process(line.strip())}\n".encode('utf-8'))
            inf.close()
        outf.close()


if __name__ == "__main__":
    args = parse_args()
    check_args(args)
    main(args)
