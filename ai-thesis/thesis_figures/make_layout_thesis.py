import re
D='/Users/shanzeyang/Desktop/I can Here You/ai-thesis/submission/'
L=open(D+'dariousshan-drawing-floorplandimensions_full_text.svg',encoding='utf-8').read().split('\n')
drop=['Installation layout — floor plan','Project stage:','>installation footprint<','(doors open, like an open book)','>laptop inside<','>inside the wardrobe<','hand raised towards','visitor lies on','back, head on pillows','feet towards wardrobe','overhead on lighting truss','lighting truss / ceiling','(projector height)','≈ 2.8 m (wardrobe front to P1)','footprint ≈','≈1.6 m','0.15 m','P1 projection<','≈ 1.2 × 1.6 m','book cover →','BED (2 single quilts)','P2 projection on quilt','dashed colour lines','Artist: Shanze','Units: metres','+ laptop<','>SUITCASE</text>\n']
# geometry lines tied to removed dims
dropgeo=['x1="160" y1="821.0"','x1="692.0" y1="821.0"','x1="160" y1="849.5"','x1="93.5"','x1="1384.25"','x1="1175.0" y1="332.5"','x1="1175.0" y1="572.5"','x1="1135.0"','x1="1090.0" y1="1072.5" x2="1090.0" y2="831.0"']
out=[]
for ln in L:
    if any(d.strip('\n') in ln for d in drop if d!='>SUITCASE</text>\n') or any(g in ln for g in dropgeo): continue
    if 'x="1052.5" y="1344"' in ln: continue
    ln=ln.replace('JUST TALKING BEHIND…  (book cover: “Thin Walls”)','JUST TALKING BEHIND…  (book cover: “Thin Walls”)')
    ln=ln.replace('A. FLOOR PLAN  (view from above)','A. Floor plan').replace('B. FRONT ELEVATION  (from the foot of the bed, looking at the wardrobe)','B. Front elevation').replace('C. SIDE SECTION  (looking from the left, wardrobe on the left)','C. Side section')
    ln=ln.replace('1.35 m (single)','1.35 m')
    ln=ln.replace('wardrobe: book cover + room scenes (1920×1080)','wardrobe').replace('quilts: face kaleidoscope + light dots (portrait 1920×1200)','quilts').replace('USB camera on top of the suitcase: hand tracking','camera (hand tracking)').replace('laptop hidden inside the suitcase (runs TouchDesigner)','laptop (in suitcase)')
    ln=ln.replace('<rect x="60" y="1230" width="760" height="150"','<rect x="60" y="1230" width="420" height="150"')
    ln=ln.replace('<text x="1265" y="586" font-size="11"','<text x="1265" y="587" font-size="16"').replace('<rect x="1225" y="569" width="80" height="24"','<rect x="1212" y="569" width="106" height="24"')
    if '<rect x="960" y="1500"' in ln: continue
    if 'BED = 2 stacked single quilts' in ln: ln=ln.replace('BED = 2 stacked single quilts','BED')
    if 'x="1052.5" y="1284"' in ln: continue
    if 'x="474" y="342"' in ln: ln=ln.replace('x="474"','x="405"')
    if 'x="500" y="356"' in ln: ln=ln.replace('x="500"','x="431"')
    m=re.match(r'<text [^>]*font-size="(\d+)"[^>]*>(.*)</text>',ln)
    if m and not re.fullmatch(r'P1|P2|1|2',m.group(2)):
        sz=int(m.group(1)); t=m.group(2)
        if sz in (38,): pass
        elif t.startswith(('A. ','B. ','C. ')): ln=ln.replace('font-size="24"','font-size="30"')
        elif t in ('WARDROBE','SUITCASE','BED'): ln=ln.replace('font-size="%d"'%sz,'font-size="24"')
        elif t=='laptop': pass
        elif t in ('camera','pillows'): ln=ln.replace('font-size="%d"'%sz,'font-size="20"')
        elif 'x="145"' in ln: ln=ln.replace('font-size="%d"'%sz,'font-size="20"')
        else: ln=ln.replace('font-size="%d"'%sz,'font-size="22"')
    out.append(ln)
s='\n'.join(out)
# side section suitcase label: none inside; legend text positions fine
open(D+'dariousshan-drawing-floorplandimensions.svg','w',encoding='utf-8').write(s)
