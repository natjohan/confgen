#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, csv
from jinja2 import Environment, FileSystemLoader
from io import open

__author__ = u'@natjohan'
__credits__= u'KISS philosophy : Keep it Simple, Stupid'

def dieWith(msg) :
    sys.stderr.write(u'Ooops ' + unicode(msg) + u'\n :( \n')
    sys.exit(-1)

def readCSV(input_file, csv_delimiter):
    file = open(input_file.name) # , encoding='utf-8')
    try:
        data = [row for row in csv.DictReader(file, delimiter=csv_delimiter)]
    except Exception, e:
        dieWith(e)
    finally:
        file.close()
    return data

def readTemplate(file):
    env = Environment(loader=FileSystemLoader(u''), newline_sequence=u'\n')
    #if template == 'stdin' :
    #    file = sys.stdin
    #else:
    #    file = open(template)
    template = env.get_template(file.name)
    return template


def main():
    parser = argparse.ArgumentParser(description=u'This script will populate a Jinja2 template \
     ((http://jinja.pocoo.org/docs/) with some input data (CSV format) and output\
      one entire file or one file per line.\n ', epilog=u'-- twitter: @natjohan -- contact@natjohan.info')

    parser.add_argument(u'-v',u'--version', action=u'version', version=u'%(prog)s 0.3 beta')
    parser.add_argument(u'-i',u'--input', help=u'Input file name CSV', type=argparse.FileType(u'rt'), required=True)
    parser.add_argument(u'-t',u'--template', help=u'Your template file', type=argparse.FileType(u'rt'), required=True)
    parser.add_argument(u'-d',u'--delimiter', help=u'Delimiter for your CSV file, default is ;', default=u';')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(u'-so',u'--simpleoutput',help=u'Output file name, stdout if not specified', nargs=u'?', const=u'stdout')
    group.add_argument(u'-mo',u'--multipleoutput',help=u'Generate one file per line, you must specify the\
     name of the column where are the names of files to generate, stdout if not specified', nargs=u'?', const=u'stdout')

    parser.add_argument(u'-a',u'--append', help=u'Appending the output to the end of the file if it exists',\
     nargs=u'?', choices=[u'w', u'a'], const=u'a', default=u'w')

    args = parser.parse_args()
     
    # Show values
    print u"-----------------------------------------\n"
    print u"Input file : %s" % args.input.name
    print u"Template file : %s" % args.template.name
    print u"Delimiter : %s \n" % args.delimiter
    print u"-----------------------------------------\n"

    # Read CSV data & template
    data = readCSV(args.input, args.delimiter)
    template = readTemplate(args.template)

    output_from_template = u''
    # For outputting in a single file
    if args.simpleoutput :
        for row in data :
            output_from_template += unicode(template.render(row)) + u'\n'
        
        if args.simpleoutput == u'stdout' :
            out = sys.stdout
            out.write(output_from_template)
        else :
            out = open(args.simpleoutput, args.append)
            out.write(output_from_template)
            sys.stderr.write(u'*** File %s was generated ***\n' % args.simpleoutput)

    # For outputting in multiple files
    else :
        if args.multipleoutput == u'stdout' :
            for row in data :
                output_from_template += unicode(template.render(row)) + u'\n'
            out = sys.stdout
            out.write(output_from_template)
        else :
            counter = 0
            for row in data :
                output_from_template = template.render(row)
                outFilename = row[unicode(args.multipleoutput)]
                out = open(outFilename, args.append)
                out.write(output_from_template)
                counter += 1
                sys.stderr.write(u'File %s was generated \n' % outFilename )
            sys.stderr.write(u'\n *** Good job my buddy ! %s Files were generated *** \n' % counter)
