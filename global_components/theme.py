from utils.helpers import get_theme_template

import dash_mantine_components as dmc 
from typing import Literal
from dash_iconify import DashIconify
from flash import clientside_callback, Input, callback, Output, Patch
import plotly.io as pio


shadcn_gray = [
    "#030712",
    "#111827",
    "#1f2937",
    "#374151",
    "#4b5563",
    "#6b7280",
    "#9ca3af",
    "#e5e7eb",
    "#f3f4f6",
    "#f9fafb",
]
shadcn_slate = [
    "#020617",
    "#0f172a",
    "#1e293b",
    "#334155",
    "#475569",
    "#64748b",
    "#94a3b8",
    "#e2e8f0",
    "#f1f5f9",
    "#f8fafc",
]
mantine_dark = [
    "#d3d4d6",
    "#7a7e83",
    "#383e46",
    "#4a5d79",
    "#222831",
    "#1f242c",
    "#181c22",
    "#0e1014",
    "#14181d",
    "#1b2027",
]

theme_type = Literal['plotly_dark', 'plotly']

class ThemeComponent(dmc.Switch):

    class ids:
        toggle = "color-scheme-toggle"
    
    base_colors_scheme = "dark"

    theme_csc = clientside_callback(
        """ 
        (switchOn) => {
            const theme = switchOn ? 'dark' : 'light'
            document.documentElement.setAttribute('data-mantine-color-scheme', theme);  
        }
        """,
        Input(ids.toggle, "checked"),
    )

    @classmethod
    def graph_theme_callback(cls, graph_id: str):
        @callback(
            Output(graph_id, 'figure', allow_duplicate=True),
            Input(cls.ids.toggle, 'checked'),
            prevent_initial_call=True
        )

        def update_graph_template(is_darkmode: bool):   
            template = get_theme_template(is_darkmode)
            figure = Patch()
            figure.layout.template = template
            return figure
        
    @classmethod
    def echarts_theme_callback(cls, graph_id: str):
        return clientside_callback(
            '''( isDarkmode ) => { return isDarkmode ? 'dark' : 'light' }''',
            Output(graph_id, 'theme'),
            Input(cls.ids.toggle, 'checked'),
            prevent_initial_call=True
        )


    theme = {
        "primaryColor": "violet",
        "primareShade": "3",
        "defaultRadius": "md",  
        "components": {"Card": {"defaultProps": {"shadow": "sm"}}},
        "focusRing": "never",
        "colors": {"dark": mantine_dark, "slate": list(reversed(shadcn_slate))},
    }

    def __init__(self) -> None:
        super().__init__(
            mt="auto",
            offLabel=DashIconify(
                icon="line-md:sun-rising-loop", 
                width=15, 
                color=dmc.DEFAULT_THEME["colors"]["yellow"][8],
                id='temp2'
            ),
            onLabel=DashIconify(
                icon="line-md:moon-rising-alt-loop",
                width=15,
                color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                id='temp1'
            ),
            id=self.ids.toggle,
            color="grey",
            checked=True
        )


