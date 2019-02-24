#!/usr/bin/python
import getopt
import logging as log
import os
import sys


def main():
    try:
        input_file_name = sys.argv[1]
    except IndexError:
        input_file_name = input('No input file specified! Please supply a file: ')

    options, not_included = getopt.gnu_getopt(sys.argv[2:], 'o:v', ['output_file=',
                                                                    'verbose'])

    output_file_name = os.path.splitext(input_file_name)[0] + '.html'
    log.basicConfig(format='%(levelname)s: %(message)s')

    for option, arg in options:
        if option in ('-o', '--output_file'):
            output_file_name = arg
        elif option in ('-v', '--verbose'):
            log.getLogger().setLevel(log.DEBUG)

    if not_included:
        if len(not_included) == 1:
            log.warning(f'Unknown argument will not be applied: \'{not_included[0]}\'')
        else:
            log.warning(f'Unknown arguments will not be applied: {not_included}')

    log.info(f'Output file: {output_file_name}')
    parse_file(input_file_name)


def parse_file(input_file_name):
    log.debug(f'Parsing file: {input_file_name}')
    if not os.path.isfile(input_file_name):
        log.critical(f'File Not Found: \'{input_file_name}\'')
        exit(1)

    with open(input_file_name, 'r') as file:
        line = file.readline().rstrip()
        while line:
            log.debug('line: ' + line)
            # TODO parse line
            line = file.readline().rstrip()


if __name__ == '__main__':
    main()
