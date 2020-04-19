#! /bin/bash
for i in samples/*.out; do
    file="$(cut -d'/' -f2 <<<"$i")"
    filename="$(cut -d'.' -f1 <<<"$file")"
    echo "$filename"
    diff -w out/"$filename".out "$i" || break
done