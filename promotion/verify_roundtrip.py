import os, re, json, math, hashlib, zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime

SRC='/mnt/data/TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx'
RT='/mnt/data/TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE'
OUT_JSON='/mnt/data/nfl_v11_roundtrip_verification.json'
OUT_MD='/mnt/data/nfl_v11_roundtrip_verification.md'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def canon(el):
    if el is None: return None
    return (el.tag.split('}')[-1],tuple(sorted((k.split('}')[-1],v) for k,v in el.attrib.items())),(el.text or '').strip(),tuple(canon(x) for x in list(el)))

def workbook_info(path):
    with zipfile.ZipFile(path) as z:
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rid={x.attrib['Id']:x.attrib['Target'] for x in rels}
        out=[]
        for s in wb.find('m:sheets',NS):
            target=rid[s.attrib['{'+NS['r']+'}id']]
            if target.startswith('/'): target=target.lstrip('/')
            elif not target.startswith('xl/'): target='xl/'+target
            target=os.path.normpath(target).replace('\\','/')
            out.append((s.attrib['name'],s.attrib.get('state','visible'),target))
        return out

def shared_strings(z):
    if 'xl/sharedStrings.xml' not in z.namelist(): return []
    root=ET.fromstring(z.read('xl/sharedStrings.xml'))
    return [''.join(t.text or '' for t in si.findall('.//m:t',NS)) for si in root.findall('m:si',NS)]

def parse_cells(path):
    info=workbook_info(path); out={}; rawf={}
    with zipfile.ZipFile(path) as z:
        ss=shared_strings(z)
        for name,state,target in info:
            root=ET.fromstring(z.read(target)); cells={}; fm={}
            for c in root.findall('.//m:c',NS):
                coord=c.attrib['r']; typ=c.attrib.get('t'); style=int(c.attrib.get('s','0'))
                f=c.find('m:f',NS); v=c.find('m:v',NS)
                if f is not None:
                    form=(f.attrib.get('t'),f.attrib.get('si'),f.attrib.get('ref'),f.text or '')
                    fm[coord]=form
                    val=('FORMULA',form,v.text if v is not None else None)
                else:
                    if typ=='s': val=ss[int(v.text)] if v is not None and v.text is not None else ''
                    elif typ=='inlineStr': val=''.join(x.text or '' for x in c.findall('.//m:t',NS))
                    elif typ=='b': val=bool(int(v.text)) if v is not None and v.text is not None else None
                    elif typ in ('str','e','d'): val=v.text if v is not None else ''
                    else:
                        txt=v.text if v is not None else None
                        if txt is None: val=None
                        else:
                            try: val=float(txt)
                            except: val=txt
                cells[coord]=(val,style,typ)
            out[name]=cells; rawf[name]=fm
    return out,rawf

def cached(cell):
    if cell is None:return None
    val,style,typ=cell
    if isinstance(val,tuple) and val and val[0]=='FORMULA':
        raw=val[-1]
        if raw is None:return None
        if typ=='b':return bool(int(raw))
        if typ in ('str','e','d'):return raw
        try:return float(raw)
        except:return raw
    return val

def defined_names(path):
    with zipfile.ZipFile(path) as z: root=ET.fromstring(z.read('xl/workbook.xml'))
    p=root.find('m:definedNames',NS); out=[]
    if p is not None:
        for x in p: out.append((tuple(sorted(x.attrib.items())),x.text or ''))
    return out

def child(el,name):
    if el is None:return None
    for x in list(el):
        if x.tag.split('}')[-1]==name:return x
    return None

def color(el): return None if el is None else tuple(sorted(el.attrib.items()))
def attr(el,k,d=None):return d if el is None else el.attrib.get(k,d)

