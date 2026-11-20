# 在 TD 的 Textport 里运行：测麦克风听到的声音有多响。共 12 秒：前 6 秒请保持安静（只有环境声），后 6 秒请连续敲几下箱子。
# 结果会打印出来，并写进 td_live/knock_probe.txt。测完自动清理，不影响游戏。
p = op('/project1')
old = p.op('sc_knock_probe')
if old is not None:
    old.destroy()
ex = p.create(executeDAT, 'sc_knock_probe')
ex.text = '''
import time
OUT = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/knock_probe.txt'
_S = {'t0': None, 'quiet': 0.0, 'knock': 0.0, 'n': 0, 'dev': ''}
def onFrameEnd(frame):
    o = op('/project1/clap_in')
    if o is None:
        print('knock_probe：没有 clap_in 节点')
        me.destroy()
        return
    now = time.time()
    if _S['t0'] is None:
        _S['t0'] = now
        try:
            _S['dev'] = str(o.par.device.eval()) + ' | 采样率 ' + str(o.par.rate.eval() if hasattr(o.par, 'rate') else '')
        except Exception:
            pass
        print('knock_probe：开始。现在起 6 秒请保持安静……')
    e = now - _S['t0']
    try:
        a = o.numpyArray()
        pk = float(abs(a).max())
        ch = int(o.numChans)
    except Exception as ex_:
        pk, ch = 0.0, -1
    _S['n'] += 1
    if e < 6.0:
        _S['quiet'] = max(_S['quiet'], pk)
    else:
        if _S.get('said') is None:
            _S['said'] = True
            print('knock_probe：现在请连续敲箱子（6 秒）……')
        _S['knock'] = max(_S['knock'], pk)
    if e >= 12.0:
        msg = '安静时最响=%.4f | 敲箱子最响=%.4f | 通道数=%s | 设备=%s' % (_S['quiet'], _S['knock'], ch, _S['dev'])
        print('knock_probe 结果：', msg)
        open(OUT, 'w', encoding='utf-8').write(msg)
        me.destroy()
    return
'''
ex.par.active = True
ex.par.framestart = False
ex.par.frameend = True
ex.nodeX, ex.nodeY = 1900, -4300
print('knock_probe 已启动：前 6 秒保持安静，后 6 秒连续敲箱子。')
