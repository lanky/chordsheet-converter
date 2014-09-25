#!/usr/bin/env python
import re
# import os
import sys
from optparse import OptionParser

# chords are
# A-G #|b min|maj possibly followed by 5/6/7/9/13
# A-G #|b sus followed by 2 or 4
# A-G #|b aug|dim followd by nothing
# A-G #|b <nothing>

    
CRD = re.compile(r"\b((?:[A-G])(?:#|b)?(?:m|maj|sus)?(?:[0-9]+)?(?:/[A-G](?:#|b)?)?)\b")


def parse_args(argv):
    """
    Process commandline options and arguments
    """
    usage = """%prog [-a ARTIST] [ -t TITLE] CHORDSHEET
Process a chordsheet in ultimate-guitar format (chords above lyrics).
Produce a chordsheet in UW format
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--artist", help="Artist Name")
    parser.add_option("-t", "--title", help="Song title")
    parser.add_option("-c", "--chord-marker", default="(%s)",
        help="python string expansion expression for wrapping chords when found. Default: '%default'")
    
    opts, args = parser.parse_args(argv)

    if len(args) != 1:
        print "ERROR: must provide a chordsheet file to process"
        sys.exit(1)

    return opts, args[0]

def insert_chords(chordline, lyricline, chordpatt="(%s)"):
    """
    process a chordline, using RE to find matches.
    Inserts those matches into the lyricline provided
    returns the combined string

    Args:
        chordline(str): line of whitespace-separated chords 
        lyricline(str): line of lyrics to which they apply
    Kwargs:
        chordpatt(str): string replacement pattern for inserting chords.
                        defaults to (%s) - chord with () around it
    """
    outparts = []
    # start at the beginning of the line
    curpos = 0
    for crd in CRD.finditer(chordline):
        # where on the line does the chord go?
        m = crd.start()
        chordstr = chordpatt % crd.groups()[0]
        outparts.append("%s%s" %(lyricline[curpos:m], chordstr))
        # next time we start at this chord's position
        curpos = m
    # anything after the final match needs appending, also.
    outparts.append(lyricline[curpos:])
    return ''.join(outparts)

# ideally, what we want to achieve
# walk each line in input
# if it matches our chordline pattern:
# - check the next line.
# -  if that matches chords also, we're probably in an instrumental section
#    so add the current line as-is to output
#    if it doesn't, we'll consume it as a lyric line
# if it doesn't match or is blank, add it to output.
# 
# could work with a while len(lines) loop?
# and pop(0)

def process_lines(chordlines, chordpattern="(%s)"):
    """
    an attempt to preserve blank lines
    """
    output = []
    chordrepl = chordpattern % r'\\1'
    while len(chordlines) > 0:
        # pull out the first line
        curline = chordlines.pop(0)
        # preserve blank lines
        if curline.strip() == '':
            output.append(curline)
            continue
        # is it a chord line?
        elif CRD.search(curline) is not None:
            nextline = chordlines.pop(0)
            # is the next line chords too?
            if CRD.search(nextline) is not None:
                crds = CRD.sub(chordrepl, curline)
                output.append(crds)
                # put the next line back on the pile
                chordlines.insert(0, nextline)
            else:
                newline = insert_chords(curline, nextline, chordpatt=chordpattern)
                output.append(newline)
                continue
        else:
            output.append(curline)
            continue
    return output




def main():
    opts, chordsheet = parse_args(sys.argv[1:])
    try:
        data = open(chordsheet).read().splitlines()
        # let's record which lines contain chords and see if 
        # we can insert them appropriately on the following lines

        output = process_lines(data, chordpattern=opts.chord_marker)

        print '\n'.join(output)

    except (IOError, OSError), Err:
        print "cannot open %s (%s)" % (sys.argv[1], Err.strerror)
        raise


if __name__ == "__main__":
    main()