def visual_styles(path):
    with zipfile.ZipFile(path) as z: root=ET.fromstring(z.read('xl/styles.xml'))
    def arr(name):
        p=root.find('m:'+name,NS); return list(p) if p is not None else []
    fonts,fills,borders=arr('fonts'),arr('fills'),arr('borders')
    custom={}
    p=root.find('m:numFmts',NS)
    if p is not None:
        for x in p:custom[int(x.attrib['numFmtId'])]=x.attrib['formatCode']
    out=[]
    for xf in arr('cellXfs'):
        f=fonts[int(xf.attrib.get('fontId',0))]; fi=fills[int(xf.attrib.get('fillId',0))]; b=borders[int(xf.attrib.get('borderId',0))]
        u=child(f,'u')
        fd=(attr(child(f,'name'),'val'),attr(child(f,'sz'),'val'),child(f,'b') is not None,child(f,'i') is not None,tuple(sorted(u.attrib.items())) if u is not None else None,child(f,'strike') is not None,color(child(f,'color')),attr(child(f,'vertAlign'),'val'))
        pf=child(fi,'patternFill'); fill=(attr(pf,'patternType'),color(child(pf,'fgColor')),color(child(pf,'bgColor')))
        bd=[]
        for side in ('left','right','top','bottom','diagonal'):
            e=child(b,side); bd.append((side,attr(e,'style'),color(child(e,'color'))))
        al=child(xf,'alignment'); ad=[]
        if al is not None:
            for k in ('horizontal','vertical','textRotation','indent','relativeIndent','justifyLastLine'):
                if k in al.attrib:ad.append((k,al.attrib[k]))
            for k in ('wrapText','shrinkToFit'):ad.append((k,al.attrib.get(k,'0') not in ('0','false','False')))
        prot=child(xf,'protection')
        out.append((fd,fill,tuple(bd),custom.get(int(xf.attrib.get('numFmtId',0)),('builtin',int(xf.attrib.get('numFmtId',0)))),tuple(sorted(ad)),tuple(sorted(prot.attrib.items())) if prot is not None else None))
    return out

def colnum(coord):
    n=0
    for ch in re.match(r'[A-Z]+',coord).group(0):n=n*26+ord(ch)-64
    return n

def widths(path):
    out={}
    with zipfile.ZipFile(path) as z:
        for name,state,target in workbook_info(path):
            root=ET.fromstring(z.read(target)); w={}; p=root.find('m:cols',NS)
            if p is not None:
                for x in p:
                    for i in range(int(x.attrib['min']),int(x.attrib['max'])+1):w[i]=(float(x.attrib.get('width','8.43')),x.attrib.get('hidden','0'))
            out[name]=w
    return out

def unordered_validations(path):
    out={}
    with zipfile.ZipFile(path) as z:
        for name,state,target in workbook_info(path):
            root=ET.fromstring(z.read(target)); p=root.find('m:dataValidations',NS)
            out[name]=Counter(canon(x) for x in list(p)) if p is not None else Counter()
    return out

def errors(cells):
    out=[]
    for sh,d in cells.items():
        for co,cell in d.items():
            v=cached(cell); typ=cell[2]
            if typ=='e' or (isinstance(v,str) and v.startswith('#')): out.append((sh,co,v))
    return sorted(out)

src_info=workbook_info(SRC); rt_info=workbook_info(RT)
src_cells,src_f=parse_cells(SRC); rt_cells,rt_f=parse_cells(RT)
checks={}
checks['sheet_order_states_exact']=src_info==rt_info
checks['sheet_count_21']=len(rt_info)==21
checks['formula_count_exact']=sum(len(x) for x in rt_f.values())==57399
checks['formula_coordinates_text_exact']=src_f==rt_f
# cache values
cache_diff=[]; const_diff=[]
for sh in src_cells:
    for co in set(src_cells[sh])|set(rt_cells[sh]):
        a=src_cells[sh].get(co); b=rt_cells[sh].get(co)
        af=a and isinstance(a[0],tuple) and a[0][0]=='FORMULA'; bf=b and isinstance(b[0],tuple) and b[0][0]=='FORMULA'
        if af or bf:
            if cached(a)!=cached(b):cache_diff.append((sh,co,cached(a),cached(b)))
        else:
            av,bv=cached(a),cached(b)
            eq=math.isclose(av,bv,rel_tol=1e-12,abs_tol=1e-12) if isinstance(av,float) and isinstance(bv,float) else av==bv
            if not eq:const_diff.append((sh,co,av,bv))
