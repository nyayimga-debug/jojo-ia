import json,re,statistics as st,datetime as dt,sys
from ytapi import get
def dur(d):
    m=re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',d); return sum(int(x or 0)*f for x,f in zip(m.groups(),(3600,60,1)))
NOW=dt.datetime(2026,10,12)
def chstats(cids,C):
    out={}
    for cid in cids:
        try: pl=get('playlistItems',part='contentDetails',playlistId='UU'+cid[2:],maxResults=50)
        except Exception: continue
        ids=[x['contentDetails']['videoId'] for x in pl.get('items',[])]
        if not ids: continue
        vs=get('videos',part='statistics,snippet,contentDetails',id=','.join(ids))['items']
        lng=[(int(v['statistics'].get('viewCount',0)),dur(v['contentDetails']['duration']),v['snippet']['publishedAt'][:10],v['snippet']['title'],v['id']) for v in vs if dur(v['contentDetails']['duration'])>=480 and (NOW-dt.datetime.fromisoformat(v['snippet']['publishedAt'][:10])).days>=7]
        if not lng: continue
        ks=sorted(x[0] for x in lng)
        b=max(lng)
        out[cid]=dict(n=len(lng),med=int(st.median(ks)),p25=ks[int(.25*(len(ks)-1))],s100=round(100*sum(k>=1e5 for k in ks)/len(ks)),dur=int(st.median(x[1] for x in lng)/60),best=b[3],bestk=b[0],bestid=b[4],titles=[x[3] for x in sorted(lng,key=lambda x:x[2])[-5:]],first=min(x[2] for x in lng),last=max(x[2] for x in lng))
    return out
if __name__=='__main__':
    raw=json.load(open(sys.argv[1])); C=raw['ch']; V=raw['vids']
    since=sys.argv[3]
    cand=[c for c,v in C.items() if v['created']>=since and any(x['ch']==c and x.get('k',0)>=int(sys.argv[4]) for x in V.values())]
    print(len(cand),'candidates',file=sys.stderr)
    S=chstats(cand,C)
    json.dump(S,open(sys.argv[2],'w'),ensure_ascii=False); print(len(S))
