# 在 TD 的 Textport 里运行：把 TD 认出的屏幕和两个投影窗口的位置写进 td_live/screen_diag.txt（只读不改任何东西）
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/screen_diag.txt'
L = []
for i, m in enumerate(monitors):
    d = {}
    for k in ('width', 'height', 'left', 'top', 'right', 'bottom', 'isPrimary', 'primary', 'name', 'description', 'scale', 'dpi'):
        try:
            d[k] = getattr(m, k)
        except Exception:
            pass
    L.append('monitor %d: %s' % (i, d))
for nm in ('gz_win', 'sc_win2'):
    o = op('/project1/' + nm)
    if o is None:
        L.append(nm + ': 没有这个节点')
        continue
    d = {}
    for k in ('display', 'justifyoffsetto', 'justifyh', 'justifyv', 'winoffsetx', 'winoffsety', 'winw', 'winh', 'borders'):
        try:
            d[k] = o.par[k].eval()
        except Exception as e:
            d[k] = 'ERR'
    L.append('%s: isOpen=%s %s' % (nm, o.isOpen, d))
try:
    L.append('bed_display() 选的是：' + str(op('/project1/sc_game_exec').module._bed_display()))
except Exception as e:
    L.append('bed_display() 读取失败：' + repr(e)[:80])
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print('OK 已写入 screen_diag.txt，告诉我一声就行')