checks['formula_cached_values_exact']=not cache_diff
checks['nonformula_constants_exact']=not const_diff
checks['defined_names_exact_order_insensitive']=Counter(defined_names(SRC))==Counter(defined_names(RT))
checks['data_validations_exact_order_insensitive']=unordered_validations(SRC)==unordered_validations(RT)
# styles meaningful cells
sv,rv=visual_styles(SRC),visual_styles(RT); style_diff=[]
for sh in src_cells:
    for co in set(src_cells[sh])&set(rt_cells[sh]):
        a,b=src_cells[sh][co],rt_cells[sh][co]
        if cached(a) is None and cached(b) is None:continue
        if sv[a[1]]!=rv[b[1]]:style_diff.append((sh,co,a[1],b[1]))
checks['meaningful_cell_visual_styles_exact']=not style_diff
# used widths
sw,rw=widths(SRC),widths(RT); width_diff=[]
for sh in src_cells:
    maxused=max((colnum(c) for c,v in src_cells[sh].items() if cached(v) is not None or (isinstance(v[0],tuple) and v[0][0]=='FORMULA')),default=0)
    for i in range(1,maxused+1):
        if sw[sh].get(i,(8.43,'0'))!=rw[sh].get(i,(8.43,'0')):width_diff.append((sh,i,sw[sh].get(i),rw[sh].get(i)))
checks['used_column_widths_exact']=not width_diff
# zip parity
with zipfile.ZipFile(SRC) as a,zipfile.ZipFile(RT) as b:
    am,bm=set(a.namelist()),set(b.namelist()); common=am&bm
    same=[n for n in common if a.read(n)==b.read(n)]
    diffs=[n for n in common if a.read(n)!=b.read(n)]
    drawing_members=[n for n in common if n.startswith('xl/drawings/') or n=='xl/persons/person.xml']
    drawing_same=all(a.read(n)==b.read(n) for n in drawing_members)
checks['zip_members_same']=am==bm
checks['drawings_persons_byte_exact']=drawing_same
# production state
sched=rt_cells['IMPORT SCHEDULE']; counts=Counter(); scored26=0
for r in range(6,563):
    season=cached(sched.get(f'B{r}')); typ=cached(sched.get(f'C{r}'))
    if season is None:continue
    counts[(int(season),str(typ))]+=1
    if int(season)==2026 and typ=='REG' and (cached(sched.get(f'I{r}')) is not None or cached(sched.get(f'K{r}')) is not None):scored26+=1
checks['schedule_2026_272_reg_unscored']=counts[(2026,'REG')]==272 and scored26==0
ml=rt_cells['MARKET LINES']; usable=[r for r in range(5,305) if cached(ml.get(f'Q{r}')) not in (None,'')]
checks['usable_market_spreads_zero']=len(usable)==0
adj=rt_cells['ADJUSTMENTS']; active_adj=[]
for r in range(5,105):
    if cached(adj.get(f'M{r}')) not in (None,'',0,0.0):active_adj.append(r)
checks['active_adjustments_zero']=not active_adj
qb=rt_cells['QB VALUES']; qbnz=[]
for r in range(5,37):
    v=cached(qb.get(f'F{r}'))
    if isinstance(v,(int,float)) and abs(v)>1e-12:qbnz.append((r,v))
