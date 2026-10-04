"""Print full abstracts of records sent to full text (records.csv ta_decision=FT), in batches.
Usage: python3 ft_dump.py <rawdir> <batch> <size>"""
import csv, json, os, sys
RAW, b, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
recs = {r["id"]: r for r in json.load(open(os.path.join(RAW, "merged.json")))}
ft = [r["id"] for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(RAW)), "records.csv"))) if r["ta_decision"] == "FT"]
for i in ft[b * n:(b + 1) * n]:
    r = recs[i]
    print(f'## {i} | {r["year"]} | {r["title"]}\n{(r["abstract"] or "")[:1100]}\n')
print(f"-- ft batch {b}: {len(ft[b*n:(b+1)*n])} of {len(ft)}")
