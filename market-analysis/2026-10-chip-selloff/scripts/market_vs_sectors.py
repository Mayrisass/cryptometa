import os
HERE = os.path.dirname(os.path.abspath(__file__))
import json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from datetime import datetime
J=json.load(open(os.path.join(HERE, "etf_closes.json")))
d=[datetime.fromisoformat(x) for x in J["d"]]; C=J["C"]
names={"SPY":"S&P 500","QQQ":"Nasdaq-100","DIA":"Dow Jones","XLK":"Technology","XLF":"Financials","XLE":"Energy"}
col={"SPY":"#2a78d6","QQQ":"#eb6834","DIA":"#1baf7a","XLK":"#eda100","XLF":"#e87ba4","XLE":"#008300"}
ink,ink2,grid,bg="#1f1f1d","#6b6a63","#e6e5e0","#fcfcfb"
pct={k:[(x/v[0]-1)*100 for x in v] for k,v in C.items()}
fig,axes=plt.subplots(1,2,figsize=(14,6.6),dpi=150,sharey=True); fig.patch.set_facecolor(bg)
groups=[("Broad market",["QQQ","SPY","DIA"]),("Sectors",["XLE","XLF","XLK"])]
for ax,(title,keys) in zip(axes,groups):
    ax.set_facecolor(bg)
    ends=sorted(keys,key=lambda k:pct[k][-1])
    # nudge labels apart (min 0.75pt gap)
    ys={}; prev=None
    for k in ends:
        y=pct[k][-1]
        if prev is not None and y-prev<0.75: y=prev+0.75
        ys[k]=y; prev=y
    for k in keys:
        p=pct[k]
        ax.plot(d,p,color=col[k],lw=2,solid_capstyle="round",label=f"{k} · {names[k]}")
        ax.plot(d[-1],p[-1],"o",ms=7,color=col[k],mec=bg,mew=2,zorder=5)
        ax.annotate(f"{k} {p[-1]:+.1f}%",(d[-1],p[-1]),xytext=(d[-1],ys[k]),textcoords="data",
                    va="center",fontsize=10.5,color=ink,fontweight="bold",
                    xycoords="data",annotation_clip=False,
                    bbox=None)
    for t in ax.texts: t.set_x(mdates.date2num(d[-1])+0.6)
    ax.axhline(0,color=ink2,lw=1)
    ax.set_xlim(d[0],datetime(2026,11,4))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y,_:f"{y:+.0f}%" if y else "0%"))
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.grid(axis="y",color=grid,lw=0.8); ax.set_axisbelow(True)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=ink2,length=0,labelsize=10)
    ax.set_title(title,loc="left",fontsize=12.5,fontweight="bold",color=ink,pad=8)
    ax.legend(loc="lower left",frameon=False,fontsize=10,labelcolor=ink)
fig.text(0.045,0.955,"Market vs. sectors — past month",fontsize=16,fontweight="bold",color=ink)
fig.text(0.045,0.915,"Change in daily close since Sep 29, 2026 · through Oct 29 · same scale on both panels · Source: Massive",fontsize=10.5,color=ink2)
plt.subplots_adjust(left=0.045,right=0.975,top=0.84,bottom=0.07,wspace=0.12)
fig.savefig(os.path.join(HERE, "..", "charts", "market_vs_sectors_past_month.png"),facecolor=bg)
for k,v in C.items():
    ih=max(range(len(v)),key=v.__getitem__); il=min(range(len(v)),key=v.__getitem__)
    print(f"{k} month {pct[k][-1]:+.2f}% week {(v[-1]/v[18]-1)*100:+.2f}%  hi {v[ih]} {d[ih]:%b%d} lo {v[il]} {d[il]:%b%d}  Oct6->Oct23 {(v[18]/v[5]-1)*100:+.2f}%")
