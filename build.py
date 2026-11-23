# Generates the static pages. Edit SHOP_URL after the BOOTH shop exists.
SHOP_URL="https://kurashitools.booth.pm/"
import pathlib
def page(fn,title,desc,body,js=""):
    shop=f'''<div class="card shop"><span class="tag">作者のショップ</span>このサイトの作者が作った<a href="{SHOP_URL}" rel="noopener">イラスト依頼管理表・同人イベント管理シート・クリエイター向け帳簿</a>などのExcelテンプレートをBOOTHで販売しています（無料の家計簿・カレンダーもあります）。</div>'''
    html=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | クリエイターの計算ツール</title><meta name="description" content="{desc}"><link rel="stylesheet" href="style.css"></head>
<body><header><a href="./">クリエイターの計算ツール</a></header><main><h1>{title}</h1>{body}{shop if fn!="privacy.html" else ""}</main>
<footer><a href="./">ツール一覧</a> ・ <a href="privacy.html">プライバシーポリシー・免責事項</a><br>入力内容はお使いのブラウザ内だけで計算され、送信・保存されません。</footer>{js}</body></html>'''
    pathlib.Path(fn).write_text(html,encoding='utf-8')
tools=[('commission-fee.html','依頼料金の手取り計算','依頼料金から販売サイトの手数料・振込手数料を引いた手取り額と、手取りから逆算した料金を計算します。'),
('doujin-cost.html','同人誌の原価・損益分岐計算','印刷費と頒布価格から、1部あたりの原価と何部で元が取れるかを計算します。'),
('deadline.html','締切逆算スケジュール','締切日と各工程の日数から、ラフ・線画・着彩などの開始日を逆算します。'),
('wareki.html','和暦・西暦 変換','西暦と和暦（令和・平成・昭和・大正・明治）を相互に変換します。'),
('age.html','年齢計算','生年月日から今日時点または指定日時点の満年齢を計算します。'),
('days.html','日数計算','2つの日付の間の日数や、ある日から○日後の日付を計算します。'),
('tax.html','消費税計算（10%・8%）','税込・税抜の金額を10%と8%（軽減税率）で計算します。'),
('warikan.html','割り勘計算','合計金額と人数から1人あたりの金額を計算します。端数の扱いも選べます。')]
page('index.html','クリエイターの計算ツール','依頼料金の手取り、同人誌の原価、締切の逆算など、イラストや同人活動で使う計算ができる無料ツール集です。',
 '<p>登録不要・無料で使える、イラスト・同人・創作活動のための計算ツールです。</p><div class="grid">'+''.join(f'<a href="{f}"><b>{t}</b><br><small>{d}</small></a>' for f,t,d in tools)+'</div>'+'<h2 style="font-size:1.2rem;margin-top:2rem">作者のExcelテンプレート（BOOTH）</h2>'+''.join(f'<div class="card"><b>{t}</b>（{p}）<br><img src="img/{i}.jpg" alt="{t}の画面例" style="width:100%;height:auto;margin:8px 0;border:1px solid var(--line)"><a href="https://kurashitools.booth.pm/items/{n}" rel="noopener">BOOTHで詳しく見る</a></div>' for t,p,i,n in [('イラスト依頼（コミッション）管理表','500円','commission_1','9210066'),('同人イベント 頒布・在庫・売上管理シート','500円','doujin_1','9210067'),('クリエイター向け 売上・経費 帳簿','600円','tax_1','9210071')]))
ERAS_JS='''const ERAS=[["令和",2019,5,1],["平成",1989,1,8],["昭和",1926,12,25],["大正",1912,7,30],["明治",1868,10,23]];'''
page('wareki.html',*tools[3][1:],'''<div class="card"><label>西暦（年）</label><input id="y" type="number" value="2027"><div class="out" id="o1"></div></div>
<div class="card"><label>和暦</label><select id="e"></select><label>年</label><input id="n" type="number" value="9"><div class="out" id="o2"></div></div>
<div class="card"><h2 style="font-size:1.1rem">元号の始まり</h2><p>令和: 2019年5月1日 / 平成: 1989年1月8日 / 昭和: 1926年12月25日 / 大正: 1912年7月30日 / 明治: 1868年10月23日</p><p>改元のあった年は、日付によって元号が変わります（例: 2019年4月30日までは平成31年）。</p></div>''',
f'''<script>{ERAS_JS}
const e=document.getElementById("e");ERAS.forEach(a=>e.add(new Option(a[0],a[0])));
function f1(){{const y=+document.getElementById("y").value;const r=ERAS.filter(a=>y>=a[1]&&y<=(ERAS[ERAS.indexOf(a)-1]?.[1]??9999)).map(a=>a[0]+(y-a[1]+1===1?"元":y-a[1]+1)+"年");document.getElementById("o1").textContent=r.length?y+"年 は "+r.join(" / "):"明治以降の年を入力してください";}}
function f2(){{const a=ERAS.find(x=>x[0]===e.value),n=+document.getElementById("n").value;document.getElementById("o2").textContent=n>0?e.value+n+"年 は 西暦"+(a[1]+n-1)+"年":"";}}
["y","n","e"].forEach(i=>document.getElementById(i).addEventListener("input",()=>{{f1();f2()}}));f1();f2();</script>''')
page('age.html',*tools[4][1:],'''<div class="card"><label>生年月日</label><input id="b" type="date" value="1990-01-01"><label>基準日（空欄なら今日）</label><input id="d" type="date"><div class="out" id="o"></div></div>
<p>満年齢は誕生日を迎えた日に1歳加算して計算しています。</p>''',
'''<script>function f(){const b=new Date(document.getElementById("b").value),dv=document.getElementById("d").value,d=dv?new Date(dv):new Date();if(isNaN(b))return;let a=d.getFullYear()-b.getFullYear();if(d.getMonth()<b.getMonth()||(d.getMonth()===b.getMonth()&&d.getDate()<b.getDate()))a--;document.getElementById("o").textContent=a>=0?"満 "+a+" 歳":"基準日が生年月日より前です";}
document.querySelectorAll("input").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('days.html',*tools[5][1:],'''<div class="card"><label>開始日</label><input id="a" type="date"><label>終了日</label><input id="b" type="date"><div class="out" id="o1"></div></div>
<div class="card"><label>基準日</label><input id="c" type="date"><label>何日後（前の場合はマイナス）</label><input id="n" type="number" value="100"><div class="out" id="o2"></div></div>''',
'''<script>const t=new Date().toISOString().slice(0,10);["a","b","c"].forEach(i=>document.getElementById(i).value=t);
const D=s=>{const[y,m,d]=s.split("-").map(Number);return Date.UTC(y,m-1,d)};const W="日月火水木金土";
function f(){const a=document.getElementById("a").value,b=document.getElementById("b").value;if(a&&b){const n=(D(b)-D(a))/864e5;document.getElementById("o1").textContent=n+" 日（両端を含めると "+(n+(n>=0?1:-1))+" 日）";}
const c=document.getElementById("c").value,k=+document.getElementById("n").value;if(c){const r=new Date(D(c)+k*864e5);document.getElementById("o2").textContent=r.getUTCFullYear()+"年"+(r.getUTCMonth()+1)+"月"+r.getUTCDate()+"日（"+W[r.getUTCDay()]+"）";}}
document.querySelectorAll("input").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('tax.html',*tools[6][1:],'''<div class="card"><label>金額（円）</label><input id="v" type="number" value="1000"><label>入力した金額は</label><select id="k"><option value="ex">税抜</option><option value="in">税込</option></select><label>端数処理</label><select id="r"><option value="floor">切り捨て</option><option value="round">四捨五入</option><option value="ceil">切り上げ</option></select>
<table style="margin-top:1rem"><tr><th>税率</th><th>税抜</th><th>消費税</th><th>税込</th></tr><tbody id="o"></tbody></table></div>
<p>実際の請求額は、お店や事業者の端数処理の方法によって数円異なる場合があります。</p>''',
'''<script>function f(){const v=+document.getElementById("v").value,k=document.getElementById("k").value,R=Math[document.getElementById("r").value];const fm=x=>x.toLocaleString("ja-JP");
document.getElementById("o").innerHTML=[10,8].map(p=>{let ex,inc;if(k==="ex"){ex=v;inc=v+R(v*p/100)}else{inc=v;ex=inc-R(inc*p/(100+p))}return `<tr><td>${p}%</td><td>${fm(ex)}</td><td>${fm(inc-ex)}</td><td>${fm(inc)}</td></tr>`}).join("")}
document.querySelectorAll("input,select").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('warikan.html',*tools[7][1:],'''<div class="card"><label>合計金額（円）</label><input id="t" type="number" value="10000"><label>人数</label><input id="p" type="number" value="3" min="1"><label>集める単位</label><select id="u"><option>1</option><option>10</option><option selected>100</option><option>500</option><option>1000</option></select><div class="out" id="o"></div></div>''',
'''<script>function f(){const t=+document.getElementById("t").value,p=Math.max(1,+document.getElementById("p").value|0),u=+document.getElementById("u").value;const each=Math.ceil(t/p/u)*u,low=Math.floor(t/p/u)*u;
const nHigh=u?Math.max(0,Math.ceil((t-low*p)/(each-low||1))):0;let s="1人 "+each.toLocaleString()+" 円ずつ集めると "+(each*p-t).toLocaleString()+" 円余ります。";
if(each!==low&&nHigh<p)s+="<br>または "+nHigh+"人が "+each.toLocaleString()+" 円、"+(p-nHigh)+"人が "+low.toLocaleString()+" 円（合計 "+(nHigh*each+(p-nHigh)*low).toLocaleString()+" 円）";document.getElementById("o").innerHTML=s}
document.querySelectorAll("input,select").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('privacy.html','プライバシーポリシー・免責事項','当サイトのプライバシーポリシーと免責事項です。','''<div class="card"><h2 style="font-size:1.1rem">入力情報について</h2><p>各ツールの計算はお使いのブラウザ内で行われ、入力内容がサーバーに送信・保存されることはありません。</p>
<h2 style="font-size:1.1rem">広告について</h2><p>当サイトは今後、アフィリエイトプログラムを利用する場合があります。その場合、広告であることが分かるよう「広告」「PR」と明記します。</p>
<h2 style="font-size:1.1rem">免責事項</h2><p>計算結果の正確性には注意を払っていますが、その内容を保証するものではありません。重要な手続きには公的機関などの情報もあわせてご確認ください。当サイトの利用により生じた損害について責任を負いかねます。</p>
<h2 style="font-size:1.1rem">著作権</h2><p>当サイトの文章・プログラムの無断転載はご遠慮ください。</p><p>制定日: 2026年11月24日</p></div>''')

page('commission-fee.html',*tools[0][1:],'''<div class="card"><label>依頼料金（円）</label><input id="p" type="number" value="10000"><label>販売サイトの手数料（%）</label><input id="r" type="number" value="0" step="0.1"><label>1件あたりの固定手数料・振込手数料（円）</label><input id="f" type="number" value="0"><div class="out" id="o1"></div></div>
<div class="card"><label>手取りで受け取りたい金額（円）</label><input id="w" type="number" value="10000"><div class="out" id="o2"></div></div>
<p>手数料率は利用するサービスの最新の規約でご確認のうえ入力してください。サービスによっては依頼者側が手数料を払う場合もあります。</p>''',
'''<script>function f(){const p=+document.getElementById("p").value,r=+document.getElementById("r").value/100,x=+document.getElementById("f").value,w=+document.getElementById("w").value;const fm=n=>Math.round(n).toLocaleString("ja-JP");
const fee=Math.ceil(p*r);document.getElementById("o1").textContent="手数料 "+fm(fee+x)+" 円 → 手取り "+fm(p-fee-x)+" 円";
const need=r<1?Math.ceil((w+x)/(1-r)):0;document.getElementById("o2").textContent="必要な依頼料金は 約 "+fm(need)+" 円";}
document.querySelectorAll("input").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('doujin-cost.html',*tools[1][1:],'''<div class="card"><label>印刷部数</label><input id="n" type="number" value="100"><label>印刷費（円）</label><input id="c" type="number" value="40000"><label>その他の制作費（表紙デザイン外注・送料など）（円）</label><input id="o" type="number" value="0"><label>イベント参加費・交通費など（円）</label><input id="e" type="number" value="0"><label>頒布価格（円）</label><input id="p" type="number" value="500"><div class="out" id="r"></div></div>''',
'''<script>function f(){const g=i=>+document.getElementById(i).value;const n=g("n"),total=g("c")+g("o")+g("e"),p=g("p");const fm=x=>Math.round(x).toLocaleString("ja-JP");
let s="1部あたりの原価：約 "+(n?fm(total/n):"-")+" 円<br>損益分岐：<b>"+(p?Math.ceil(total/p):"-")+" 部</b> 頒布で元が取れます";
if(n&&p)s+="<br>全部頒布した場合の収支："+fm(n*p-total)+" 円";document.getElementById("r").innerHTML=s}
document.querySelectorAll("input").forEach(i=>i.addEventListener("input",f));f();</script>''')
page('deadline.html',*tools[2][1:],'''<div class="card"><label>締切日（納品日）</label><input id="d" type="date"><label>予備日（日）</label><input id="b" type="number" value="2">
<div id="steps"></div><button id="add" type="button" style="margin-top:8px;padding:6px 12px">工程を追加</button>
<table style="margin-top:1rem"><thead><tr><th>工程</th><th>開始日</th><th>終了日</th></tr></thead><tbody id="o"></tbody></table></div>''',
'''<script>const W="日月火水木金土";const def=[["ラフ",2],["線画",3],["着彩",4],["仕上げ",1]];const box=document.getElementById("steps");
function row(n,d){const e=document.createElement("div");e.innerHTML=`<label>工程名と日数</label><input value="${n}" style="max-width:150px"> <input type="number" value="${d}" style="max-width:80px"> 日`;box.appendChild(e);e.querySelectorAll("input").forEach(i=>i.addEventListener("input",f))}
def.forEach(x=>row(...x));document.getElementById("add").onclick=()=>{row("工程",1);f()};
const t=new Date(Date.now()+14*864e5);document.getElementById("d").value=t.toISOString().slice(0,10);
const fd=x=>(x.getUTCMonth()+1)+"/"+x.getUTCDate()+"（"+W[x.getUTCDay()]+"）";
function f(){const v=document.getElementById("d").value;if(!v)return;const[y,m,dd]=v.split("-").map(Number);let end=Date.UTC(y,m-1,dd)-(+document.getElementById("b").value)*864e5;
const st=[...box.children].map(e=>{const i=e.querySelectorAll("input");return[i[0].value,+i[1].value]});const out=[];
for(let k=st.length-1;k>=0;k--){const s=end-(st[k][1]-1)*864e5;out.unshift(`<tr><td>${st[k][0]}</td><td>${fd(new Date(s))}</td><td>${fd(new Date(end))}</td></tr>`);end=s-864e5}
document.getElementById("o").innerHTML=out.join("")}
document.querySelectorAll("#d,#b").forEach(i=>i.addEventListener("input",f));f();</script>''')
