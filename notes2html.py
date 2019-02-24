#!/usr/bin/python
import getopt
import logging as log
import os
import sys

last_was_list = False


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
    init_out_file(input_file_name, output_file_name)
    parse_file(input_file_name, output_file_name)
    with open(output_file_name, 'a') as out_file:
        out_file.write('</body>\n')
        out_file.write('</html>')


def init_out_file(input_file_name, output_file_name):
    with open(output_file_name, 'w') as out_file:
        out_file.write('<!DOCTYPE html>\n')
        out_file.write('<html lang="en">\n')
        out_file.write('<head>\n')
        out_file.write('\t<meta charset="UTF-8">\n')
        out_file.write(f'\t<title>{os.path.basename(input_file_name)}</title>\n')
        out_file.write('</head>\n')
        out_file.write('<body>\n')


def parse_file(input_file_name, output_file_name):
    log.debug(f'Parsing file: {input_file_name}')
    if not os.path.isfile(input_file_name):
        log.critical(f'File Not Found: \'{input_file_name}\'')
        exit(1)

    with open(input_file_name, 'r') as input_file:
        file_length = len(input_file.readlines())

    with open(input_file_name, 'r') as input_file:
        with open(output_file_name, 'a') as out_file:
            line = input_file.readline().rstrip()
            next_line = input_file.readline().rstrip()
            for i in range(0, file_length):
                log.debug('line: ' + line)
                parse_line(out_file, line, next_line)

                line = next_line
                next_line = input_file.readline().rstrip()


def parse_line(out_file, line, next_line):
    words = line.split()

    if not line:
        out_file.write('<p>&nbsp;</p>\n')
    elif words[0] == ';;topic':
        out_file.write(f'<h1>{line.split(maxsplit=1)[1]}</h1>\n')
    elif words[0] == ';;point':
        out_file.write(f'<h2>{line.split(maxsplit=1)[1]}</h2>\n')

    elif words[0] == '--':
        global last_was_list
        if not last_was_list:
            out_file.write('<ul>\n')
            last_was_list = True
        out_file.write(f'<li>{line.split(" ", maxsplit=1)[1]}')
        count_tabs = line.count('\t')
        if '--' in next_line:
            next_count_tabs = next_line.count('\t')
            if next_count_tabs <= count_tabs:
                for i in range(next_count_tabs, count_tabs):
                    out_file.write('</li>\n')
                    out_file.write('</ul>\n')
                out_file.write('</li>\n')
            else:
                out_file.write('<ul>\n')
        else:
            for i in range(0, count_tabs + 1):
                out_file.write('</li>\n')
                out_file.write('</ul>\n')

    elif words[0] == '!!':
        out_file.write(f'<h4><span style="color: #F00;">{line.split(maxsplit=1)[1]}</span></h4>\n')
    elif words[0] == ';;img':
        out_file.write(f'<p><img src="{line.split(maxsplit=1)[1]}" alt=""/></p>\n')
    elif '<' in line and '>' in line.split('<')[1]:
        link = line.split('<')[1].split('>')[0]
        out_file.write(f'<p><a href="{link}" target="_blank" rel="noopener">{link}</a></p>\n')
    else:
        # Need to parse the line
        out_file.write('<p>')

        open_bold = False
        open_underline = False
        open_italic = False
        for char in line:
            if char == '*':
                if not open_bold:
                    out_file.write('<strong>')
                    open_bold = True
                else:
                    out_file.write('</strong>')
                    open_bold = False
            elif char == '_':
                if not open_underline:
                    out_file.write('<span style="text-decoration: underline;">')
                    open_underline = True
                else:
                    out_file.write('</span>')
                    open_underline = False
            elif char == '~':
                if not open_italic:
                    out_file.write('<em>')
                    open_italic = True
                else:
                    out_file.write('</em>')
                    open_italic = False
            else:
                out_file.write(char)
        out_file.write('</p>\n')


if __name__ == '__main__':
    main()
