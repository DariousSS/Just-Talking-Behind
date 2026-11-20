# 在 TD 的 Textport 里运行：看衣柜的 Kantan 里，人脸画面是怎么进来的、每个形状贴的是什么（只读，写进 td_live/ending_diag.txt）
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/ending_diag.txt'
L = []
km = op('/project1/kantanMapper')
if km is None:
    L.append('没有 /project1/kantanMapper')
else:
    L.append('kantanMapper 输入：%s' % [i.path for i in km.inputs])
    L.append('kantanMapper 参数里和背景有关的：%s' % [(x.name, x.eval()) for x in km.pars() if 'bg' in x.name.lower() or 'back' in x.name.lower()][:6])
    sh = op('/project1/kantanMapper/project/allShapes')
    if sh is not None:
        for c in sh.children:
            sp = c.op('parameters')
            try:
                nm = str(sp.par.Name.eval()) if sp is not None and hasattr(sp.par, 'Name') else ''
                tx = str(sp.par.Texture.eval()) if sp is not None and hasattr(sp.par, 'Texture') else ''
                sx = str(sp.par.Showtexture.eval()) if sp is not None and hasattr(sp.par, 'Showtexture') else ''
            except Exception as e:
                nm, tx, sx = '?', '?', '?'
            try:
                rd = c.par.render.eval()
            except Exception:
                rd = '?'
            L.append('形状 %s 名字=%s 贴图=%s 显示贴图=%s render=%s' % (c.name, nm, tx, sx, rd))
for n in ('gz_final', 'gz_over', 'board_view', 'map_sel', 'map_fit', 'sc_perfstage'):
    o = op('/project1/' + n)
    L.append('%s: %s 输入=%s' % (n, '没有' if o is None else o.OPType, [] if o is None else [i.path for i in o.inputs]))
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print('OK 已写入 ending_diag.txt')
