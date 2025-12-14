"""
Gapminder Dashboard
-------------------

Interactive Dash application for exploring the Gapminder dataset.

Features:
- Dataset table
- Bar charts for Population, GDP per Capita, and Life Expectancy
  by Continent and Year
- Choropleth map for selected variable by Year like GDP per Capita, Population, or Life Expectancy
"""

from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# APP CONFIGURATION
# -----------------------------------------------------------------------------

# External CSS for styling (Bootstrap 5 in this case)
external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
]

# Create Dash app instance
# (component_id: app, property: n/a – this is the application object)
app = Dash(
    name="Gapminder Dashboard",
    external_stylesheets=external_css
)

# -----------------------------------------------------------------------------
# DATASET
# -----------------------------------------------------------------------------

# Load Gapminder dataset with datetime and geographic centroids
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)

# Convert "Year" column from datetime to integer year (e.g 1952-05-01 -> 1952)
gapminder_df["Year"] = gapminder_df["Year"].dt.year

# -----------------------------------------------------------------------------
# CHART FACTORY FUNCTIONS
# -----------------------------------------------------------------------------

def create_table():
    """
    Create a Plotly Table figure displaying the full Gapminder dataset.

    Returns
    -------
    plotly.graph_objs.Figure
        Figure containing a data table.
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=gapminder_df.columns,
                    align="left"
                ),
                cells=dict(
                    values=gapminder_df.values.T,
                    align="left"
                ),
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        height=700,
    )
    return fig


def create_population_chart(continent: str = "Asia", year: int = 1952):
    """
    Create bar chart of Population by Country for a given continent and year.

    Parameters
    ----------
    continent : str
        Continent name selected by user.
    year : int
        Year selected by user.

    Returns
    -------
    plotly.graph_objs.Figure
        Population bar chart figure.
    """
    filtered_df = gapminder_df[
        (gapminder_df["Continent"] == continent) &
        (gapminder_df["Year"] == year)
    ]

    # Top 15 countries by population
    filtered_df = filtered_df.sort_values(
        by="Population",
        ascending=False
    ).head(15)

    fig = px.bar(
        filtered_df,
        x="Country",
        y="Population",
        color="Country",
        title=f"Country Population for {continent} Continent in {year}",
        text_auto=True,
    )

    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
    )
    return fig


def create_gdp_chart(continent: str = "Asia", year: int = 1952):
    """
    Create bar chart of GDP per Capita by Country for a given continent and year.

    Parameters
    ----------
    continent : str
        Continent name selected by user.
    year : int
        Year selected by user.

    Returns
    -------
    plotly.graph_objs.Figure
        GDP per Capita bar chart figure.
    """
    filtered_df = gapminder_df[
        (gapminder_df["Continent"] == continent) &
        (gapminder_df["Year"] == year)
    ]

    # Top 15 countries by GDP per Capita
    filtered_df = filtered_df.sort_values(
        by="GDP per Capita",
        ascending=False
    ).head(15)

    fig = px.bar(
        filtered_df,
        x="Country",
        y="GDP per Capita",
        color="Country",
        title=f"Country GDP per Capita for {continent} Continent in {year}",
        text_auto=True,
    )

    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
    )
    return fig


def create_life_exp_chart(continent: str = "Asia", year: int = 1952):
    """
    Create bar chart of Life Expectancy by Country for a given continent and year.

    Parameters
    ----------
    continent : str
        Continent name selected by user.
    year : int
        Year selected by user.

    Returns
    -------
    plotly.graph_objs.Figure
        Life Expectancy bar chart figure.
    """
    filtered_df = gapminder_df[
        (gapminder_df["Continent"] == continent) &
        (gapminder_df["Year"] == year)
    ]

    # Top 15 countries by life expectancy
    filtered_df = filtered_df.sort_values(
        by="Life Expectancy",
        ascending=False
    ).head(15)

    fig = px.bar(
        filtered_df,
        x="Country",
        y="Life Expectancy",
        color="Country",
        title=f"Country Life Expectancy for {continent} Continent in {year}",
        text_auto=True,
    )

    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
    )
    return fig


def create_choropleth_map(variable: str, year: int):
    """
    Create a choropleth map for the selected variable and year.

    Parameters
    ----------
    variable : str
        Column name to visualize (e.g. 'Population', 'GDP per Capita', 'Life Expectancy').
    year : int
        Year selected by user.

    Returns
    -------
    plotly.graph_objs.Figure
        Choropleth map figure.
    """
    filtered_df = gapminder_df[gapminder_df["Year"] == year]

    fig = px.choropleth(
        filtered_df,
        color=variable,
        locations="ISO Alpha Country Code",
        locationmode="ISO-3",
        color_continuous_scale="RdYlBu",
        hover_data=["Country", variable],
        title=f"{variable} Choropleth Map [{year}]",
    )

    fig.update_layout(
        dragmode=False,
        paper_bgcolor="#e5ecf6",
        height=600,
        margin={"l": 0, "r": 0},
    )
    return fig

# -----------------------------------------------------------------------------
# WIDGETS (INPUT COMPONENTS)
# -----------------------------------------------------------------------------

# Distinct continents and years for dropdown options
continents = gapminder_df["Continent"].unique()
years = gapminder_df["Year"].unique()

# Each widget definition includes component_id and property in comments.

# Dropdown for Population tab - continent selection
# component_id: "cont_pop", property: "value"
cont_population = dcc.Dropdown(
    id="cont_pop",
    options=continents,
    value="Asia",
    clearable=False,
)

# Dropdown for Population tab - year selection
# component_id: "year_pop", property: "value"
year_population = dcc.Dropdown(
    id="year_pop",
    options=years,
    value=1952,
    clearable=False,
)

# Dropdown for GDP tab - continent selection
# component_id: "cont_gdp", property: "value"
cont_gdp = dcc.Dropdown(
    id="cont_gdp",
    options=continents,
    value="Asia",
    clearable=False,
)

# Dropdown for GDP tab - year selection
# component_id: "year_gdp", property: "value"
year_gdp = dcc.Dropdown(
    id="year_gdp",
    options=years,
    value=1952,
    clearable=False,
)

# Dropdown for Life Expectancy tab - continent selection
# component_id: "cont_life_exp", property: "value"
cont_life_exp = dcc.Dropdown(
    id="cont_life_exp",
    options=continents,
    value="Asia",
    clearable=False,
)

# Dropdown for Life Expectancy tab - year selection
# component_id: "year_life_exp", property: "value"
year_life_exp = dcc.Dropdown(
    id="year_life_exp",
    options=years,
    value=1952,
    clearable=False,
)

# Dropdown for Choropleth map - year selection
# component_id: "year_map", property: "value"
year_map = dcc.Dropdown(
    id="year_map",
    options=years,
    value=1952,
    clearable=False,
)

# Dropdown for Choropleth map - variable selection
# component_id: "var_map", property: "value"
var_map = dcc.Dropdown(
    id="var_map",
    options=["Population", "GDP per Capita", "Life Expectancy"],
    value="Life Expectancy",
    clearable=False,
)

# -----------------------------------------------------------------------------
# APP LAYOUT
# -----------------------------------------------------------------------------

# Top-level Div for the entire application
# (no component_id needed because it is not used in callbacks)
app.layout = html.Div(
    [
        html.Div(
            [
                # App title
                html.H1(
                    "Gapminder Dataset Analysis",
                    className="text-center fw-bold m-2",
                ),
                html.Br(),

                # Tabs container
                # component_id: (implicit for Tabs), each Tab contains components with explicit ids
                dcc.Tabs(
                    [
                        # -----------------------------------------------------------------
                        # TAB 1: Dataset Table
                        # -----------------------------------------------------------------
                        dcc.Tab(
                            [
                                html.Br(),
                                # Graph component to display data table
                                # component_id: "dataset", property: "figure"
                                dcc.Graph(
                                    id="dataset",
                                    figure=create_table(),
                                ),
                            ],
                            label="Dataset",
                        ),

                        # -----------------------------------------------------------------
                        # TAB 2: Population
                        # -----------------------------------------------------------------
                        dcc.Tab(
                            [
                                html.Br(),
                                "Continent",
                                cont_population,
                                "Year",
                                year_population,
                                html.Br(),
                                # component_id: "population", property: "figure"
                                dcc.Graph(id="population"),
                            ],
                            label="Population",
                        ),

                        # -----------------------------------------------------------------
                        # TAB 3: GDP Per Capita
                        # -----------------------------------------------------------------
                        dcc.Tab(
                            [
                                html.Br(),
                                "Continent",
                                cont_gdp,
                                "Year",
                                year_gdp,
                                html.Br(),
                                # component_id: "gdp", property: "figure"
                                dcc.Graph(id="gdp"),
                            ],
                            label="GDP Per Capita",
                        ),

                        # -----------------------------------------------------------------
                        # TAB 4: Life Expectancy
                        # -----------------------------------------------------------------
                        dcc.Tab(
                            [
                                html.Br(),
                                "Continent",
                                cont_life_exp,
                                "Year",
                                year_life_exp,
                                html.Br(),
                                # component_id: "life_expectancy", property: "figure"
                                dcc.Graph(id="life_expectancy"),
                            ],
                            label="Life Expectancy",
                        ),

                        # -----------------------------------------------------------------
                        # TAB 5: Choropleth Map
                        # -----------------------------------------------------------------
                        dcc.Tab(
                            [
                                html.Br(),
                                "Variable",
                                var_map,
                                "Year",
                                year_map,
                                html.Br(),
                                # component_id: "choropleth_map", property: "figure"
                                dcc.Graph(id="choropleth_map"),
                            ],
                            label="Choropleth Map",
                        ),
                    ]
                ),
            ],
            className="col-8 mx-auto",
        ),
    ],
    style={"background-color": "#e5ecf6", "height": "100vh"},
)

# -----------------------------------------------------------------------------
# CALLBACKS
# -----------------------------------------------------------------------------
# Each callback lists the mapping between component_id and property clearly.

@callback(
    # Output: component_id="population", property="figure"
    Output("population", "figure"),
    # Inputs:
    # - component_id="cont_pop", property="value"
    # - component_id="year_pop", property="value"
    [Input("cont_pop", "value"), Input("year_pop", "value")],
)
def update_population_chart(continent: str, year: int):
    """
    Update Population bar chart when continent or year changes.

    Parameters
    ----------
    continent : str
        Value of Dropdown with id="cont_pop".
    year : int
        Value of Dropdown with id="year_pop".

    Returns
    -------
    plotly.graph_objs.Figure
        Updated population figure for selected continent and year.
    """
    return create_population_chart(continent, year)


@callback(
    # Output: component_id="gdp", property="figure"
    Output("gdp", "figure"),
    # Inputs:
    # - component_id="cont_gdp", property="value"
    # - component_id="year_gdp", property="value"
    [Input("cont_gdp", "value"), Input("year_gdp", "value")],
)
def update_gdp_chart(continent: str, year: int):
    """
    Update GDP per Capita bar chart when continent or year changes.

    Parameters
    ----------
    continent : str
        Value of Dropdown with id="cont_gdp".
    year : int
        Value of Dropdown with id="year_gdp".

    Returns
    -------
    plotly.graph_objs.Figure
        Updated GDP per Capita figure for selected continent and year.
    """
    return create_gdp_chart(continent, year)


@callback(
    # Output: component_id="life_expectancy", property="figure"
    Output("life_expectancy", "figure"),
    # Inputs:
    # - component_id="cont_life_exp", property="value"
    # - component_id="year_life_exp", property="value"
    [Input("cont_life_exp", "value"), Input("year_life_exp", "value")],
)
def update_life_exp_chart(continent: str, year: int):
    """
    Update Life Expectancy bar chart when continent or year changes.

    Parameters
    ----------
    continent : str
        Value of Dropdown with id="cont_life_exp".
    year : int
        Value of Dropdown with id="year_life_exp".

    Returns
    -------
    plotly.graph_objs.Figure
        Updated Life Expectancy figure for selected continent and year.
    """
    return create_life_exp_chart(continent, year)


@callback(
    # Output: component_id="choropleth_map", property="figure"
    Output("choropleth_map", "figure"),
    # Inputs:
    # - component_id="var_map", property="value"
    # - component_id="year_map", property="value"
    [Input("var_map", "value"), Input("year_map", "value")],
)
def update_map(variable: str, year: int):
    """
    Update choropleth map when variable or year changes.

    Parameters
    ----------
    variable : str
        Value of Dropdown with id="var_map".
    year : int
        Value of Dropdown with id="year_map".

    Returns
    -------
    plotly.graph_objs.Figure
        Updated choropleth map for selected variable and year.
    """
    return create_choropleth_map(variable, year)

# -----------------------------------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Run Dash development server
    app.run(debug=True)
