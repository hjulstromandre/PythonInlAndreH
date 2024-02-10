# Importerar numpy, för att kunna generera (pseudo)slumpade tal.
# importerar plotly för att generera diagram som är mer interaktiva än matplot.
# eftersom att flera linjer inkluderas i diagrammet, används graph_objects.
# pandas importeras för att skapa dataframes där den genererade datan ingår.
# För att göra statistiska uträkningar (t.ex. standardavvikelser) importeras statistics-biblioteket.
# För att göra parallella operationer för snabbare generering av 3D-spridningsdiagram, importeras parallel-funktionen från joblib och delayed så diagrammets generering kan inväntas.

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import statistics
from joblib import Parallel, delayed