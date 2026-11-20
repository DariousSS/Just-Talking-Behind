# 在 TD 的 Textport 里运行：把工程里所有写死的旧路径换成新路径。
# 原因：文件夹从 "I can Here You" 改名成 "Just Talking Behind"，TD 里的脚本/参数还指着旧名字，所以报 FileNotFoundError。
# 它只改"含旧路径的文字"，别的不碰。先把工程另存一份再运行更保险。
OLD = '/Users/shanzeyang/Desktop/I can Here You'
NEW = '/Users/shanzeyang/Desktop/Just Talking Behind'
n_dat = n_par = n_expr = 0
for o in root.findChildren(depth=20):
    try:
        if o.isDAT and hasattr(o, 'text') and not (hasattr(o.par, 'file') and str(o.par.file.eval()).strip()):
            t = o.text
            if OLD in t:
                o.text = t.replace(OLD, NEW)
                n_dat += 1
    except Exception as e:
        print('DAT 跳过', o.path, repr(e)[:60])
    try:
        for p in o.pars():
            try:
                if p.mode == ParMode.CONSTANT and isinstance(p.val, str) and OLD in p.val:
                    p.val = p.val.replace(OLD, NEW)
                    n_par += 1
                elif p.mode == ParMode.EXPRESSION and OLD in str(p.expr):
                    p.expr = str(p.expr).replace(OLD, NEW)
                    n_expr += 1
            except Exception:
                pass
    except Exception:
        pass
print('完成：改了 %d 个脚本(DAT)、%d 个参数、%d 个表达式。' % (n_dat, n_par, n_expr))
