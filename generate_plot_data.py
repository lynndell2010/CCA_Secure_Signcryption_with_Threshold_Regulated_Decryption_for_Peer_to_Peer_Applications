"""Regenerate numerical figure inputs and summary statistics from supplied data."""
import csv
import hashlib
import json
import statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
OUT=ROOT/'figures'

def write(name,columns,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(exist_ok=True)
    inputs=['benchmark_current_3_2.json','benchmark_current_5_3.json','benchmark_current_p2p.json']
    groups=[json.loads((DATA/f).read_text()) for f in inputs[:2]]
    assert all(g.get('complete') and g['trials']==5 for g in groups), 'incomplete experiment'
    summary=[]; outputs=[]
    for tag,size in [('1kb',1024),('1mb',1048576)]:
        rows=[];comparison=[]
        for g in groups:
            ours=[r for r in g['samples'] if r['message_bytes']==size]
            base=[r for r in g['baseline_samples'] if r['message_bytes']==size]
            assert len(ours)==len(base)==g['trials']
            assert all(r['proof_bytes']>0 for r in ours)
            means={k:statistics.mean(r[k] for r in ours) for k in ['signcrypt','regulator','receiver','contributions','certificate_issue','prove','issuance_verify']}
            rows.append(dict(n=g['n'],t=g['t'],auth=means['certificate_issue'],tvrf=means['contributions'],
                signcrypt=means['signcrypt'],receiver=means['receiver'],regulator=means['regulator']))
            for metric in ['signcrypt','receiver','regulator']:
                comparison.append(dict(id=len(comparison)+1,n=g['n'],t=g['t'],metric=metric,
                    baseline=statistics.mean(r[metric] for r in base),ours=means[metric]))
            for kind,samples in [('STRD',ours),('baseline',base)]:
                for metric in (list(means) if kind=='STRD' else ['signcrypt','receiver','regulator']):
                    values=[r[metric] for r in samples]
                    summary.append(dict(n=g['n'],t=g['t'],message_bytes=size,scheme=kind,metric=metric,
                        trials=len(values),mean_ms=statistics.mean(values),std_ms=statistics.stdev(values),min_ms=min(values),max_ms=max(values)))
        name='scheme_'+tag+'.csv';write(name,['t','n','auth','tvrf','signcrypt','receiver','regulator'],rows);outputs.append(name)
        name='threshold_compare_'+tag+'.csv';write(name,['id','n','t','metric','baseline','ours'],comparison);outputs.append(name)
    p2p=json.loads((DATA/inputs[2]).read_text())
    assert len(p2p['results'])==18 and all(len(r['samples'])==50 for r in p2p['results'])
    representative=[r for r in p2p['results'] if (r['n'],r['t']) in [(5,3),(13,7)]]
    name='p2p_emulation.csv'
    write(name,['id','n','t','scenario','mean','p95','successes','bytes'],[
        dict(id=i,n=r['n'],t=r['t'],scenario=r['scenario'],mean=r['mean_ms'],p95=r['p95_ms'],successes=r['successes'],bytes=r['mean_application_bytes'])
        for i,r in enumerate(representative,1)])
    outputs.append(name)
    (DATA/'benchmark_current_summary.json').write_text(json.dumps(summary,indent=2))
    manifest=dict(generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),inputs={f:hashlib.sha256((DATA/f).read_bytes()).hexdigest() for f in inputs},
                  csv={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in outputs})
    (OUT/'current_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
