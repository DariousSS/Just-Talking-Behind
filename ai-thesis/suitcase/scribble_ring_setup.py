# 在 TD 的 Textport 里运行（一次）：紫色的线（衣柜上「伤口」形状，贴图 sk_draw）一进入"房间图"（衣柜右页右上角那块），线就不再画，
# 改成跟着指尖的紫色光圈（和盖子上的手电筒圈一个意思），这样观众只看到一个"鼠标"。
# 新建：sk_ring（GLSL，画圈）、sk_final（= 圈叠在 sk_draw 上）；改：sk_exec（指尖进入房间框就不画线，改画圈）；把「伤口」的贴图换成 sk_final。
# 可调（Textport 里）：
#   op('/project1').store('sk_room_box', (0.56, 0.69, 0.92, 0.885))   房间框 (x0, y0, x1, y1)，都是 0~1，y 向上；框住"房间图"那块
#   op('/project1').store('sk_room_dbg', True)                         把房间框画出来（白线），对准以后设回 False
#   op('/project1').store('sk_ring_r', 0.04)                           圈的半径（占画面高度的比例）
#   op('/project1').store('sk_ring_on', False)                         关掉这个功能（线照常画）
# 撤销：运行 scribble_ring_undo.py
p = op('/project1')
draw = p.op('sk_draw')
ex = p.op('sk_exec')
if draw is None or ex is None:
    raise Exception('没找到 sk_draw / sk_exec：请先运行 scribble_setup.py')
W, H = int(draw.par.resolutionw.eval()), int(draw.par.resolutionh.eval())

SHADER = '''uniform vec4 uRing;
uniform vec4 uBox;
uniform vec4 uOpt;
out vec4 fragColor;
void main() {
    vec2 uv = vUV.st;
    float Wd = uTDOutputInfo.res.z;
    float Ht = uTDOutputInfo.res.w;
    vec2 asp = vec2(Wd / Ht, 1.0);
    vec4 res = vec4(0.0);
    if (false && uRing.w > 0.0) {                       // 圈不再自己画：用房间里原来的手电筒圈（淡紫色）
        float d = length((uv - uRing.xy) * asp);
        float R = max(uRing.z, 0.001);
        float ring = 1.0 - smoothstep(0.0, 0.0045, abs(d - R));
        float glow = exp(-pow(max(d - R, 0.0) / (R * 0.55), 2.0)) * 0.28 * step(d, R * 1.8);
        float fill = (1.0 - smoothstep(R * 0.55, R, d)) * 0.16;
        float a = clamp(ring + glow + fill, 0.0, 1.0) * uRing.w;
        res = vec4(vec3(0.62, 0.28, 0.95) * a, a);
    }
    if (uOpt.x > 0.5) {
        float t = 0.003;
        bool inx = uv.x >= uBox.x - t && uv.x <= uBox.z + t;
        bool iny = uv.y >= uBox.y - t && uv.y <= uBox.w + t;
        bool edge = (abs(uv.x - uBox.x) < t || abs(uv.x - uBox.z) < t) && iny || (abs(uv.y - uBox.y) < t || abs(uv.y - uBox.w) < t) && inx;
        if (edge) res = vec4(1.0, 1.0, 1.0, 1.0);
    }
    fragColor = TDOutputSwizzle(res);
}
'''
ring = p.op('sk_ring') or p.create(glslTOP, 'sk_ring')
ring.nodeX, ring.nodeY = 200, -2450
ring.par.outputresolution = 'custom'
ring.par.resolutionw, ring.par.resolutionh = W, H
try:
    ring.par.format = 'rgba16float'
except Exception:
    pass
try:
    ring.seq.vec.numBlocks = 3
except Exception as e:
    print('sk_ring 的 vec 序列设置失败：', repr(e)[:80])
for i, nm in enumerate(('uRing', 'uBox', 'uOpt')):
    setattr(ring.par, 'vec%dname' % i, nm)
px = p.op('sk_ring_pixel')
if px is None:
    raise Exception('没找到 sk_ring_pixel（GLSL 的像素着色器 DAT）')
px.text = SHADER
fin = p.op('sk_final') or p.create(overTOP, 'sk_final')
fin.nodeX, fin.nodeY = 200, -2300
fin.inputConnectors[0].connect(ring)
fin.inputConnectors[1].connect(draw)

t = ex.text
if 'sk_ring' not in t:
    a1 = "    blob, bcol = (0, 0, 0, 0), (0, 0, 0, 0)\n"
    a2 = "            if fy: y = 1.0 - y\n"
    a3 = "    host.store('sk_st', S)\n"
    for a in (a1, a2, a3):
        if t.count(a) != 1:
            raise Exception('sk_exec 里没找到要改的位置（可能被改过），请把这行发给我：' + repr(a))
    t = t.replace(a1, a1 + "    ring = None\n    RB = host.fetch('sk_room_box', (0.56, 0.69, 0.92, 0.885)) if host.fetch('sk_ring_on', True) else None\n")
    t = t.replace(a2, a2 + """            if RB is not None and RB[0] <= x <= RB[2] and RB[1] <= y <= RB[3]:     # 指尖进了"房间框"：不画线，改画圈
                ring = (x, y)
                host.store('sk_room_t', now)                                      # 告诉游戏：手现在在房间里
                H['last'] = None
                H['len'] = 0.0
                H['seen'] = now
                continue
""")
    t = t.replace(a3, """    rg = op('/project1/sk_ring')                                              # 圈：进框后显示，出框后 0.25 秒内淡掉
    if rg is not None:
        if ring is not None:
            S['ring'] = (ring[0], ring[1], now)
        rr = S.get('ring')
        a_ = 0.0
        if rr is not None and now - rr[2] < 0.25:
            a_ = 1.0 if now - rr[2] < 0.12 else 1.0 - (now - rr[2] - 0.12) / 0.13
        R_ = float(host.fetch('sk_ring_r', 0.04))
        for j_, v_ in enumerate((rr[0] if rr else 0.0, rr[1] if rr else 0.0, R_, a_)):
            setattr(rg.par, 'vec0value' + 'xyzw'[j_], float(v_))
        for j_, v_ in enumerate(host.fetch('sk_room_box', (0.56, 0.69, 0.92, 0.885))):
            setattr(rg.par, 'vec1value' + 'xyzw'[j_], float(v_))
        rg.par.vec2valuex = 1.0 if host.fetch('sk_room_dbg', False) else 0.0
""" + a3)
    ex.text = t
for k, v in (('sk_room_box', (0.56, 0.69, 0.92, 0.885)), ('sk_room_dbg', False), ('sk_ring_r', 0.04), ('sk_ring_on', True)):
    if p.fetch(k, None) is None:
        p.store(k, v)

hits = 0
for r in ('/project1/kantanMapper', '/project1/sc_bedkantan/kantanMapper'):
    try:
        shapes = op(r + '/project/allShapes').findChildren(maxDepth=4)
    except Exception:
        continue
    for s in shapes:
        sp = s.op('parameters')
        if sp is not None and hasattr(sp.par, 'Name') and str(sp.par.Name.eval()).strip() == '伤口':
            sp.par.Texture = '/project1/sk_final'
            hits += 1
print('OK：圈已建好；「伤口」形状的贴图已换成 sk_final（%d 处）。先运行 op("/project1").store("sk_room_dbg", True) 看房间框对不对。' % hits)
