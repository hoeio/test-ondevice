# My lightweighted models vs. original models

Hugging Face account `WoobinPeekaboo`: 2 repos (`Ollie`, `Spicy`), 10 GGUF files, 19.6 GB. Base models were identified from GGUF metadata (architecture, layer/width/vocab shape, base_model fields). None of the models is Qwen. `spicy.gguf` is a Mistral-7B-shaped Llama model. Each model was compared with its original, downloaded as the public Q8_0 GGUF: TinyLlama-1.1B-Chat-v1.0, gemma-3-1b-it, Llama-3.2-1B-Instruct, stablelm-3b-4e1t, Llama-3.2-3B-Instruct, EXAONE-3.5-2.4B-Instruct and Mistral-7B-v0.1.

## Test dates
Some of the tests on these models are from early 2025, and a few were retested in late 2026. The results in this report are the late-2026 retests (November 2026). The early-2025 results are added to this repository separately.

## Method
Both sides were measured identically on a Mac (Apple M4 Pro, CPU, llama.cpp):
* **Perplexity, English:** WikiText-2 test, context 512, first 30 chunks.
* **Perplexity, Korean:** Korean Wikipedia sample, same settings.
* **Decode speed:** `llama-bench` tg32 (32 generated tokens) on the Mac, CPU only.

Lower perplexity is better; "change" is the woobinpeekaboo value relative to the original (negative = better). Perplexity is compared only between a model and its own original, which share a tokenizer.

## Quality and size
| Model file | Base model | Quant | Size GB | Original Q8_0 GB | Size saved | PPL EN | Original PPL EN | EN change | PPL KO | Original PPL KO | KO change |
|---|---|---|
| ollie_english | TinyLlama-1.1B (chat finetune) | Q8_0 | 1.17 | 1.17 | 0% | 7.95 | 18.68 | -57% | 4.44 | 4.29 | +3% |
| ollie_english120 | Gemma-3-1B-it | Q4/Q5/Q8 mix | 0.81 | 1.07 | 25% | 26.52 | 25.94 | +2% | 19.32 | 18.00 | +7% |
| ollie_english2 | Llama-3.2-1B (FuseChat) | Q4_K/Q6_K | 0.81 | 1.32 | 39% | 18.08 | 13.95 | +30% | 27.25 | 20.82 | +31% |
| ollie_english3 | StableLM-3B (HelpingAI) | Q4_K/Q6_K | 1.71 | 2.97 | 43% | 47.85 | 8.65 | +453% | 9.02 | 3.41 | +165% |
| ollie_korean | Llama-3.2-3B (Bllossom) | Q4_K/Q6_K | 2.02 | 3.42 | 41% | 10.94 | 10.35 | +6% | 12.39 | 13.95 | -11% |
| ollie_korean2 | Llama-3.2-3B (Bllossom) | Q4_0 | 1.92 | 3.42 | 44% | 11.23 | 10.35 | +8% | 13.88 | 13.95 | -0% |
| ollie_korean3 | Llama-3.2-3B (Bllossom) | Q3_K/Q4_K | 1.69 | 3.42 | 51% | 12.34 | 10.35 | +19% | 14.76 | 13.95 | +6% |
| ollie_korean121 | EXAONE-3.5-2.4B | Q4_0 | 1.58 | 2.84 | 44% | 10.01 | 9.50 | +5% | 8.07 | 7.76 | +4% |
| ollie_korean4 | EXAONE-3.5-2.4B | Q4_K/Q6_K | 1.84 | 2.84 | 35% | 9.73 | 9.50 | +2% | 8.01 | 7.76 | +3% |
| spicy | Mistral-7B | Q8_0 | 7.70 | 7.70 | -0% | 5.69 | 5.48 | +4% | 4.21 | 4.04 | +4% |

## Speed
CPU decode on the Mac. Interpretation of the rows where the compressed file is slower: see "Mac speed columns" in the README.

| Model file | Mac tok/s | Original Mac tok/s |
|---|---|---|
| ollie_english | 108 | 111 |
| ollie_english120 | 98 | 118 |
| ollie_english2 | 45 | 106 |
| ollie_english3 | 37 | 46 |
| ollie_korean | 48 | 29 |
| ollie_korean2 | 74 | 29 |
| ollie_korean3 | 43 | 29 |
| ollie_korean121 | 98 | 50 |
| ollie_korean4 | 47 | 50 |
| spicy | 17 | 17 |

## Findings
* **Size:** eight of the ten files are 25-51% smaller than their original's Q8_0 file; `ollie_english` and `spicy` are Q8_0 themselves.
* **Closest to original quality:** `ollie_english120` (Gemma 3 1B, +2% EN, +7% KO) and `spicy` (Mistral-7B, +4% EN, +4% KO) stay within a few percent of the original while `ollie_english120` is 25% smaller.
* **Bllossom 3B:** Korean perplexity is lower than Llama-3.2-3B-Instruct (13.95) for the Q4_K/Q6_K file (12.39), equal for Q4_0 (13.88) and higher for Q3_K (14.76), reflecting the Korean finetune. English perplexity rises 6-19% as quantization gets coarser (Q4_K/Q6_K 10.94, Q4_0 11.23, Q3_K 12.34 vs 10.35).
* **EXAONE 2.4B:** `ollie_korean4` is +2.4% EN / +3.2% KO against the original at 35% smaller; `ollie_korean121` is +5.4% / +4.0% at 44% smaller and the faster of the two (98 vs 47 tok/s on the Mac).
* **TinyLlama:** `ollie_english` (chat finetune) has lower perplexity than TinyLlama-1.1B-Chat on English (7.95 vs 18.68) and about equal on Korean.
* **Largest quality loss:** `ollie_english3` (HelpingAI-3B) has English perplexity 47.85 against 8.65 for StableLM-3B-4E1T, in exchange for 43% smaller size. `ollie_english2` (FuseChat Llama-3.2-1B) is +30% EN / +31% KO against Llama-3.2-1B-Instruct at 39% smaller.
* **7B:** `spicy` is the best-modelled file (EN 5.69 / KO 4.21) at 7.7 GB, the same size as the original Q8_0.

Files: `run_ppl.sh` and `run_orig.sh` (evaluation scripts), `results.txt` and `results_orig.txt` (raw numbers).
