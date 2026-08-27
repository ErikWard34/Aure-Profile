import requests,json,os,re
from pathlib import Path
K=os.environ["SERPAPI_API_KEY"];A="wtQUkJgAAAAJ";U="https://serpapi.com/search.json"
def q(**p):p["api_key"]=K;r=requests.get(U,params=p,timeout=45);r.raise_for_status();return r.json()
arts=q(engine="google_scholar_author",author_id=A,hl="en",sort="pubdate",num=100).get("articles",[])
def pre(a):return any(x in (" ".join([a.get("title",""),a.get("link",""),a.get("publication_info",{}).get("summary","")])).lower() for x in ["preprint","arxiv","biorxiv","medrxiv","ssrn"])
def norm(s):return re.sub(r"\W+","",s.lower())
best={}
for a in arts:
 k=norm(a.get("title",""))
 if k and (k not in best or (pre(best[k]) and not pre(a))):best[k]=a
out=[]
for a in best.values():
 apa=None;rid=a.get("result_id")
 if rid:
  try:apa=next((x["snippet"] for x in q(engine="google_scholar_cite",q=rid,hl="en").get("citations",[]) if x.get("title")=="APA"),None)
  except:pass
 s=a.get("publication_info",{}).get("summary","");m=re.search(r"(?:19|20)\d{2}",s)
 out.append({"title":a.get("title"),"year":int(m.group()) if m else None,"apa":apa or s,"link":a.get("link"),"type":"preprint" if pre(a) else "publication"})
out.sort(key=lambda x:(x["year"] or 0,x["title"] or ""),reverse=True)
Path("data/publications.json").write_text(json.dumps({"publications":out},ensure_ascii=False,indent=2),encoding="utf-8")
