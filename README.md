chordsheet-converter
====================

scripts to process chordsheets and convert them to Ukulele Wednesdays format

this currently takes chordsheets in this format:
```
C               G
  You shout it out
    Am
but I can't hear a word you say
C               G              Am
  I'm talking loud not saying much
```
and producing this:
```
(C)  You shout it o(G)ut
but (Am)I can't hear a word you say
(C)  I'm talking lo(G)ud not saying m(Am)uch
```
so far this consists of a python script to process files.

Eventually it will output into multiple formats, hopefully including

    * ReST (intended to be the primary output format, convertible to...)
    * HTML
    * PDF
    * RTF

And possibly ODT and/or MS Word

Eventually I'll add support for other formats too (chordpro, for example)
and probably also a limited chordshape rendering, although I think that's much harder work :)

The intention is to wrap this functionality in a web framework, probably DJango, to keep track of songs submitted and make submission simpler (auto-emailing admins etc)
