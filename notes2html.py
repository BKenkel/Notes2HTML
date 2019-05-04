#!/usr/bin/python
import argparse
import logging as log
import os
import markdown

last_was_list = False


def generate_HTML_from_file(input_file_name, output_file):
    log.debug(f'Parsing file: {input_file_name}')
    if not os.path.isfile(input_file_name):
        log.critical(f'File Not Found: \'{input_file_name}\'')
        exit(1)

    with open(input_file_name, 'r') as input_file:
        lines = input_file.read()
    html = markdown.markdown(lines, extensions=['extra', 'nl2br', 'sane_lists', 'toc'])
    with open(output_file, 'w') as out:
        out.write(html)


if __name__ == '__main__':
    log.basicConfig(format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Generate an html file from a file using the schema.')
    parser.add_argument('--output-file', '-o', action='store', type=str)
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('file_to_parse', action='store')

    args = parser.parse_args()
    if args.output_file is None:
        args.output_file = os.path.splitext(args.file_to_parse)[0] + '.html'
    if args.verbose:
        log.getLogger().setLevel(log.DEBUG)
    print(args)

    log.info(f'Output file: {args.output_file}')
    generate_HTML_from_file(args.file_to_parse, args.output_file)
