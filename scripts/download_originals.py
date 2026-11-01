from huggingface_hub import hf_hub_download as d
L=[("bartowski/Llama-3.2-1B-Instruct-GGUF","Llama-3.2-1B-Instruct-Q8_0.gguf"),
("bartowski/Llama-3.2-3B-Instruct-GGUF","Llama-3.2-3B-Instruct-Q8_0.gguf"),
("unsloth/gemma-3-1b-it-GGUF","gemma-3-1b-it-Q8_0.gguf"),
("TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF","tinyllama-1.1b-chat-v1.0.Q8_0.gguf"),
("LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct-GGUF","EXAONE-3.5-2.4B-Instruct-Q8_0.gguf"),
("mradermacher/stablelm-3b-4e1t-GGUF","stablelm-3b-4e1t.Q8_0.gguf"),
("TheBloke/Mistral-7B-v0.1-GGUF","mistral-7b-v0.1.Q8_0.gguf")]
for r,f in L:
    for i in range(6):
        try: d(r,f,local_dir="orig"); break
        except Exception as e: print("retry",f,e,flush=True)
    else: print("FAILED",f,flush=True)
