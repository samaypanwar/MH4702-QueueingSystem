import numpy as np
import pandas as pd
from simulationmain import SimulationStuff

simulation = SimulationStuff()
results = pd.DataFrame()

while simulation.time < 100:
    print(f"Current time is {simulation.time}.")
    simulation.time_step()

print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")