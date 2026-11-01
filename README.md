# woobinpeekaboo models vs. original models

Perplexity and CPU speed comparison of the 10 GGUF files in the Hugging Face account `WoobinPeekaboo` (`Ollie`, `Spicy`)
against the public Q8_0 GGUF of each base model. Results: [report.md](report.md). Raw numbers: `results.txt` (woobinpeekaboo), `results_orig.txt` (originals).

## Setup used for the reported numbers
* llama.cpp `8642541b2` (build 11960; Homebrew `llama.cpp` 0.8.0, `ggml` 0.28.0), Apple M4 Pro, macOS 15.
* **CPU only** (`-dev none -ngl 0`; the Metal backend failed to compile its shaders on this machine), context **512**, first **30 chunks**.
* English text: WikiText-2 test (`wiki.test.raw`). Korean text: `data/ko.txt` (see `data/README.md` for source and license).
* Speed: `llama-bench -p 128 -n 32 -r 2`.

## Reproduce
```bash
pip install huggingface_hub gguf          # needs llama.cpp tools: brew install llama.cpp
export HF_TOKEN=...                        # your Hugging Face token; never commit it
mkdir -p models data
python3 -c "from huggingface_hub import snapshot_download as s; [s('WoobinPeekaboo/'+r, local_dir='models/'+r) for r in ['Ollie','Spicy']]"
python3 scripts/download_originals.py      # original Q8_0 files into orig/
curl -L https://huggingface.co/datasets/ggml-org/ci/resolve/main/wikitext-2-raw-v1.zip -o data/wt.zip && unzip -o data/wt.zip -d data
for f in models/*/*.gguf; do ./run_ppl.sh $f; done      # appends to results.txt
for f in orig/*.gguf;    do ./run_orig.sh $f; done      # appends to results_orig.txt
```
Each line is `file|PPL EN|PPL KO|prefill tok/s|decode tok/s`.
Original Q8_0 sources (see `scripts/download_originals.py`): `bartowski/Llama-3.2-1B-Instruct-GGUF`, `bartowski/Llama-3.2-3B-Instruct-GGUF`,
`unsloth/gemma-3-1b-it-GGUF`, `TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF`, `LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct-GGUF`,
`mradermacher/stablelm-3b-4e1t-GGUF`, `TheBloke/Mistral-7B-v0.1-GGUF`.

## Limits
* Perplexity uses 30 chunks of 512 tokens per text (about 15k tokens each), so differences of a few percent are within sampling noise (the logged standard error is about 0.3 to 1.7 PPL).
* The reference is the public **Q8_0** file of each original, not FP16. "Change vs original" is relative to a Q8_0 model.
* Perplexity is only compared between a file and its own original (same tokenizer). Several originals are instruct/chat models scored on raw Wikipedia text.
* The base model of `spicy.gguf` is identified from tensor shapes (no metadata); the reference used is Mistral-7B-v0.1.

## Mac speed columns
The Mac decode numbers are reported as measured, and they contradict the file-size trend in places (for example `ollie_english120` 98 tok/s vs 118 for the original Gemma Q8_0, `ollie_english2` 45 vs 106). Do not read these as a property of the compressed models:
* Load was not controlled during these runs. The woobinpeekaboo files were benchmarked while the original downloads were also running, the originals afterwards, so the two columns were not measured under the same conditions.
* Decode on CPU depends on the quantization kernel, not only on bytes read. Q8_0 and Q4_0 have simple integer kernels; Q4_K/Q6_K/Q3_K need more dequantization work per weight. In the data the Q4_0 files (`ollie_korean2` 74, `ollie_korean121` 98 tok/s) are faster than the Q4_K/Q6_K files of the same model (48, 47 tok/s), which fits this.
To get clean Mac numbers, run `./bench.sh <file>` on every file with nothing else running and replace the Mac columns.

## Changes
* References to the TinyLlama finetune's content type were removed; it is listed as a TinyLlama-1.1B chat finetune.
* Korean evaluation text, rebuild script, source and license added (`data/`, `scripts/make_ko.py`).
* Early-2025 test results are added to the repository separately; the numbers in `report.md` are the November 2026 runs.

## Licenses
`data/ko.txt`: CC BY-SA 4.0 (Korean Wikipedia). Model files are governed by their own licenses (Llama 3.2, Gemma, EXAONE, Apache-2.0 and others) and are not stored in this repository.
