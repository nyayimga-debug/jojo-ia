import json,sys
from ytapi import get
Q={'de':{
'doctor_seniors':["Arzt warnt ab 60","Gesundheit Senioren Arzt erklärt"],
'nurse':["Krankenschwester verrät","Palliativ was Sterbende sagen"],
'nutrition_food':["Lebensmittel ab 60 essen","ab 60 jeden Morgen essen"],
'grandma_cooking':["Omas alte Rezepte","Rezepte aus der Nachkriegszeit"],
'grandma_wisdom':["wie unsere Großeltern sparten","Oma Tipps von früher"],
'pastor_bible':["Predigt Trost Senioren","was passiert nach dem Tod Bibel"],
'psychology_aging':["Psychologe Einsamkeit im Alter","Weisheit im Alter Lebensweisheiten"],
'retirement_money':["Rentner Fehler Rente","Rente Tipps Geld Rentner"],
'farmer_garden':["alter Gärtner Tipps","Garten Tricks von früher"],
'carpenter_diy':["alter Schreiner Trick","Handwerker Trick von früher"],
'amish':["Amish Geheimnis","Amish Leben sparen"],
'lawyer_legal':["Anwalt erklärt Erbe Fehler","Vorsorgevollmacht Fehler Senioren"],
'cop_veteran':["Ex Polizist verrät","Einbruch Tipps Polizist"],
'japanese_wisdom':["japanische Oma Geheimnis","japanische Langlebigkeit Gewohnheiten"],
'pets_vet':["Tierarzt warnt Hundebesitzer","Hund Fehler Tierarzt"],
'funeral_death':["Bestatter verrät","was passiert beim Sterben"],
'sleep_health':["schlafen ab 60","was passiert mit deinem Körper wenn du"],
'cleaning_home':["Haushaltstricks von früher","Oma Putztricks"],
'survival_prep':["Notvorrat anlegen Liste","Vorräte für die Krise"],
'real_estate':["Haus verkaufen im Alter Fehler","Immobilienmakler verrät"],
'fitness_seniors':["Übungen ab 70","Gehen ab 60 Fehler"],
'relationships_aging':["erwachsene Kinder melden sich nicht","undankbare Kinder im Alter"],
'history_storyteller':["Leben in den 50er Jahren Deutschland","Alltag früher DDR Kindheit"],
'beauty_aging':["Mode ab 60 Frauen","Hautpflege ab 60"]},
'fr':{
'doctor_seniors':["médecin seniors après 60 ans","cardiologue alerte seniors"],
'nurse':["infirmière révèle","soins palliatifs ce que disent les mourants"],
'nutrition_food':["aliments à manger après 60 ans","manger chaque matin après 60 ans"],
'grandma_cooking':["recettes de grand-mère d'autrefois","recettes oubliées de nos grands-mères"],
'grandma_wisdom':["astuces de nos grands-parents économiser","ce que faisaient nos grands-parents"],
'pastor_bible':["prédication réconfort personnes âgées","que se passe-t-il après la mort bible"],
'psychology_aging':["psychologue solitude vieillesse","sagesse de la vieillesse leçons de vie"],
'retirement_money':["retraite erreurs à éviter retraités","retraite conseils argent"],
'farmer_garden':["vieux jardinier astuces","astuces potager des anciens"],
'carpenter_diy':["vieux menuisier astuce","astuce bricolage des anciens"],
'amish':["secret des amish","mode de vie amish économiser"],
'lawyer_legal':["notaire explique succession erreurs","héritage erreurs à éviter"],
'cop_veteran':["ancien policier révèle","cambriolage conseils policier"],
'japanese_wisdom':["grand-mère japonaise secret","longévité japonaise habitudes"],
'pets_vet':["vétérinaire alerte propriétaires de chien","erreurs chien vétérinaire"],
'funeral_death':["croque-mort révèle","que se passe-t-il quand on meurt"],
'sleep_health':["sommeil après 60 ans","ce qui arrive à votre corps si"],
'cleaning_home':["astuces ménage de grand-mère","astuces ménage d'autrefois"],
'survival_prep':["provisions à stocker crise","réserves alimentaires liste"],
'real_estate':["vendre sa maison à la retraite erreurs","agent immobilier révèle"],
'fitness_seniors':["exercices après 70 ans","marcher après 60 ans erreurs"],
'relationships_aging':["enfants adultes ingrats","quand vos enfants vous ignorent"],
'history_storyteller':["la vie dans les années 50 en France","souvenirs de la France d'autrefois"],
'beauty_aging':["mode après 60 ans femme","soins de la peau après 60 ans"]}}
lg=sys.argv[1]; V={}
REG={'de':'DE','fr':'FR'}
for arch,qs in Q[lg].items():
    for q in qs:
        for dur in ('medium','long'):
            try: r=get('search',part='snippet',q=q,type='video',maxResults=50,order='viewCount',relevanceLanguage=lg,regionCode=REG[lg],videoDuration=dur,publishedAfter='2026-01-01T00:00:00Z')
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
json.dump({'vids':V,'ch':C},open(lg+'_raw.json','w'),ensure_ascii=False)
print(len(V),len(C))
