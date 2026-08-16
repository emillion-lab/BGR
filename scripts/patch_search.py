#!/usr/bin/env python3
# BGR patch #1 — search behaviour (gS + filtering CSS + results counter)
# Idempotent. Marker: BGR-PATCH-SEARCH-v1
import sys, io

PATH = "index.html"
MARK = "BGR-PATCH-SEARCH-v1"

CSS = """
/* ═══ BGR-PATCH-SEARCH-v1 ═══ */
#home.filtering .sect{display:none}
#home.filtering .hero{display:none}
.sres{max-width:900px;margin:10px auto 2px;padding:8px 14px;font:600 12px var(--mn,monospace);
color:var(--ac,#e8a33d);letter-spacing:.4px;text-transform:uppercase}
"""

NEW_GS = """function gS(){
  var box=document.getElementById('q');
  var raw=box.value;
  if(cur){goHome();box.value=raw;}
  var q=raw.trim().toLowerCase();
  var home=document.getElementById('home');
  if(!q){home.classList.remove('filtering');rH(Object.keys(D));return;}
  var res=Object.keys(D).filter(function(k){
    var c=D[k];
    var hay=(k+' '+c.co+' '+c.rgn+' '+c.items.map(function(i){return i.n}).join(' ')).toLowerCase();
    return q.split(/\\s+/).some(function(w){return hay.indexOf(w)!==-1;});
  });
  home.classList.add('filtering');
  rH(res);
  var bar=document.createElement('div');
  bar.className='sres';
  bar.textContent=res.length+' '+L('results');
  home.insertBefore(bar,home.firstChild);
  window.scrollTo(0,0);
}
"""

def main():
    src = io.open(PATH, encoding="utf-8").read()
    if MARK in src:
        print("SKIP: " + MARK + " already applied")
        return 0

    # 1) replace gS() body
    start = src.find("function gS(){")
    if start == -1:
        print("FAIL: gS() not found"); return 1
    end = src.find("\n}\n", start)
    if end == -1:
        print("FAIL: end of gS() not found"); return 1
    src = src[:start] + NEW_GS + src[end + 3:]

    # 2) append CSS to the LAST style block (theme overrides, wins order)
    i = src.rfind("</style>")
    if i == -1:
        print("FAIL: </style> not found"); return 1
    src = src[:i] + CSS + src[i:]

    io.open(PATH, "w", encoding="utf-8").write(src)
    print("OK: search patch applied")
    return 0

sys.exit(main())