vizro_dark = {
  "layout": {
    "annotationdefaults": {
      "font": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "showarrow": False
    },
    "bargroupgap": 0.1,
    "coloraxis": {
      "autocolorscale": False,
      "colorbar": {
        "outlinewidth": 0,
        "showticklabels": True,
        "thickness": 20,
        "tickfont": {
          "size": 14,
          "color": "rgba(255, 255, 255, 0.6)"
        },
        "ticklabelposition": "outside",
        "ticklen": 8,
        "ticks": "outside",
        "tickwidth": 1,
        "title": {
          "font": {
            "size": 14,
            "color": "rgba(255, 255, 255, 0.6)"
          }
        },
        "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    },
    "colorscale": {
      "diverging": [
        [0.0, "#7e000c"],
        [0.05555555555555555, "#9d1021"],
        [0.1111111111111111, "#bc1f37"],
        [0.16666666666666666, "#db2f4c"],
        [0.2222222222222222, "#ea536b"],
        [0.2777777777777778, "#f67486"],
        [0.3333333333333333, "#fe94a0"],
        [0.3888888888888889, "#fbb6be"],
        [0.4444444444444444, "#f8d6da"],
        [0.5, "#E6E8EA"],
        [0.5555555555555556, "#afe7f9"],
        [0.6111111111111112, "#5bd6fe"],
        [0.6666666666666666, "#3bbef1"],
        [0.7222222222222222, "#24a6e1"],
        [0.7777777777777778, "#0d8ed1"],
        [0.8333333333333334, "#0077bd"],
        [0.8888888888888888, "#0061a4"],
        [0.9444444444444444, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequential": [
        [0.0, "#afe7f9"],
        [0.125, "#5bd6fe"],
        [0.25, "#3bbef1"],
        [0.375, "#24a6e1"],
        [0.5, "#0d8ed1"],
        [0.625, "#0077bd"],
        [0.75, "#0061a4"],
        [0.875, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequentialminus": [
        [0.0, "#7e000c"],
        [0.125, "#9d1021"],
        [0.25, "#bc1f37"],
        [0.375, "#db2f4c"],
        [0.5, "#ea536b"],
        [0.625, "#f67486"],
        [0.75, "#fe94a0"],
        [0.875, "#fbb6be"],
        [1.0, "#f8d6da"]
      ]
    },
    "colorway": [
      "#00b4ff",
      "#ff9222",
      "#3949ab",
      "#ff5267",
      "#08bdba",
      "#fdc935",
      "#689f38",
      "#976fd1",
      "#f781bf",
      "#52733e"
    ],
    "font": {
      "family": "Inter, sans-serif, Arial",
      "size": 14,
      "color": "rgba(255, 255, 255, 0.8784313725)"
    },
    "legend": {
      "bgcolor": "rgba(0, 0, 0, 0)",
      "font": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "orientation": "h",
      "title": {
        "font": {
          "size": 14,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        }
      },
      "y": -0.2
    },
    "map": {
      "style": "carto-darkmatter"
    },
    "margin": {
      "autoexpand": True,
      "b": 64,
      "l": 80,
      "pad": 0,
      "r": 24,
      "t": 64
    },
    "modebar": {
      "activecolor": "darkgrey",
      "bgcolor": "rgba(0, 0, 0, 0)",
      "color": "dimgrey"
    },
    "showlegend": True,
    "title": {
      "font": {
        "size": 20,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "pad": {
        "b": 0,
        "l": 24,
        "r": 24,
        "t": 24
      },
      "x": 0,
      "xanchor": "left",
      "xref": "container",
      "y": 1,
      "yanchor": "top",
      "yref": "container"
    },
    "uniformtext": {
      "minsize": 12,
      "mode": "hide"
    },
    "xaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": True,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
      "linecolor": "rgba(255, 255, 255, 0.3019607843)",
      "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
    },
    "yaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": False,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
      "linecolor": "rgba(255, 255, 255, 0.3019607843)",
      "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
    },
    "geo": {
      "bgcolor": "#141721",
      "lakecolor": "#141721",
      "landcolor": "#141721"
    },
    "paper_bgcolor": "#141721",
    "plot_bgcolor": "#141721",
    "polar": {
      "angularaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "bgcolor": "#141721",
      "radialaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    },
    "ternary": {
      "aaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "baxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "bgcolor": "#141721",
      "caxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    }
  },
  "data": {
    "bar": [
      {
        "marker": {
          "line": {
            "color": "#141721"
          }
        },
        "type": "bar"
      }
    ],
    "waterfall": [
      {
        "connector": {
          "line": {
            "color": "rgba(255, 255, 255, 0.3019607843)",
            "width": 1
          }
        },
        "decreasing": {
          "marker": {
            "color": "#ff9222"
          }
        },
        "increasing": {
          "marker": {
            "color": "#00b4ff"
          }
        },
        "textfont": {
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "textposition": "outside",
        "totals": {
          "marker": {
            "color": "grey"
          }
        },
        "type": "waterfall"
      }
    ]
  }
}

vizro_light = {
  "layout": {
    "annotationdefaults": {
      "font": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "showarrow": False
    },
    "bargroupgap": 0.1,
    "coloraxis": {
      "autocolorscale": False,
      "colorbar": {
        "outlinewidth": 0,
        "showticklabels": True,
        "thickness": 20,
        "tickfont": {
          "size": 14,
          "color": "rgba(20, 23, 33, 0.6)"
        },
        "ticklabelposition": "outside",
        "ticklen": 8,
        "ticks": "outside",
        "tickwidth": 1,
        "title": {
          "font": {
            "size": 14,
            "color": "rgba(20, 23, 33, 0.6)"
          }
        },
        "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    },
    "colorscale": {
      "diverging": [
        [0.0, "#7e000c"],
        [0.05555555555555555, "#9d1021"],
        [0.1111111111111111, "#bc1f37"],
        [0.16666666666666666, "#db2f4c"],
        [0.2222222222222222, "#ea536b"],
        [0.2777777777777778, "#f67486"],
        [0.3333333333333333, "#fe94a0"],
        [0.3888888888888889, "#fbb6be"],
        [0.4444444444444444, "#f8d6da"],
        [0.5, "#E6E8EA"],
        [0.5555555555555556, "#afe7f9"],
        [0.6111111111111112, "#5bd6fe"],
        [0.6666666666666666, "#3bbef1"],
        [0.7222222222222222, "#24a6e1"],
        [0.7777777777777778, "#0d8ed1"],
        [0.8333333333333334, "#0077bd"],
        [0.8888888888888888, "#0061a4"],
        [0.9444444444444444, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequential": [
        [0.0, "#afe7f9"],
        [0.125, "#5bd6fe"],
        [0.25, "#3bbef1"],
        [0.375, "#24a6e1"],
        [0.5, "#0d8ed1"],
        [0.625, "#0077bd"],
        [0.75, "#0061a4"],
        [0.875, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequentialminus": [
        [0.0, "#7e000c"],
        [0.125, "#9d1021"],
        [0.25, "#bc1f37"],
        [0.375, "#db2f4c"],
        [0.5, "#ea536b"],
        [0.625, "#f67486"],
        [0.75, "#fe94a0"],
        [0.875, "#fbb6be"],
        [1.0, "#f8d6da"]
      ]
    },
    "colorway": [
      "#00b4ff",
      "#ff9222",
      "#3949ab",
      "#ff5267",
      "#08bdba",
      "#fdc935",
      "#689f38",
      "#976fd1",
      "#f781bf",
      "#52733e"
    ],
    "font": {
      "family": "Inter, sans-serif, Arial",
      "size": 14,
      "color": "rgba(20, 23, 33, 0.8784313725)"
    },
    "legend": {
      "bgcolor": "rgba(0, 0, 0, 0)",
      "font": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "orientation": "h",
      "title": {
        "font": {
          "size": 14,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        }
      },
      "y": -0.2
    },
    "map": {
      "style": "carto-darkmatter"
    },
    "margin": {
      "autoexpand": True,
      "b": 64,
      "l": 80,
      "pad": 0,
      "r": 24,
      "t": 64
    },
    "modebar": {
      "activecolor": "darkgrey",
      "bgcolor": "rgba(0, 0, 0, 0)",
      "color": "dimgrey"
    },
    "showlegend": True,
    "title": {
      "font": {
        "size": 20,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "pad": {
        "b": 0,
        "l": 24,
        "r": 24,
        "t": 24
      },
      "x": 0,
      "xanchor": "left",
      "xref": "container",
      "y": 1,
      "yanchor": "top",
      "yref": "container"
    },
    "uniformtext": {
      "minsize": 12,
      "mode": "hide"
    },
    "xaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": True,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
      "linecolor": "rgba(20, 23, 33, 0.3019607843)",
      "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
    },
    "yaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": False,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
      "linecolor": "rgba(20, 23, 33, 0.3019607843)",
      "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
    },
    "geo": {
      "bgcolor": "white",
      "lakecolor": "white",
      "landcolor": "white"
    },
    "paper_bgcolor": "white",
    "plot_bgcolor": "white",
    "polar": {
      "angularaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "bgcolor": "white",
      "radialaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    },
    "ternary": {
      "aaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "baxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "bgcolor": "white",
      "caxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    }
  },
  "data": {
    "bar": [
      {
        "marker": {
          "line": {
            "color": "white"
          }
        },
        "type": "bar"
      }
    ],
    "waterfall": [
      {
        "connector": {
          "line": {
            "color": "rgba(20, 23, 33, 0.3019607843)",
            "width": 1
          }
        },
        "decreasing": {
          "marker": {
            "color": "#ff9222"
          }
        },
        "increasing": {
          "marker": {
            "color": "#00b4ff"
          }
        },
        "textfont": {
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "textposition": "outside",
        "totals": {
          "marker": {
            "color": "grey"
          }
        },
        "type": "waterfall"
      }
    ]
  }
}

def apply_vizro_theme():
    pio.templates['plotly_dark'] = vizro_dark
    pio.templates['plotly'] = vizro_light
