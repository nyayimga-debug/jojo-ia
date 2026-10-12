import json,sys,re,statistics as st,datetime as dt,time
from ytapi import get
A={
'doctor_seniors':["doctor warns seniors over 60","retired doctor reveals","cardiologist warns over 70"],
'nurse':["retired nurse reveals","hospice nurse what dying patients"],
'nutrition_food':["foods seniors should eat","eat this every morning over 60","nutritionist warns seniors"],
'grandma_cooking':["grandma cooking old recipes","depression era recipes grandma","old fashioned recipes nobody makes"],
'grandma_wisdom':["grandma old ways frugal","old timers frugal tips","things grandparents did"],
'pastor_bible':["pastor sermon seniors","bible teaching heaven","christian prayer elderly"],
'psychology_aging':["psychologist explains aging","stoic advice old age","why old people become lonely"],
'retirement_money':["retirement mistakes retiree","social security mistakes","retired couple advice"],
'farmer_garden':["old farmer gardening tips","old gardener secret","homestead old timer"],
'mechanic_cars':["old mechanic secrets","retired mechanic reveals"],
'carpenter_diy':["old carpenter trick","old builder secret"],
'amish':["amish secret","amish way of life money"],
'lawyer_legal':["lawyer explains seniors","estate attorney warns","what to never sign elderly"],
'cop_veteran':["retired cop reveals","veteran survival tips","navy seal secret"],
'japanese_wisdom':["japanese grandma secret","japanese longevity habits","okinawa elderly"],
'pets_vet':["veterinarian warns dog owners","dog trainer secret old"],
'funeral_death':["funeral director reveals","what happens when you die doctor"],
'sleep_health':["sleep doctor over 60","what happens to your body if"],
'cleaning_home':["old cleaning tricks grandma","housekeeping tips old fashioned"],
'survival_prep':["prepping food storage old timer","survival items to stockpile"],
'real_estate':["realtor warns buyers","downsizing seniors house"],
'fitness_seniors':["exercise over 70 physical therapist","walking after 60 mistakes"],
'relationships_aging':["adult children ungrateful elderly","narcissist mother elderly","when your children ignore you"],
'history_storyteller':["old man tells story 1950s","life in the 1960s remember"],
'beauty_aging':["skin care over 60 dermatologist","women over 60 style"],
}
V={}
for arch,qs in A.items():
    for q in qs:
        for dur in ('medium','long'):
            try: r=get('search',part='snippet',q=q,type='video',maxResults=50,order='viewCount',relevanceLanguage='en',regionCode='US',videoDuration=dur,publishedAfter='2026-05-01T00:00:00Z')
            except SystemExit: print('QUOTA',file=sys.stderr); break
            for it in r.get('items',[]): V.setdefault(it['id']['videoId'],{'arch':arch,'q':q,'ch':it['snippet']['channelId'],'t':it['snippet']['title']})
    print(arch,len(V),file=sys.stderr)
ids=list(V)
for i in range(0,len(ids),50):
    for it in get('videos',part='statistics,snippet',id=','.join(ids[i:i+50]))['items']:
        V[it['id']].update(k=int(it['statistics'].get('viewCount',0)),al=it['snippet'].get('defaultAudioLanguage',''),pub=it['snippet']['publishedAt'][:10])
chs=list({v['ch'] for v in V.values()});C={}
for i in range(0,len(chs),50):
    for it in get('channels',part='snippet,statistics',id=','.join(chs[i:i+50]))['items']:
        C[it['id']]={'t':it['snippet']['title'],'h':it['snippet'].get('customUrl',''),'created':it['snippet']['publishedAt'][:10],'country':it['snippet'].get('country',''),'subs':int(it['statistics'].get('subscriberCount',0)),'views':int(it['statistics'].get('viewCount',0)),'nv':int(it['statistics'].get('videoCount',0)),'desc':it['snippet'].get('description','')[:700]}
json.dump({'vids':V,'ch':C},open('us_raw.json','w'),ensure_ascii=False)
print(len(V),len(C))
