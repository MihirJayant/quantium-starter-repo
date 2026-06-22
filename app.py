import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

app = Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[

        html.H1(
            "📈 Soul Foods Pink Morsel Sales Analysis",
            className="title"
        ),

        html.P(
            "Explore Pink Morsel sales trends before and after the January 2021 price increase.",
            className="subtitle"
        ),

        html.Div(
            className="cards",
            children=[

                html.Div(
                    className="card",
                    children=[
                        html.H3("15 Jan 2021"),
                        html.P("Price Increase Date")
                    ]
                ),

                html.Div(
                    className="card",
                    children=[
                        html.H3("4 Regions"),
                        html.P("Interactive Filters")
                    ]
                ),

                html.Div(
                    className="card",
                    children=[
                        html.H3("2018 - 2022"),
                        html.P("Sales History")
                    ]
                )
            ]
        ),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East", "value": "east"},
                {"label": "West", "value": "west"}
            ],
            value="all",
            inline=True,
            className="radio-buttons"
        ),

        dcc.Graph(
            id="sales-chart",
            style={
                "borderRadius": "20px",
                "overflow": "hidden"
            }
        )
    ]
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[
            filtered_df["Region"] == selected_region
        ]

    daily_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales Trend - {selected_region.title()}"
    )

    fig.update_traces(
        line=dict(width=4)
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red",
        line_width=3
    )

    fig.add_annotation(
        x="2021-01-15",
        y=daily_sales["Sales"].max(),
        text="💰 Price Increase",
        showarrow=True,
        arrowhead=2
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",

        title_x=0.5,

        xaxis_title="Date",
        yaxis_title="Sales",

        font=dict(size=16),

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40
        )
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)