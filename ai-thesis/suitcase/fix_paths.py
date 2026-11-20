# 在 TD 的 Textport 里运行：把工程里所有指向旧位置的 ai-thesis 路径改成现在的位置。
# （v2：不再只认某个固定的旧名字，凡是 /Users/shanzeyang/.../ai-thesis 开头的都换成新位置）
import re
NEWBASE = '/Users/shanzeyang/Desktop/Just Talking Behind/ai-thesis'
PAT = re.compile(r"/Users/shanzeyang/[^'\"\n\\]*?/ai-thesis")
h = op('/project1/heart_exec')
print('heart_exec 存在：', h is not None, '|', (h.path if h is not None else ''))
if h is not None:
    print('heart_exec 里的路径：', PAT.findall(h.text)[:3], '| 它有没有 File 参数：', hasattr(h.par, 'file') and repr(h.par.file.eval()))
n_dat = n_par = 0
seen = set()
for o in root.findChildren(depth=25):
    try:
        if o.isDAT and hasattr(o, 'text'):
            t = o.text
            found = [m for m in PAT.findall(t) if m != NEWBASE]
            if found:
                o.text = PAT.sub(NEWBASE, t)
                n_dat += 1
                seen.update(found)
    except Exception as e:
        print('跳过', o.path, repr(e)[:60])
    try:
        for p in o.pars():
            try:
                if p.mode == ParMode.CONSTANT and isinstance(p.val, str):
                    f = [m for m in PAT.findall(p.val) if m != NEWBASE]
                    if f:
                        p.val = PAT.sub(NEWBASE, p.val); n_par += 1; seen.update(f)
                elif p.mode == ParMode.EXPRESSION:
                    f = [m for m in PAT.findall(str(p.expr)) if m != NEWBASE]
                    if f:
                        p.expr = PAT.sub(NEWBASE, str(p.expr)); n_par += 1; seen.update(f)
            except Exception:
                pass
    except Exception:
        pass
print('完成：改了 %d 个脚本(DAT)、%d 个参数。找到的旧路径有：%s' % (n_dat, n_par, sorted(seen)))
