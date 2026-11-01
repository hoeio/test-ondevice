"""Rebuild data/ko.txt: first 300 rows of Korean Wikipedia (wikimedia/wikipedia, config 20231101.ko, split train),
keeping articles longer than 1500 characters, joined by blank lines."""
import json, sys, urllib.request
out = []
for off in range(0, 300, 100):
    url = ("https://datasets-server.huggingface.co/rows?dataset=wikimedia/wikipedia"
           f"&config=20231101.ko&split=train&offset={off}&length=100")
    out += [r["row"]["text"] for r in json.load(urllib.request.urlopen(url))["rows"]]
open(sys.argv[1] if len(sys.argv) > 1 else "data/ko.txt", "w").write("\n\n".join(x for x in out if len(x) > 1500))