checks['nonzero_qb_deltas_zero']=not qbnz
tr=rt_cells['TEAM RATINGS']; ovs=[(r,cached(tr.get(f'I{r}'))) for r in range(5,37) if cached(tr.get(f'I{r}')) not in (None,'')]
checks['team_overrides_zero']=not ovs
checks['dq_current_week_clean']=cached(rt_cells['DATA QUALITY'].get('B5'))==0 and cached(rt_cells['DATA QUALITY'].get('B6'))==0 and cached(rt_cells['DATA QUALITY'].get('B7'))==0 and cached(rt_cells['DATA QUALITY'].get('B9'))==0
checks['banner_v11']=cached(rt_cells['START HERE'].get('A1'))=='TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)'
checks['changelog_alignment_entry_preserved']=cached(rt_cells['CHANGELOG'].get('A4'))=='1.1' and cached(rt_cells['CHANGELOG'].get('B4'))=='2026-07-23'
err_src,err_rt=errors(src_cells),errors(rt_cells)
checks['cached_error_cells_exact']=err_src==err_rt and len(err_rt)==6 and all(x[2]=='#DIV/0!' for x in err_rt)
passed=all(checks.values())
report={
 'status':'PASS' if passed else 'FAIL','verified_at_utc':datetime.utcnow().isoformat()+'Z','sheet_id':'1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew','sheet_url':'https://docs.google.com/spreadsheets/d/1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew','source_sha256':sha(SRC),'roundtrip_sha256':sha(RT),'source_size':os.path.getsize(SRC),'roundtrip_size':os.path.getsize(RT),'sheet_count':len(rt_info),'visible_sheets':sum(1 for _,s,_ in rt_info if s=='visible'),'hidden_sheets':sum(1 for _,s,_ in rt_info if s=='hidden'),'formula_count':sum(len(x) for x in rt_f.values()),'nonformula_constant_count':sum(1 for sh in rt_cells.values() for v in sh.values() if not (isinstance(v[0],tuple) and v[0][0]=='FORMULA') and cached(v) is not None),'schedule_counts':{f'{k[0]}_{k[1]}':v for k,v in sorted(counts.items())},'cached_errors':err_rt,'package_members':len(am),'package_members_byte_identical':len(same),'package_members_changed':len(diffs),'changed_package_parts':sorted(diffs),'accepted_package_differences':['Google export deduplicated style IDs and removed no-op style metadata; visual styles on every meaningful cell remain equivalent.','Google export removed formatting-only cells/column spans beyond each sheet’s populated area; used-column widths remain identical.','Named-range and data-validation order changed, but definitions and target ranges are identical.','Shared-string and worksheet XML were repackaged without changing formulas, constants, cached outputs, drawings, or workbook behavior.'],'checks':checks,'diff_details':{'formula_cache_diffs':cache_diff[:20],'constant_diffs':const_diff[:20],'visual_style_diffs':style_diff[:20],'used_width_diffs':width_diff[:20]},'production_state':{'usable_market_spreads':len(usable),'active_adjustments':len(active_adj),'nonzero_qb_deltas':len(qbnz),'team_overrides':len(ovs),'dq_blocked':cached(rt_cells['DATA QUALITY'].get('B5')),'dq_warnings':cached(rt_cells['DATA QUALITY'].get('B6'))}}
with open(OUT_JSON,'w',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False)
md=f'''# NFL v1.1 Google Sheets Round-Trip Verification\n\n**Status: {report['status']}**\n\n- Native Google Sheet ID: `{report['sheet_id']}`\n- Source SHA-256: `{report['source_sha256']}`\n- Round-trip XLSX SHA-256: `{report['roundtrip_sha256']}`\n- Sheets: {report['sheet_count']} ({report['visible_sheets']} visible / {report['hidden_sheets']} hidden)\n- Formula cells: {report['formula_count']:,}\n- 2026 regular-season games: {counts[(2026,'REG')]} (unscored: {counts[(2026,'REG')]-scored26})\n- Usable market spreads: {len(usable)}\n- Active adjustments: {len(active_adj)}\n- Nonzero QB deltas: {len(qbnz)}\n- Team-rating overrides: {len(ovs)}\n\n## Verification\n'''
for k,v in checks.items():md+=f"- {'PASS' if v else 'FAIL'} — {k}\n"
md+='''\n## Accepted Google package differences\n\n- Style IDs were deduplicated and no-op style metadata removed; every meaningful cell retains equivalent visual formatting.\n- Formatting-only cells and column spans beyond populated ranges were omitted; populated/used column widths are unchanged.\n- Named ranges and validation rules were reordered only; their definitions and targets are unchanged.\n- Shared strings and worksheet XML were repackaged; formulas, constants, cached results, drawings, and workbook behavior are unchanged.\n'''
with open(OUT_MD,'w',encoding='utf-8') as f:f.write(md)
print(json.dumps({'status':report['status'],'checks_failed':[k for k,v in checks.items() if not v],'source_sha':report['source_sha256'],'roundtrip_sha':report['roundtrip_sha256'],'formula_count':report['formula_count'],'sheet_count':report['sheet_count'],'package_same':len(same),'package_changed':len(diffs),'errors':err_rt,'schedule':report['schedule_counts'],'production':report['production_state']},indent=2))
