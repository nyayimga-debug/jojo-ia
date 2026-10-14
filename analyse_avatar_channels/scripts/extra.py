import json,sys
from ytapi import get
Q={'de':{
'butcher_grocery':["Metzger verrät Fleisch günstig","Supermarkt Tricks sparen Insider"],
'collectibles':["wertvolle Dinge auf dem Dachboden","alte Sachen die viel Geld wert sind"],
'travel_seniors':["Reisen ab 60 Tipps","Bahn fahren Senioren Tipps"],
'camping_fishing':["Angeln Tipps alter Angler","Camping Tricks von früher"],
'trucking':["LKW Fahrer erzählt","Berufskraftfahrer Tipps"],
'plumbing_repair':["Klempner verrät","Schimmel entfernen Hausmittel"],
'decluttering':["Ausmisten im Alter","Döstädning schwedisch aufräumen"],
'style_oldmoney':["Old Money Stil Männer","Stil Fehler Frauen über 60"],
'birds':["Vögel füttern Winter Fehler","Vogelfutter Tipps"],
'frugal':["Spartipps von Oma","sparsam leben Rentner"]},
'fr':{
'butcher_grocery':["boucher révèle viande pas chère","astuces supermarché économiser"],
'collectibles':["objets de valeur dans le grenier","vieux objets qui valent de l'argent"],
'travel_seniors':["voyager après 60 ans conseils","croisière seniors astuces"],
'camping_fishing':["astuces pêche vieux pêcheur","astuces camping d'autrefois"],
'trucking':["routier raconte","chauffeur poids lourd conseils"],
'plumbing_repair':["plombier révèle","enlever moisissure astuce"],
'decluttering':["désencombrer après 60 ans","rangement suédois avant de mourir"],
'style_oldmoney':["style old money homme","erreurs de style après 60 ans"],
'birds':["nourrir les oiseaux en hiver erreurs","mangeoire oiseaux conseils"],
'frugal':["astuces d'économie de grand-mère","vivre avec peu retraite économiser"]}}
REG={'de':'DE','fr':'FR'}
for lg in ('de','fr'):
    raw=json.load(open(f'../data/{lg}_raw.json')); V=raw['vids']; C=raw['ch']; new=set()
    for arch,qs in Q[lg].items():
        for q in qs:
            for dur in ('medium','long'):
                r=get('search',part='snippet',q=q,type='video',maxResults=50,order='viewCount',relevanceLanguage=lg,regionCode=REG[lg],videoDuration=dur,publishedAfter='2026-01-01T00:00:00Z')
                for it in r.get('items',[]):
                    vid=it['id']['videoId']
                    if vid not in V: V[vid]={'arch':arch,'q':q,'ch':it['snippet']['channelId'],'t':it['snippet']['title']}; new.add(vid)
        print(lg,arch,len(new),file=sys.stderr)
    ids=list(new)
    for i in range(0,len(ids),50):
        for it in get('videos',part='statistics,snippet',id=','.join(ids[i:i+50]))['items']:
            V[it['id']].update(k=int(it['statistics'].get('viewCount',0)),al=it['snippet'].get('defaultAudioLanguage',''),pub=it['snippet']['publishedAt'][:10])
    chs=list({v['ch'] for v in V.values()}-set(C))
    for i in range(0,len(chs),50):
        for it in get('channels',part='snippet,statistics',id=','.join(chs[i:i+50]))['items']:
            C[it['id']]={'t':it['snippet']['title'],'h':it['snippet'].get('customUrl',''),'created':it['snippet']['publishedAt'][:10],'country':it['snippet'].get('country',''),'subs':int(it['statistics'].get('subscriberCount',0)),'views':int(it['statistics'].get('viewCount',0)),'nv':int(it['statistics'].get('videoCount',0)),'desc':it['snippet'].get('description','')[:700]}
    json.dump({'vids':V,'ch':C},open(f'../data/{lg}_raw.json','w'),ensure_ascii=False)
    print(lg,'done',len(V),len(C),file=sys.stderr)
