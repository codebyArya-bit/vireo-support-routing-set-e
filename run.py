#!/usr/bin/env python3
import argparse,json
from src.analysis import run
p=argparse.ArgumentParser(description='Vireo offline support analysis')
p.add_argument('--data',default='data',help='Folder containing the five canonical CSVs or supplied UUID-prefixed filenames')
p.add_argument('--out',default='output')
a=p.parse_args();s=run(a.data,a.out)
print(json.dumps({k:s[k] for k in ['tickets','diagnostics','business_case','run_seconds']},indent=2))
