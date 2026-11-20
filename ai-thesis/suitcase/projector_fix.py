# 在 TD 的 Textport 里运行：重新接投影仪后，窗口跑到电脑上时用。每次插拔线，Mac 给屏幕排的编号会变，所以它不用旧编号，
# 而是按"分辨率"重新认：1920x1200 的 = 被子/盖子投影仪（sc_win2），1920x1080 的（非电脑屏幕）= 衣柜投影仪（gz_win）。
# 做的事：① 把认出的屏幕号写进 audio_fx.json（先备份）② 关掉两个窗口 ③ 等约 1 秒 ④ 再打开到对的屏幕。
import json, shutil, os
FX = '/Users/shanzeyang/Desktop/I can Here You/ai-thesis/td_live/gaze_bridge/audio_fx.json'
mons = [(i, m.width, m.height, bool(getattr(m, 'isPrimary', False))) for i, m in enumerate(monitors)]
print('TD 现在认出的屏幕：', mons)
bed = [i for i, w, h, pr in mons if not pr and sorted((w, h)) == [1200, 1920]]
ward = [i for i, w, h, pr in mons if not pr and sorted((w, h)) == [1080, 1920]]
if not bed or not ward:
    print('没找全两台投影仪（被子 1920x1200：%s，衣柜 1920x1080：%s）。请检查线，在 Mac 的 系统设置 > 显示器 里确认有 3 块屏幕，再运行一次。' % (bed or '没找到', ward or '没找到'))
else:
    b, w_ = bed[0], ward[0]
    try:
        shutil.copy(FX, FX.replace('.json', '_before_projfix.json'))
        d = json.load(open(FX, encoding='utf-8'))
        d['win_display'] = w_
        d['bed_display'] = b
        json.dump(d, open(FX, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    except Exception as e:
        print('写 audio_fx.json 出错（不影响本次）：', repr(e)[:80])
    g, s = op('/project1/gz_win'), op('/project1/sc_win2')
    g.par.winclose.pulse()
    s.par.winclose.pulse()
    run("g=op('/project1/gz_win'); s=op('/project1/sc_win2'); g.par.display=%d; s.par.display=%d; g.par.winopen.pulse(); s.par.winopen.pulse(); print('已重新打开：衣柜(gz_win)->屏幕%d，被子(sc_win2)->屏幕%d')" % (w_, b, w_, b), delayFrames=40)
    print('认出：衣柜投影仪=屏幕 %d，被子投影仪=屏幕 %d。约 1 秒后窗口会重新打开。' % (w_, b))
