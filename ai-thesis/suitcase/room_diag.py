# 在 TD 的 Textport 里运行：房间图消失的时候运行它，把现场写进 td_live/room_diag.txt（只读不改）
import re
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/room_diag.txt'
L = []
for n in ('sc_room', 'sc_room_B', 'sc_room_x', 'sc_gamelid'):
    o = op('/project1/' + n)
    if o is None:
        L.append('%s: 没有这个节点' % n)
        continue
    d = {'type': o.OPType}
    try:
        d['file'] = o.par.file.eval() if hasattr(o.par, 'file') else ''
        d['cross'] = o.par.cross.eval() if hasattr(o.par, 'cross') else ''
        d['size'] = '%dx%d' % (o.width, o.height)
        d['errors'] = str(o.errors())[:200]
        d['warnings'] = str(o.warnings())[:200]
        d['inputs'] = [i.name for i in o.inputs]
    except Exception as e:
        d['read_err'] = repr(e)[:80]
    L.append('%s: %s' % (n, d))
g = op('/project1/sc_game_exec')
if g is not None:
    t = g.text
    L.append('game_exec 里的 BASE：' + str(re.findall(r"BASE\s*=\s*'([^']*)'", t)[:2]))
    G = g.fetch('G', {}) or {}
    L.append('游戏状态：state=%s day=%s week=%s' % (G.get('state'), G.get('day'), G.get('week')))
    L.append('game_exec 有没有双缓冲代码：%s' % ('sc_room_x' in t))
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print('OK 已写入 room_diag.txt')
