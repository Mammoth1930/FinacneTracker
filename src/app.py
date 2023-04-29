import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from flask import Flask, request, abort

server = Flask(__name__)

@server.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        print(request.json)
        return "OK", 200
    else:
        abort(400)

app = dash.Dash(server=server)

df = pd.read_csv(
    "https://raw.githubusercontent.com/ThuwarakeshM/geting-started-with-plottly-dash/main/life_expectancy.csv"
)

fig = px.scatter(
    df,
    x="GDP",
    y="Life expectancy",
    size="Population",
    color="continent",
    hover_name="Country",
    log_x=True,
    size_max=60,
)

app.layout = html.Div([dcc.Graph(id="life-exp-vs-gdp", figure=fig)])


if __name__ == "__main__":
    app.run_server(debug=True)