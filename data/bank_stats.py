import sys, importlib, collections
sys.path.insert(0,'bank')
mods=[importlib.import_module('t%02d'%i) for i in range(1,13)]
tot=0; L=collections.Counter()
for m in mods:
    q=m.Q; n=len(q); tot+=n
    d=collections.Counter(x[0] for x in q)
    lon=sum(1 for x in q if len(x[2])>=max(len(x[3]),len(x[4]),len(x[5])))
    print(m.THEME[0],n,dict(d),'plus long %d%%'%round(100*lon/n))
print(tot)
