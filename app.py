from dash import Dash, dcc, html, Input, Output, callback, State, ctx, set_props, clientside_callback, Patch, DiskcacheManager, CeleryManager, no_update
import diskcache
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from NLP_Search import Search, Update
from datetime import datetime

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME])

rowData = [{'Title': 'SOP Title', 'Link': 'SOP Link'}]
color_switch = html.Span(
    [
        dbc.Label(class_name="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch(id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence="True"),
        dbc.Label(class_name="fa fa-sun", html_for="color-mode-switch"),
    ],
)

grid = dag.AgGrid(
            id='results-grid',
            rowData=rowData,
            columnDefs=[{"field": 'Title'}, {"field": 'Link'},],
            columnSize="sizeToFit",
            defaultColDef={"flex": 1, "minWidth": 150, "sortable": False, "resizable": True, "filter": True},
        )

app.layout = dbc.Container(
    [
        html.Div(id="header",
                 className="p-2 rounded-3 position-relative bg-primary",
                 children=[
                     html.Div([
                         html.H1("SOP Search", className="display-3 fw-bold text-dark"),
                         html.P("By Canon Sparks", className="text-dark"),
                         ]),
                     ]),
        color_switch,
        html.Br(),
        dcc.Interval(id="interval", interval=1000*60*5, n_intervals=0),
        dbc.Input(id='my-input', type='text', placeholder="Search or enter SOP name:", debounce=True, className="rounded-pill"),
        html.Br(),
        grid,
    ],
    className="dbc dbc-ag-grid",
    fluid=True,
)

@callback(
    Output("interval", "id"),
    Input("interval", "n_intervals"),
    prevent_initial_call=True,
    background=True,
    manager=background_callback_manager,
)
def update_clock(n):
    print(f"Updating at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    Update()
    print(f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return no_update

@callback(
    Output('results-grid', 'rowData'),
    Output('results-grid','columnDefs'),
    Input('my-input', 'value'),
    prevent_initial_call=True,
)
def out(input_value):
    if input_value is not None and input_value.strip() != "":
        SOPS = Search(input_value).SOP
        data = [{'Title': SOP[0], 'Link': SOP[1]} for SOP in SOPS] # type: ignore
        defs=[{"field": 'Title'}, {"field": 'Link', "cellRenderer":"Link"},]
        return [data, defs]
    return [[{'Title': 'SOP Title', 'Link': 'SOP Link'}], [{"field": 'Title'}, {"field": 'Link'},]]


clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark'); 
        return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == '__main__':
    app.run(debug=False)

