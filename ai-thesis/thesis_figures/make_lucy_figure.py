# 论文用图：Lucy 的 11 层。字都 >= 26px（图宽 1800），说明文字放在论文图注里，图里不放小字。
layers=[('D0',128),('D1',64),('D2',32),('D3',16),('D4',8),('MID',8),('U0',8),('U1',16),('U2',32),('U3',64),('U4',128)]
mods={'D0':('Contour','30'),'D2':('Texture','90'),'D3':('Dissolve','96'),'MID':('Distortion','231'),'U4':('Fine detail','67')}
depth={'D0':0,'D1':1,'D2':2,'D3':3,'D4':4,'MID':5,'U0':4,'U1':3,'U2':2,'U3':1,'U4':0}
W,H=1800,900; bw,bh,gap,x0=134,92,20,38; top,step=60,100
pos={n:(x0+i*(bw+gap),top+depth[n]*step) for i,(n,r) in enumerate(layers)}
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
 '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#777"/></marker></defs>',
 f'<rect width="{W}" height="{H}" fill="#fff"/>']
names=[l[0] for l in layers]
for e,d in (('D0','U4'),('D1','U3'),('D2','U2'),('D3','U1'),('D4','U0')):
    xa,ya=pos[e];xb,yb=pos[d]
    o.append(f'<path d="M{xa+bw/2},{ya} C{xa+bw/2},{ya-45} {xb+bw/2},{yb-45} {xb+bw/2},{yb}" fill="none" stroke="#c4c4c4" stroke-width="3" stroke-dasharray="9 7"/>')
for a,b in zip(names[:-1],names[1:]):
    xa,ya=pos[a];xb,yb=pos[b]
    o.append(f'<line x1="{xa+bw}" y1="{ya+bh/2}" x2="{xb-2}" y2="{yb+bh/2}" stroke="#777" stroke-width="4" marker-end="url(#ar)"/>')
for n,r in layers:
    x,y=pos[n]
    fill,stroke,tc='#f1f1f1','#888','#222'
    if n in mods: fill,stroke,tc='#7b3fe4','#4b1fa8','#fff'
    if n=='U3': fill,stroke,tc='#f6a04d','#b3631a','#222'
    o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="4"/>')
    o.append(f'<text x="{x+bw/2}" y="{y+42}" font-size="36" font-weight="bold" text-anchor="middle" fill="{tc}">{n}</text>')
    o.append(f'<text x="{x+bw/2}" y="{y+78}" font-size="28" text-anchor="middle" fill="{tc}">{r} px</text>')
    if n in mods:
        nm,ch=mods[n]
        o.append(f'<text x="{x+bw/2}" y="{y+bh+38}" font-size="30" font-weight="bold" text-anchor="middle" fill="#4b1fa8">{nm}</text>')
        o.append(f'<text x="{x+bw/2}" y="{y+bh+72}" font-size="28" text-anchor="middle" fill="#4b1fa8">ch {ch}</text>')
    if n=='U3':
        o.append(f'<text x="{x+bw/2}" y="{y+bh+38}" font-size="30" font-weight="bold" text-anchor="middle" fill="#b3631a">Gaze</text>')
# legend
ly=H-60
o.append(f'<rect x="60" y="{ly-26}" width="34" height="34" rx="6" fill="#7b3fe4" stroke="#4b1fa8" stroke-width="3"/>')
o.append(f'<text x="108" y="{ly+2}" font-size="30" fill="#222">edited channel</text>')
o.append(f'<rect x="420" y="{ly-26}" width="34" height="34" rx="6" fill="#f6a04d" stroke="#b3631a" stroke-width="3"/>')
o.append(f'<text x="468" y="{ly+2}" font-size="30" fill="#222">gaze layer</text>')
o.append('</svg>')
open('lucy_hidden_layers.svg','w',encoding='utf-8').write('\n'.join(o))
