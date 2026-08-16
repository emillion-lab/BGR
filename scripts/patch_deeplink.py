#!/usr/bin/env python3
# BGR patch #2 — deep links (#/Град) + share button
# Idempotent. Marker: BGR-PATCH-DEEPLINK-v1
import sys, io

PATH = "index.html"
MARK = "BGR-PATCH-DEEPLINK-v1"

CSS = """
/* ═══ BGR-PATCH-DEEPLINK-v1 ═══ */
#bgToast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);
background:#1c1c1e;color:#fff;padding:10px 18px;border-radius:22px;font:600 12.5px var(--fn,sans-serif);
opacity:0;pointer-events:none;transition:.22s;z-index:9999;box-shadow:0 4px 18px rgba(0,0,0,.35)}
#bgToast.on{opacity:1;transform:translateX(-50%) translateY(0)}
"""

JS = """
/* ═══ BGR-PATCH-DEEPLINK-v1 ═══ */
function bgHashFor(k){
  return '#/'+encodeURIComponent(k)+(curLang!=='bg'?'|'+curLang:'');
}
function bgSetHash(h){
  try{ if(location.hash!==h) history.replaceState(null,'',h||location.pathname+location.search); }
  catch(e){ location.hash=h; }
}
function bgRoute(){
  var raw=(location.hash||'').replace(/^#\\/?/,'');
  if(!raw) return false;
  var parts=raw.split('|');
  var city;
  try{ city=decodeURIComponent(parts[0]); }catch(e){ city=parts[0]; }
  var lg=parts[1];
  if(lg&&LANG[lg]) curLang=lg;
  if(city&&D[city]){ oC(city); return true; }
  return false;
}
function bgToast(msg){
  var t=document.getElementById('bgToast');
  if(!t){ t=document.createElement('div'); t.id='bgToast'; document.body.appendChild(t); }
  t.textContent=msg; t.classList.add('on');
  clearTimeout(t._h); t._h=setTimeout(function(){ t.classList.remove('on'); },2200);
}
function bgShare(k){
  var url=location.origin+location.pathname+location.search+bgHashFor(k);
  var title=(curLang==='bg'?k:((D[k]&&D[k].co)||k))+' — BulgariaGuide';
  var done=function(){ bgToast(curLang==='bg'?'Линкът е копиран':'Link copied'); };
  if(navigator.share){ navigator.share({title:title,url:url}).catch(function(){}); return; }
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(url).then(done,function(){ window.prompt('URL',url); }); return;
  }
  window.prompt('URL',url);
}
"""

NEW_INIT = """(function init(){try{
  window.addEventListener('hashchange',function(){ if(!bgRoute()) goHome(); });
  if(!bgRoute()) goHome();
}catch(e){setTimeout(init,50);}})();
"""

def main():
    src = io.open(PATH, encoding="utf-8").read()
    if MARK in src:
        print("SKIP: " + MARK + " already applied")
        return 0

    # 1) share link in the city header, next to Google Maps / TripAdvisor
    anchor = "\u2b50 TripAdvisor</a></div></div>';"
    if anchor not in src:
        print("FAIL: city header link block not found"); return 1
    share = ("\u2b50 TripAdvisor</a>'"
             "+'<a href=\"#\" onclick=\"bgShare(\\''+k.replace(/'/g,\"\\\\'\")+'\\');return false;\">"
             "\U0001f517 '+(curLang==='bg'?'\u0421\u043f\u043e\u0434\u0435\u043b\u0438':'Share')+'</a>"
             "</div></div>';")
    src = src.replace(anchor, share, 1)

    # 2) hash write on city open
    a = "function oC(k){\n  cur=k;curF=null;curSF=null;"
    if a not in src:
        print("FAIL: oC() head not found"); return 1
    src = src.replace(a, a + "\n  bgSetHash(bgHashFor(k));", 1)

    # 3) hash clear on home
    b = "function goHome(){\n  cur=null;curF=null;curSF=null;"
    if b not in src:
        print("FAIL: goHome() head not found"); return 1
    src = src.replace(b, b + "\n  bgSetHash('');", 1)

    # 4) router + share helpers, declared before init
    old_init = "(function init(){try{goHome();}catch(e){setTimeout(init,50);}})();"
    if old_init not in src:
        print("FAIL: init() not found"); return 1
    src = src.replace(old_init, JS + "\n" + NEW_INIT, 1)

    # 5) toast CSS
    i = src.rfind("</style>")
    if i == -1:
        print("FAIL: </style> not found"); return 1
    src = src[:i] + CSS + src[i:]

    io.open(PATH, "w", encoding="utf-8").write(src)
    print("OK: deeplink patch applied")
    return 0

sys.exit(main())
