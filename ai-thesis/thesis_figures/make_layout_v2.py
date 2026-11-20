import re
SRC='/Users/shanzeyang/Desktop/I can Here You/ai-thesis/submission/dariousshan-drawing-floorplandimensions_before_suitcase_move.svg'
OUT='/Users/shanzeyang/Desktop/I can Here You/ai-thesis/submission/dariousshan-drawing-floorplandimensions.svg'
L=open(SRC,encoding='utf-8').read().split('\n')
drop=['x="169.5" y="422.0" width="171.0"','x1="203.7"','x1="306.29','>SUITCASE / TRUNK<','computer hidden inside','x="299.2000','cx="245.5" cy="444.8"','>1</text>','cx="245.5" cy="490.4"','>2</text>',
'x="172.5" y="425.0"',
'x1="169.5" y1="422.0" x2="169.5"','x1="340.5" y1="422.0"','x1="169.5" y1="387.8"','>0.9 m</text>\n',
'x1="169.5" y1="422.0" x2="135.0"','x1="169.5" y1="517.0"','x1="141.0" y1="422.0"','x="133.0" y="475.5"',
'x="1017.5" y="565.0"','x1="1044.5"','x1="1125.5"','x="1092.5"','x="1103.5" y="539.0"','>SUITCASE<','P2 projection on lid',
'x1="1017.5" y1="565.0"','x1="1017.5" y1="640"','x1="992.5"','x="984.5"','x1="1017.5" y1="642"','x1="1152.5"','x1="1017.5" y1="726"','x="1085.0" y="718"',
'x="1120.0" y="1305.0"','trunk (to the side)','gap 0.1 m',
'cx="105" cy="1364"','x="105" y="1369"','cx="105" cy="1394"','x="105" y="1399"','button 1 =','button 2 =']
out=[]
for ln in L:
    if any(d.strip('\n') in ln for d in drop):
        # keep the 0.9 m text of the elevation? both are suitcase dims -> drop
        continue
    ln=ln.replace('x2="1120.0" y2="1305.0"','x2="1105.0" y2="1357.5"')
    ln=ln.replace('Shanze Yang','Shanze Yang').replace('Artist: Darious Shan','Artist: Shanze Yang')
    ln=ln.replace('quilts + suitcase lid: face kaleidoscope, lid lights up (portrait 1920×1080)','')
    ln=ln.replace('quilts + suitcase lid: face kaleidoscope, lid lights up (portrait 1920×1200)','quilts: face kaleidoscope + light dots (portrait 1920×1200)')
    ln=ln.replace('USB camera on the suitcase lid: hand tracking','USB camera on top of the suitcase: hand tracking')
    ln=ln.replace('<rect x="60" y="1230" width="760" height="190"','<rect x="60" y="1230" width="760" height="150"')
    if '>WARDROBE</text>' in ln and 'x="483.0"' in ln:
        ln=ln.replace('x="483.0" y="331.0"','x="358" y="331.0"').replace('text-anchor="middle"','text-anchor="end"')
    if '(doors open, like an open book)' in ln:
        ln=ln.replace('x="483.0" y="353.0"','x="358" y="353.0"').replace('text-anchor="middle"','text-anchor="end"')
    if ln.startswith('<rect x="1163.75" y="617.5"'):
        out+=['<rect x="1197.5" y="565.0" width="135.0" height="75.0" rx="0" fill="#e8e0cf" stroke="#1a1a1a" stroke-width="2.5"/>',
        '<rect x="1225" y="569" width="80" height="24" rx="2" fill="none" stroke="#555" stroke-width="1.5" stroke-dasharray="5 3"/>',
        '<text x="1265" y="586" font-size="11" text-anchor="middle" fill="#444">laptop</text>',
        '<rect x="1254.0" y="547.0" width="22" height="18" rx="3" fill="#2f9e44" stroke="#1a1a1a" stroke-width="1.5"/>',
        '<text x="1265.0" y="539.0" font-size="13" text-anchor="middle" fill="#2f9e44" font-weight="bold">camera</text>',
        '<text x="1158" y="598" font-size="14" text-anchor="end" fill="#1a1a1a" font-weight="bold">SUITCASE</text>',
        '<text x="1158" y="616" font-size="12" text-anchor="end" fill="#555">inside the wardrobe</text>']
    if '>WARDROBE</text>' in ln and 'rotate' in ln:
        out.append(ln)
        out+=['<rect x="1021" y="1305" width="63" height="75" fill="#e8e0cf" stroke="#1a1a1a" stroke-width="2"/>',
        '<text x="1052.5" y="1344" font-size="11" text-anchor="middle" fill="#1a1a1a" font-weight="bold">SUITCASE</text>',
        '<text x="1052.5" y="1360" font-size="11" text-anchor="middle" fill="#444">+ laptop</text>',
        '<rect x="1064" y="1291" width="26" height="14" rx="3" fill="#2f9e44" stroke="#1a1a1a" stroke-width="1.5"/>',
        '<text x="1052.5" y="1284" font-size="12" text-anchor="middle" fill="#2f9e44" font-weight="bold">camera</text>']
        continue
    if 'x="1172.5" y="1263.0"' in ln: pass
    out.append(ln)
    if '>USB camera on top' in ln:
        out+=['<rect x="96" y="1357" width="18" height="13" rx="2" fill="#343a40" stroke="#1a1a1a" stroke-width="1.5"/>',
        '<text x="145" y="1369" font-size="15" text-anchor="start" fill="#1a1a1a">laptop hidden inside the suitcase (runs TouchDesigner)</text>']
    if '>installation footprint<' in ln: pass
open(OUT,'w',encoding='utf-8').write('\n'.join(out))
# suitcase in floor plan: insert before wardrobe depth dims
s=open(OUT,encoding='utf-8').read()
plan='''<rect x="397.5" y="296" width="171" height="70" fill="#e8e0cf" stroke="#1a1a1a" stroke-width="2.5"/>
<text x="483" y="318" font-size="14" text-anchor="middle" fill="#1a1a1a" font-weight="bold">SUITCASE</text>
<text x="483" y="334" font-size="11" text-anchor="middle" fill="#444">laptop inside</text>
<rect x="474" y="342" width="18" height="18" rx="3" fill="#2f9e44" stroke="#1a1a1a" stroke-width="1.5"/>
<text x="500" y="356" font-size="12" text-anchor="start" fill="#2f9e44" font-weight="bold">camera</text>
'''
k='<rect x="354.75" y="403.0"'
s=s.replace(k,plan+k,1)
open(OUT,'w',encoding='utf-8').write(s)
