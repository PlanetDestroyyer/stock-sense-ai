from finvizfinance.screener.overview import Overview

screener = Overview()


screener.set_filter(signal='Top Gainers')
gainers = screener.screener_view()
print("🔼 Top Gainers:")
print(gainers)

