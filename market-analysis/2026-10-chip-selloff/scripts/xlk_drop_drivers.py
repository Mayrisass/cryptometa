import os
HERE = os.path.dirname(os.path.abspath(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows=[("NVDA","Nvidia","Chips",26.1,-11.3,-2.95),("AVGO","Broadcom","Chips",8.1,-14.0,-1.13),("AMD","AMD","Chips",4.8,-21.8,-1.04),
("MU","Micron","Chips",5.3,-18.1,-0.97),("INTC","Intel","Chips",2.7,-24.0,-0.64),("LRCX","Lam Research","Chip equipment",1.9,-31.1,-0.59),
("AMAT","Applied Materials","Chip equipment",1.9,-29.2,-0.55),("KLAC","KLA","Chip equipment",1.2,-25.1,-0.29),("MSFT","Microsoft","Software",17.7,-1.6,-0.28),
("ORCL","Oracle","Software",2.0,-13.3,-0.26),("ANET","Arista","Networking",1.2,-20.6,-0.25),("CSCO","Cisco","Networking",2.1,-11.1,-0.23),
("PLTR","Palantir","Software",2.1,2.1,0.04),("IBM","IBM","Software",0.9,13.9,0.13),("AAPL","Apple","Hardware",22.0,4.4,0.96)]
neg,pos="#e34948","#2a78d6"; ink,ink2,grid,bg="#1f1f1d","#6b6a63","#e6e5e0","#fcfcfb"
fig,ax=plt.subplots(figsize=(11,7.4),dpi=150); fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
y=list(range(len(rows)))[::-1]
for yi,(t,n,g,w,r,c) in zip(y,rows):
    ax.barh(yi,c,height=0.62,color=neg if c<0 else pos,edgecolor=bg,linewidth=2)
    lbl=f"{c:+.2f} pts"; ax.text(c+(-0.05 if c<0 else 0.05),yi,lbl,va="center",ha="right" if c<0 else "left",fontsize=9.5,color=ink)
ax.set_yticks(y); ax.set_yticklabels([f"{t}  ·  {n}" for t,n,*_ in rows],fontsize=10.5,color=ink)
ax2=ax.secondary_yaxis("right"); ax2.set_yticks(y); ax2.set_yticklabels([f"{r:+.1f}%   {w:.0f}%   {g}" for t,n,g,w,r,c in rows],fontsize=9.5,color=ink2)
ax2.tick_params(length=0); [s.set_visible(False) for s in ax2.spines.values()]
ax.axvline(0,color=ink2,lw=1); ax.set_xlim(-3.5,1.75)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_:f"{x:+.0f}" if x else "0"))
ax.grid(axis="x",color=grid,lw=0.8); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0,colors=ink2)
ax.set_xlabel("Contribution to the group's drop (percentage points)",color=ink2,fontsize=10)
fig.text(0.22,0.95,"What dragged tech down: Oct 6 → Oct 22, 2026",fontsize=16,fontweight="bold",color=ink)
fig.text(0.22,0.915,"15 largest XLK-type stocks, sized by market cap · group fell −8.1% (XLK −9.7%) · Source: Massive",fontsize=10.5,color=ink2)
fig.text(0.785,0.875,"stock move  ·  weight  ·  group",fontsize=9,color=ink2)
plt.subplots_adjust(left=0.22,right=0.78,top=0.86,bottom=0.08)
fig.savefig(os.path.join(HERE, "..", "charts", "xlk_drop_drivers.png"),facecolor=bg)
