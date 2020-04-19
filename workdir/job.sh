#! /bin/bash
for i in samples/*.frag; do
    file="$(cut -d'/' -f2 <<<"$i")"
    filename="$(cut -d'.' -f1 <<<"$file")"
    echo "$filename"
    python main.py "$i" > out/"$filename".out || break
done