# 在 TD 的 Textport 里运行：让"房间框"和"手电筒的位置"对上——手在框里的位置 = 手电筒在房间图里的位置（框左下角=房间左下角，右上角=右上角）。
# 它读 sk_room_box 和 sk_flipx / sk_flipy，把游戏的 hand_x / hand_y / flip_x / flip_y 设成对应的值。调整 sk_room_box 以后要再运行一次。
p = op('/project1')
g = op('/project1/sc_game_exec')
bx = p.fetch('sk_room_box', (0.56, 0.69, 0.92, 0.885))
fx, fy = bool(p.fetch('sk_flipx', False)), bool(p.fetch('sk_flipy', False))
c = dict(g.fetch('cfg', None) or {})
c['hand_x'] = (1.0 - bx[2], 1.0 - bx[0]) if fx else (bx[0], bx[2])
c['hand_y'] = (1.0 - bx[3], 1.0 - bx[1]) if fy else (bx[1], bx[3])
c['flip_x'], c['flip_y'] = fx, fy
c['room_gate'] = True
g.store('cfg', c)
print('OK：房间框 =', bx, '| 手的范围 x =', c['hand_x'], 'y =', c['hand_y'], '| 翻转 x/y =', fx, fy)
print('以后只有手伸进房间框，才有手电筒圈；框改了就再运行一次本脚本。')
