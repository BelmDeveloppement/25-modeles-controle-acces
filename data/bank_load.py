import sys, importlib
import os; _d=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(_d,'bank')); sys.path.insert(0,_d)
import bank_fixes, bank_edits
def load():
    out=[]
    for i in range(1,13):
        m=importlib.import_module('t%02d'%i)
        fx=bank_fixes.FIX.get(i,{})
        qs=[]
        for j,q in enumerate(m.Q):
            q=list(q)
            if j in fx:
                k,t=fx[j]; q[3+k]=t
            qs.append(q)
        for j,fields in bank_edits.SET.get(i,{}).items():
            for k,t in fields.items(): qs[j][k]=t
        rm=set(bank_edits.REMOVE.get(i,[]))
        qs=[tuple(q) for j,q in enumerate(qs) if j not in rm]+[tuple(q) for q in bank_edits.ADD.get(i,[])]
        out.append((m.THEME,m.SOURCE,qs))
    return out
