import marshal, sys, types

pyc = open("config.cpython-311.pyc", "rb").read()
co = marshal.loads(pyc[16:])

def walk_consts(obj):
    out = []
    if isinstance(obj, types.CodeType):
        for c in obj.co_consts:
            out.extend(walk_consts(c))
    else:
        out.append(obj)
    return out

consts = walk_consts(co)
candidates = [x for x in consts if isinstance(x, str) and len(x) >= 8]
for s in candidates:
    print(s)
