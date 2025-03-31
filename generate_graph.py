import pandas as pd
import plotly.express as px

df = pd.read_csv('pool_history.csv')
fig = px.line(df, x='timestamp', y='ratio', title='HIVE/SWAP.HIVE Pool Ratio')
fig.write_html('docs/index.html')
