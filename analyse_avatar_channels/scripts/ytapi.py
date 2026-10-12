# Petit client YouTube Data API v3 avec rotation de clés.
# Les clés ne sont jamais dans le dépôt : export YT_KEYS="cle1,cle2,cle3"
import json,os,time,urllib.request,urllib.parse
KEYS=[k.strip() for k in os.environ.get('YT_KEYS','').split(',') if k.strip()]
ki=0
def get(ep,**p):
    global ki
    if not KEYS: raise SystemExit('YT_KEYS manquant')
    for att in range(len(KEYS)*3):
        p['key']=KEYS[ki]
        u='https://www.googleapis.com/youtube/v3/'+ep+'?'+urllib.parse.urlencode(p)
        try: return json.load(urllib.request.urlopen(u,timeout=30))
        except urllib.error.HTTPError as e:
            if e.code in (403,429): ki=(ki+1)%len(KEYS); time.sleep(1); continue
            raise
        except Exception: time.sleep(2)
    raise SystemExit('quota')
