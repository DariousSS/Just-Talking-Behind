# 论文用图：空气钢琴连线。字都 >= 28px（图宽 1800），说明文字放在论文图注里。
bw,bh=280,150
def X(i): return 20+i*370
Y1,Y2,Y3=60,330,600
cols={'track':('#dff3e3','#2e8b57'),'td':('#fff4cc','#b08900'),'sound':('#dbe9ff','#2f5fb3'),'img':('#ecdcff','#6a35c9')}
boxes={
 'hand':(X(0),Y1,'Hand','','track'),
 'cam':(X(1),Y1,'Camera','MediaPipe','track'),
 'td':(X(2),Y1,'TouchDesigner','hand to note','td'),
 'gb':(X(3),Y1,'GarageBand','Dream Voice','sound'),
 'dist':(X(3),Y2,'TouchDesigner','distortion','td'),
 'spk':(X(4),Y2,'Speakers','','sound'),
 'lucy':(X(2),Y2,'Lucy','hidden layers','img'),
 'face':(X(1),Y2,'Wardrobe','faces','img'),
 'quilt':(X(2),Y3,'Quilt','face kaleidoscope','img'),
}
W,H=1800,780
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
 '<defs><marker id="ar" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto"><path d="M0,0 L0,8 L11,4 z" fill="#555"/></marker></defs>',
 f'<rect width="{W}" height="{H}" fill="#fff"/>']
def line(a,b,side,label='',lab_dx=0):
    xa,ya=boxes[a][0],boxes[a][1];xb,yb=boxes[b][0],boxes[b][1]
    if side=='r': x1,y1,x2,y2=xa+bw,ya+bh/2,xb-4,yb+bh/2
    elif side=='l': x1,y1,x2,y2=xa,ya+bh/2,xb+bw+4,yb+bh/2
    else: x1,y1,x2,y2=xa+bw/2,ya+bh,xb+bw/2,yb-4
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" stroke-width="5" marker-end="url(#ar)"/>')
    if label:
        o.append(f'<text x="{(x1+x2)/2+lab_dx}" y="{(y1+y2)/2-16 if side!="d" else (y1+y2)/2+10}" font-size="32" font-weight="bold" text-anchor="{"middle" if side!="d" else "start"}" fill="#333">{label}</text>')
line('hand','cam','r'); line('cam','td','r'); line('td','gb','r','MIDI'); line('gb','dist','d','audio',lab_dx=16)
line('dist','spk','r'); line('td','lucy','d'); line('lucy','face','l'); line('lucy','quilt','d')
for k,(x,y,t,sub,c) in boxes.items():
    f,s=cols[c]
    o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="18" fill="{f}" stroke="{s}" stroke-width="5"/>')
    ty = y+66 if sub else y+88
    o.append(f'<text x="{x+bw/2}" y="{ty}" font-size="34" font-weight="bold" text-anchor="middle" fill="#222">{t}</text>')
    if sub:
        o.append(f'<text x="{x+bw/2}" y="{y+114}" font-size="32" text-anchor="middle" fill="#333">{sub}</text>')
o.append('</svg>')
open('air_piano_flow.svg','w',encoding='utf-8').write('\n'.join(o))
