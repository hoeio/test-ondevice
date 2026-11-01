#!/bin/bash
# usage: run_ppl.sh model.gguf  -> appends "name|en_ppl|ko_ppl|pp|tg" to results.txt
m=$1; n=$(basename $m .gguf)
ppl(){ llama-perplexity -m $m -f $1 -c 512 --chunks 30 -dev none -ngl 0 2>&1 | grep -E "Final estimate" | sed -E 's/.*PPL = ([0-9.]+).*/\1/'; }
en=$(ppl data/wikitext-2-raw/wiki.test.raw); ko=$(ppl data/ko.txt)
b=$(llama-bench -m $m -p 128 -n 32 -dev none -ngl 0 -r 2 -o csv 2>/dev/null | tail -2 | tr -d '"' | awk -F, '{print $(NF-1)}' | paste -sd'|' -)
echo "$n|$en|$ko|$b" >> results.txt
