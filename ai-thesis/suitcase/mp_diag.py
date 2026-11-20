# 在 TD 的 Textport 里运行：把 MediaPipe 现在的状态写进 td_live/mp_diag.txt（只读不改）。运行时请把手放在摄像头前面动一动。
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/mp_diag.txt'
mp = op('/project1/MediaPipe1')
L = ['摄像头: %s' % mp.par.Webcam.eval(), '菜单: %s' % list(mp.par.Webcam.menuLabels)]
for p in mp.pars():
    if 'hand' in p.name.lower() or 'hand' in p.label.lower() or 'face' in p.name.lower()[:4]:
        L.append('par %s (%s) = %s' % (p.name, p.label, p.eval()))
L.append('---- MediaPipe1 里面的节点 ----')
for c in mp.children:
    s = '%s [%s]' % (c.name, c.OPType)
    try:
        if c.isCHOP:
            s += ' 通道数=%d' % c.numChans
            if c.numChans:
                s += ' 前3个通道=' + str([(ch.name, round(float(ch.eval()), 3)) for ch in c.chans()[:3]])
        elif c.isDAT:
            s += ' 行数=%d' % c.numRows
        elif c.isTOP:
            s += ' 分辨率=%dx%d' % (c.width, c.height)
    except Exception as e:
        s += ' 读取失败 ' + repr(e)[:40]
    L.append(s)
for pth in ('/project1/hand_tracking2', '/project1/hand_tracking2/null2', '/project1/hand_tracking2/null3'):
    o = op(pth)
    L.append('%s: %s' % (pth, '没有' if o is None else (o.OPType + ((' 点数=%d' % len(list(o.points))) if hasattr(o, 'points') else ''))))
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print('OK 已写入 mp_diag.txt')
