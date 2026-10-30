import os
HERE = os.path.dirname(os.path.abspath(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from datetime import datetime
from zoneinfo import ZoneInfo
raw="""1790654400000,227.21,607.57,323.86,512.01,196.53
1790740800000,228.38,611.76,328.51,511.38,194.93
1790827200000,230.86,615.73,340.1,529.3,200.33
1790913600000,233.95,633.91,347.49,540.04,206.89
1791172800000,238.9,631.75,345.8,542.28,206.85
1791259200000,239.24,649.42,333.89,530.27,197.46
1791345600000,237.47,645.86,329.51,520.65,196.83
1791432000000,230.48,620.68,320.59,509.57,196.72
1791518400000,229.28,608.1,318.84,507.03,195.57
1791777600000,226.32,594.24,309.56,497.53,190.12
1791864000000,228.52,605.53,301.11,464.24,184.0
1791950400000,221.3,570.82,286.92,446.63,178.81
1792036800000,217.23,562.23,277.46,430.01,174.46
1792123200000,214.13,528.75,263.94,409.29,165.74
1792382400000,217.09,538.05,272.2,413.11,166.4
1792468800000,216.47,534.74,263.45,404.98,161.74
1792555200000,221.97,552.72,260.81,408.94,163.43
1792641600000,212.21,507.93,230.15,375.58,147.83
1792728000000,210.96,516.79,230.1,377.24,145.61
1792987200000,216.0,531.28,237.5,387.59,149.21
1793073600000,217.94,560.26,240.85,395.93,153.66
1793160000000,215.38,578.44,253.82,416.0,158.77
1793246400000,213.66,566.42,254.39,421.66,167.43"""
rows=[list(map(float,l.split(","))) for l in raw.splitlines()]
d=[datetime.fromtimestamp(r[0]/1000,ZoneInfo("America/New_York")).replace(tzinfo=None) for r in rows]
tick=["NVDA","AMD","LRCX","AMAT","KLAC"]; P={k:[r[i+1] for r in rows] for i,k in enumerate(tick)}
b=5  # Oct 6 index
pct={k:[(x/v[b]-1)*100 for x in v] for k,v in P.items()}
eq=[sum(pct[k][i] for k in ("LRCX","AMAT","KLAC"))/3 for i in range(len(d))]
col={"NVDA":"#2a78d6","AMD":"#eb6834","EQ":"#1baf7a"}
ink,ink2,grid,bg,ghost="#1f1f1d","#6b6a63","#e6e5e0","#fcfcfb","#a9d9c5"
fig,(ax,bx)=plt.subplots(1,2,figsize=(14,6.8),dpi=150,gridspec_kw={"width_ratios":[2.3,1]}); fig.patch.set_facecolor(bg)
for a in (ax,bx): a.set_facecolor(bg); [s.set_visible(False) for s in a.spines.values()]; a.tick_params(length=0,colors=ink2,labelsize=10)
# left: path since Oct 6
for k in ("LRCX","AMAT","KLAC"): ax.plot(d,pct[k],color=ghost,lw=1,zorder=1)
series=[("NVDA","NVDA · Nvidia",pct["NVDA"]),("AMD","AMD",pct["AMD"]),("EQ","Chip equipment (avg of LRCX, AMAT, KLAC)",eq)]
for key,lab,p in series:
    ax.plot(d,p,color=col[key],lw=2.4 if key=="NVDA" else 2,label=lab,zorder=3,solid_capstyle="round")
    ax.plot(d[-1],p[-1],"o",ms=7,color=col[key],mec=bg,mew=2,zorder=5)
    ax.annotate(f"{'Equip.' if key=='EQ' else key} {p[-1]:+.1f}%",(d[-1],p[-1]),xytext=(9,0),textcoords="offset points",va="center",fontsize=10.5,fontweight="bold",color=ink)
ax.axhline(0,color=ink2,lw=1); ax.axvline(d[18],color=ink2,lw=0.8,ls=(0,(3,3)))
ax.text(d[18],ax.get_ylim()[1] if False else 9.3,"  Oct 22–23 low",fontsize=9.5,color=ink2,va="top")
bx.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(3))
ax.set_xlim(d[0],datetime(2026,11,3)); ax.set_ylim(-34,10)
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y,_:f"{y:+.0f}%" if y else "0%"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.grid(axis="y",color=grid,lw=0.8); ax.set_axisbelow(True)
ax.legend(loc="lower left",frameon=False,fontsize=10,labelcolor=ink)
ax.set_title("Change since Oct 6 (tech peak)",loc="left",fontsize=12.5,fontweight="bold",color=ink,pad=8)
# right: bounce off each stock's own low
items=[]
for k in tick:
    v=P[k]; i=min(range(17,len(v)),key=v.__getitem__)  # low on/after Oct 21
    items.append((k,(v[-1]/v[i]-1)*100,d[i]))
items.sort(key=lambda x:x[1])
for yi,(k,bn,dl) in enumerate(items):
    c=col["NVDA"] if k=="NVDA" else col["AMD"] if k=="AMD" else col["EQ"]
    bx.barh(yi,bn,height=0.6,color=c,edgecolor=bg,linewidth=2)
    bx.text(bn+0.3,yi,f"{bn:+.1f}%",va="center",fontsize=10.5,fontweight="bold",color=ink)
bx.set_yticks(range(len(items))); bx.set_yticklabels([f"{k}\nlow {dl:%b %d}" for k,_,dl in items],fontsize=10,color=ink)
bx.set_xlim(0,18); bx.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_:f"+{x:.0f}%" if x else "0%"))
bx.grid(axis="x",color=grid,lw=0.8); bx.set_axisbelow(True); bx.axvline(0,color=ink2,lw=1)
bx.set_title("Bounce from each stock's low",loc="left",fontsize=12.5,fontweight="bold",color=ink,pad=8)
fig.text(0.045,0.955,"Nvidia vs. AMD and chip-equipment stocks",fontsize=16,fontweight="bold",color=ink)
fig.text(0.045,0.915,"Daily closes Sep 29 – Oct 29, 2026 · thin lines = LRCX, AMAT, KLAC individually · Source: Massive",fontsize=10.5,color=ink2)
plt.subplots_adjust(left=0.045,right=0.975,top=0.84,bottom=0.07,wspace=0.22)
fig.savefig(os.path.join(HERE, "..", "charts", "nvda_vs_amd_equipment.png"),facecolor=bg)
for k,bn,dl in items: print(k,f"{bn:+.1f}%",dl.date(), f"since Oct6 {pct[k][-1]:+.1f}%")
print("equip avg since Oct6",f"{eq[-1]:+.1f}%","min",f"{min(eq):+.1f}%")
