# 房间图"消失/黑掉"的时候运行：看是哪一环是黑的（只读，写进 td_live/room_diag2.txt）
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/room_diag2.txt'
L = []
def mean(o):
    try:
        a = o.numpyArray()
        return [round(float(a[..., i].mean()), 3) for i in range(min(3, a.shape[-1]))]
    except Exception as e:
        return 'ERR ' + repr(e)[:50]
for n in ('sc_room', 'sc_room_B', 'sc_room_x', 'sc_gamelid'):
    o = op('/project1/' + n)
    L.append('%s 平均颜色(r,g,b)=%s' % (n, mean(o) if o is not None else '没有'))
lid = op('/project1/sc_gamelid')
if lid is not None:
    L.append('盖子 uD(光点x,y,亮度,封面隐藏)=%s' % [round(lid.par.vec2valuex.eval(), 3), round(lid.par.vec2valuey.eval(), 3), round(lid.par.vec2valuez.eval(), 3), round(lid.par.vec2valuew.eval(), 3)])
    L.append('盖子 uF(圈x,y,半径,手在不在)=%s | uS=%s' % ([round(lid.par['vec1value' + c].eval(), 3) for c in 'xyzw'], [round(lid.par['vec0value' + c].eval(), 3) for c in 'xyzw']))
g = op('/project1/sc_game_exec')
G = (g.fetch('G', {}) or {}) if g is not None else {}
L.append('游戏：state=%s day=%s door_open=%s' % (G.get('state'), G.get('day'), G.get('door_open')))
w = op('/project1/sc_win2')
L.append('sc_win2 窗口 isOpen=%s display=%s' % (w.isOpen, w.par.display.eval()) if w is not None else 'sc_win2 没有')

for kp in ('/project1/kantanMapper', '/project1/sc_bedkantan/kantanMapper'):
    sh = op(kp + '/project/allShapes')
    if sh is None:
        L.append('Kantan %s: 没有' % kp)
        continue
    rows = []
    for c in sh.children:
        try:
            nm = str(c.op('parameters').par.Name.eval()) if c.op('parameters') is not None and hasattr(c.op('parameters').par, 'Name') else ''
        except Exception:
            nm = ''
        try:
            rows.append('%s(%s) render=%s' % (c.name, nm, c.par.render.eval()))
        except Exception as e:
            rows.append('%s ERR' % c.name)
    L.append('Kantan %s 形状：%s' % (kp, ' | '.join(rows)))
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print('OK 已写入 room_diag2.txt')
