# October 2026 chip selloff

Daily closes Sep 29 – Oct 29, 2026 from Massive (`/v2/aggs`), news from Massive's
news feed (`/v2/reference/news`). Not investment advice.

## 1. Market vs. sectors

![Market vs. sectors](charts/market_vs_sectors_past_month.png)

| ETF | Past month | Oct 6 → Oct 23 |
| --- | --- | --- |
| XLE (Energy) | +11.7% | +8.8% |
| XLF (Financials) | +5.4% | +3.5% |
| DIA (Dow) | +1.9% | +1.3% |
| SPY (S&P 500) | +0.7% | −2.5% |
| XLK (Technology) | −3.0% | −9.3% |
| QQQ (Nasdaq-100) | −3.1% | −7.3% |

Money rotated out of tech into energy and financials. See also
[`charts/etf_past_month.png`](charts/etf_past_month.png).

## 2. What dragged tech down (Oct 6 → Oct 22)

![XLK drop drivers](charts/xlk_drop_drivers.png)

Chipmakers (−6.7 pts) and chip-equipment makers (−1.4 pts) account for the whole drop
of the 15 largest tech names; Nvidia alone was about −3 pts. Apple (+4.4%) cushioned it.
Weights are approximated from market cap because ETF holdings aren't in the current
Massive plan; XLK's actual capped weights differ.

**Why, per the news feed** (mostly Motley Fool and Zacks reporting):

1. **Oct 12–15:** Chinese DRAM maker CXMT's new architecture hit Micron (−13.5% that week).
2. **Oct 14–16:** rotation into defensive sectors on rate, energy-price and bubble worries;
   strong TSMC and ASML results didn't stop it.
3. **Oct 22:** oil at a five-month high plus Meta's negative free cash flow and capex jump
   raised doubts about AI-spending sustainability (AMD −8.1% that day).

## 3. Why Nvidia hasn't bounced

![Nvidia vs AMD and chip equipment](charts/nvda_vs_amd_equipment.png)

| Since Oct 6 | Lowest point | Bounce from low | Oct 29 |
| --- | --- | --- | --- |
| NVDA | −11.8% | +1.3% | −10.7% |
| AMD | −21.8% | +11.5% | −12.8% |
| Chip equipment (avg) | −28.7% | +10.6% to +15.0% | −19.8% |

Nvidia fell least but has barely recovered. News points to Nvidia-specific concerns:
Google selling TPUs and OpenAI reportedly buying them (Oct 28–29), customer-financing
worries (CoreWeave downgrade, bond-market stress, "circular financing"), weaker-than-hoped
China shipments, and "AI bubble" commentary aimed at the largest company.

## 4. Big-tech capex scorecard (Oct 28–29 reports)

| | Microsoft | Alphabet | Amazon |
| --- | --- | --- | --- |
| Quarterly capex | $45.2B (+29.5% YoY) | $51.4B (>2× YoY, record) | $77.3B (>2× YoY) |
| Full-year plan | $170B for 2026 | $195–205B for 2026 (pre-earnings figure) | $220B for 2026 |
| Cloud growth | Azure +48% (49–50% guided) | Google Cloud +103% to $30.7B | AWS +39% to $46B (>40% guided for 2027–28) |
| Free cash flow | Positive, down 27% | −$9.1B (2nd negative quarter) | −$42.4B trailing 12 months |
| Results vs. estimates | Beat | Missed EPS; Search +12% | Missed revenue and EPS |
| Stock, Oct 29 close | −0.2% | −12.6% | −4.3% |

Combined quarterly capex is about $174B; 2026 plans total roughly $590B, plus Meta's
$135–145B. Spending keeps rising (75% of Microsoft's went to GPUs and CPUs), but the
market rewarded the company still generating cash and punished the two burning it.
Nvidia slipped on both days (−1.2%, −0.8%).

Capex, cash-flow and guidance figures come from news coverage of the reports; financial
statements aren't in the current Massive plan. Stock moves are Massive daily closes.

## Regenerating the charts

```bash
pip install matplotlib
python scripts/etf_past_month.py
python scripts/market_vs_sectors.py      # reads scripts/etf_closes.json
python scripts/xlk_drop_drivers.py
python scripts/nvda_vs_amd_equipment.py
```

Price data is embedded in the scripts (or `etf_closes.json`) as fetched on Oct 30, 2026,
so the charts reproduce exactly without an API key.
