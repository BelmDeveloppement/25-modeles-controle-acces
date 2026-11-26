import sys, importlib
sys.path.insert(0,'bank')
t=int(sys.argv[1]); m=importlib.import_module('t%02d'%t)
off=[]
for i,x in enumerate(m.Q):
    c=x[2]; ds=x[3:6]; mg=len(c)-max(len(d) for d in ds)
    if mg>0: off.append((mg,i))
off.sort(); k=int(len(off)*0.66)
sel=sorted(i for _,i in off[:k])
print('theme',t,'offenders',len(off),'to fix',len(sel))
for i in sel:
    x=m.Q[i]; print(i,'|',x[1][:50],'| C:',x[2],'| D:',' / '.join(x[3:6]))
