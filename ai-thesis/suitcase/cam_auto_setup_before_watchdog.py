# 在 TD 的 Textport 里运行（一次）：每次打开工程，自动把 MediaPipe 的摄像头切到外接摄像头（名字里有 CAM_KEY 的那个）。
# 原因：打开工程时 MediaPipe 页面的摄像头列表里只有电脑自带的，外接的要等页面加载完、刷新一次列表才出现，工程里存的名字就会被丢掉，回到电脑自带摄像头。
# 做法：打开后 20 秒刷新一次列表，35 秒起每 1 秒左右检查，一出现外接摄像头就切过去；2 分钟还没出现就放弃（继续用电脑自带，不会卡住）。
# 撤销：op('/project1/sc_cam_exec').destroy()
CAM_KEYS = ('Dari Camera', 'StreamCam')      # 按顺序找：先红外 Dari Camera，没有就用罗技 StreamCam；都没有就不动（不会退回电脑自带之外的别的）
p = op('/project1')
ex = p.op('sc_cam_exec') or p.create(executeDAT, 'sc_cam_exec')
ex.text = '''
import time
CAM_KEYS = %r
_T0 = None
_DONE = False
_RESET = False
def onFrameEnd(frame):
    global _T0, _DONE, _RESET
    if _DONE or frame %% 30 != 0:
        return
    now = time.time()
    if _T0 is None:
        _T0 = now
        return
    e = now - _T0
    mp = op('/project1/MediaPipe1')
    if mp is None:
        return
    if e > 20 and not _RESET:
        _RESET = True
        mp.par.Reset.pulse()          # 只刷新这一次摄像头列表（以后不再循环重置，重置会让画面卡住）
        return
    if e > 35:
        names, labels = list(mp.par.Webcam.menuNames), list(mp.par.Webcam.menuLabels)
        for key in CAM_KEYS:
            hit = [n for n, l in zip(names, labels) if key in l]
            if hit:
                _DONE = True
                if mp.par.Webcam.eval() != hit[0]:
                    mp.par.Webcam = hit[0]
                print('sc_cam_exec：已自动切到外接摄像头', hit[0])
                return
        if e > 150:
            _DONE = True
            print('sc_cam_exec：没找到红外/罗技摄像头，现在用的是', mp.par.Webcam.eval(), '。请检查 USB 线，再把工程重新打开。')
    return
''' % (CAM_KEYS,)
ex.par.active = True
ex.par.framestart = False
ex.par.frameend = True
ex.nodeX, ex.nodeY = 1900, -3900
print('OK：sc_cam_exec 已装好。以后每次打开工程，约 35 秒后自动切到外接摄像头。')
