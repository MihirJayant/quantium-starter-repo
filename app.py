import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Group sales by date
daily_sales = (
    df.groupby("Date")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

# Price increase marker
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red"
)

fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["Sales"].max(),
    text="Price Increase",
    showarrow=True
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales"
)
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red"
)

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Soul Foods Pink Morsel Sales Analysis",
        style={"textAlign": "center"}
    ),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)