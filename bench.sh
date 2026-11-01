#!/bin/bash
# CPU-only decode/prefill benchmark on an idle machine. usage: bench.sh model.gguf >> bench_results.txt
m=$1
llama-bench -m "$m" -p 128 -n 32 -dev none -ngl 0 -r 3 -o csv 2>/dev/null | tail -2 | tr -d '"' | awk -F, -v n="$(basename $m .gguf)" '{a[NR]=$(NF-1)} END{print n"|"a[1]"|"a[2]}'
