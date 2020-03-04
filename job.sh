#! /bin/bash
echo "comment"
python lex_analyzer.py samples/comment.frag > out/comment.out
echo "ident"
python lex_analyzer.py samples/ident.frag > out/ident.out
echo "number"
python lex_analyzer.py samples/number.frag > out/number.out
echo "reserve_op"
python lex_analyzer.py samples/reserve_op.frag > out/reserve_op.out
echo "string"
python lex_analyzer.py samples/string.frag > out/string.out
echo "program"
python lex_analyzer.py samples/program.decaf > out/program.out
echo "badbool"
python lex_analyzer.py samples/badbool.frag > out/badbool.out
echo "badreserve"
python lex_analyzer.py samples/badreserve.frag > out/badreserve.out
echo "badint"
python lex_analyzer.py samples/badint.frag > out/badint.out
echo "badstring"
python lex_analyzer.py samples/badstring.frag > out/badstring.out
echo "badop"
python lex_analyzer.py samples/badop.frag > out/badop.out
echo "badident"
python lex_analyzer.py samples/badident.frag > out/badident.out
echo "baddouble"
python lex_analyzer.py samples/baddouble.frag > out/baddouble.out