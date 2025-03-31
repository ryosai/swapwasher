import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Load data
df = pd.read_csv('pool_history.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create interactive plot
fig = px.line(
    df, 
    x='timestamp', 
    y='ratio',
    title='HIVE/SWAP.HIVE Pool Ratio Trend',
    labels={'ratio': 'Ratio (HIVE/SWAP.HIVE)', 'timestamp': 'Time'},
    template='plotly_dark'
)

# Add reward threshold lines
fig.add_hline(y=1.0, line_dash="dot", line_color="white", annotation_text="Perfect Balance")
fig.add_hline(y=1.05, line_dash="dash", line_color="orange", annotation_text="Upper Reward Threshold")
fig.add_hline(y=0.95, line_dash="dash", line_color="orange", annotation_text="Lower Reward Threshold")

# Highlight reward opportunities
reward_periods = df[(df['ratio'] < 0.95) | (df['ratio'] > 1.05)]
fig.add_scatter(
    x=reward_periods['timestamp'],
    y=reward_periods['ratio'],
    mode='markers',
    marker=dict(color='red', size=8),
    name='Reward Opportunity'
)

# Save as HTML
fig.write_html('docs/index.html')  # GitHub Pages looks for /docs/index.html
