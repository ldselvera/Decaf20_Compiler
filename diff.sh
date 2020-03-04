#! /bin/bash
# echo "comment"
# diff -w out/comment.out samples/comment.out
# echo "ident"
# diff -w out/ident.out samples/ident.out
# echo "number"
# diff -w out/number.out samples/number.out
# echo "program"
# diff -w out/program.out samples/program.out
# echo "reserve_op"
# diff -w out/reserve_op.out samples/reserve_op.out
# echo "string"
# diff -w out/string.out samples/string.out
# echo "badbool"
# diff -w out/badbool.out samples/badbool.out
# echo "badreserve"
# diff -w out/badreserve.out samples/badreserve.out
# echo "badint"
# diff -w out/badint.out samples/badint.out
# echo "badstring"
# diff -w out/badstring.out samples/badstring.out
# echo "badop"
# diff -w out/badop.out samples/badop.out
# echo "badident"
# diff -w out/badident.out samples/badident.out
# echo "baddouble"
# diff -w out/baddouble.out samples/baddouble.out

for i in samples/*.out; do
    file="$(cut -d'/' -f2 <<<"$i")"
    filename="$(cut -d'.' -f1 <<<"$file")"
    echo "$filename"
    diff -w out/"$filename".out "$i" || break
done