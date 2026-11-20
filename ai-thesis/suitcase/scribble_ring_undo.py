# 撤销 scribble_ring_setup.py：把「伤口」的贴图换回 sk_draw，关掉圈（sk_exec 里的圈代码会因 sk_ring_on=False 不起作用）
p = op('/project1')
p.store('sk_ring_on', False)
for r in ('/project1/kantanMapper', '/project1/sc_bedkantan/kantanMapper'):
    try:
        shapes = op(r + '/project/allShapes').findChildren(maxDepth=4)
    except Exception:
        continue
    for s in shapes:
        sp = s.op('parameters')
        if sp is not None and hasattr(sp.par, 'Name') and str(sp.par.Name.eval()).strip() == '伤口':
            sp.par.Texture = '/project1/sk_draw'
print('已撤销：「伤口」贴图 = sk_draw，圈功能已关闭。')
