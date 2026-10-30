import os
HERE = os.path.dirname(os.path.abspath(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from datetime import datetime
from zoneinfo import ZoneInfo
ts=[1790654400000,1790740800000,1790827200000,1790913600000,1791172800000,1791259200000,1791345600000,1791432000000,1791518400000,1791777600000,1791864000000,1791950400000,1792036800000,1792123200000,1792382400000,1792468800000,1792555200000,1792641600000,1792728000000,1792987200000,1793073600000,1793160000000,1793246400000]
d=[datetime.fromtimestamp(t/1000,ZoneInfo("America/New_York")).replace(tzinfo=None) for t in ts]
C={"QQQ":[737.93,739.77,742.03,749.58,756.2,759.66,757.73,747.58,751.27,746.04,743.57,728.95,728.0,709.8,718.36,717.63,725.2,704.47,704.4,712.2,721.25,725.61,715.34],
   "SPY":[764.2,762.63,763.99,769.64,774.83,779.09,777.22,773.93,778.57,778.1,778.01,769.6,771.79,763.25,766.48,769.05,773.09,763.96,759.97,765.37,769.66,772.31,769.36],
   "DIA":[512.88,508.55,508.62,511.1,512.11,514.56,511.02,511.65,516.11,517.91,516.21,515.63,521.18,519.1,518.92,524.36,527.7,527.89,521.37,522.97,523.28,524.68,522.73]}
names={"SPY":"S&P 500","QQQ":"Nasdaq-100","DIA":"Dow Jones"}
col={"SPY":"#2a78d6","QQQ":"#eb6834","DIA":"#1baf7a"}
ink,ink2,grid,bg="#1f1f1d","#6b6a63","#e6e5e0","#fcfcfb"
fig,ax=plt.subplots(figsize=(11,6.2),dpi=150); fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
for k,v in C.items():
    p=[(x/v[0]-1)*100 for x in v]
    ax.plot(d,p,color=col[k],lw=2,solid_capstyle="round",label=f"{k} · {names[k]}")
    ax.plot(d[-1],p[-1],"o",ms=7,color=col[k],mec=bg,mew=2,zorder=5)
    ax.annotate(f"{k}  {p[-1]:+.1f}%  (${v[-1]:.2f})",(d[-1],p[-1]),xytext=(10,0),textcoords="offset points",va="center",fontsize=10.5,color=ink,fontweight="bold")
ax.axhline(0,color=ink2,lw=1)
ax.set_xlim(d[0],datetime(2026,11,6))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y,_:f"{y:+.0f}%" if y else "0%"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.grid(axis="y",color=grid,lw=0.8); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(colors=ink2,length=0,labelsize=10)
ax.legend(loc="lower left",frameon=False,fontsize=10,labelcolor=ink)
fig.text(0.06,0.95,"SPY, QQQ and DIA — past month",fontsize=16,fontweight="bold",color=ink)
fig.text(0.06,0.905,"Change in daily close since Sep 29, 2026 · through Oct 29 · Source: Massive",fontsize=10.5,color=ink2)
plt.subplots_adjust(left=0.06,right=0.97,top=0.86,bottom=0.08)
fig.savefig(os.path.join(HERE, "..", "charts", "etf_past_month.png"),facecolor=bg)
for k,v in C.items():
    i_hi=max(range(len(v)),key=v.__getitem__); i_lo=min(range(len(v)),key=v.__getitem__)
    print(k,f"{(v[-1]/v[0]-1)*100:+.2f}%","hi",v[i_hi],d[i_hi].date(),"lo",v[i_lo],d[i_lo].date(),"maxDD",f"{(min(v[i_hi:])/v[i_hi]-1)*100:.2f}%")
