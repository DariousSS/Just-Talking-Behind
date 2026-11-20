# 在 TD 的 Textport 里运行（一次）：装一个"投影仪自动归位"：打开工程约 15 秒后，以及以后每次屏幕数量/分辨率变化（插拔投影仪）时，
# 自动运行 projector_fix.py（按分辨率认出两台投影仪，关掉窗口、等一下、再开到对的屏幕）。不用再手动敲命令。
# 撤销：op('/project1/sc_proj_exec').destroy()
p = op('/project1')
ex = p.op('sc_proj_exec') or p.create(executeDAT, 'sc_proj_exec')
ex.text = '''
import time
FIX = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/suitcase/projector_fix.py'
_T0 = None
_LAST = None
def onFrameEnd(frame):
    global _T0, _LAST
    if frame % 60 != 0:
        return
    now = time.time()
    if _T0 is None:
        _T0 = now
        return
    if now - _T0 < 15:
        return
    try:
        sig = tuple((m.width, m.height, bool(getattr(m, 'isPrimary', False))) for m in monitors)
    except Exception:
        return
    if sig == _LAST or len(sig) < 3:
        return
    _LAST = sig
    try:
        exec(open(FIX, encoding='utf-8').read(), {'op': op, 'run': run, 'monitors': monitors, 'ParMode': ParMode})
    except Exception as e:
        print('sc_proj_exec 出错：', repr(e)[:120])
    return
'''
ex.par.active = True
ex.par.framestart = False
ex.par.frameend = True
ex.nodeX, ex.nodeY = 1900, -4100
print('OK：sc_proj_exec 已装好。以后打开工程约 15 秒后、和每次插拔投影仪时，会自动把两个窗口归位。')
