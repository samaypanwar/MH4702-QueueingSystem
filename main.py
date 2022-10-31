import pandas as pd
from simulation import SimulationStuff

simulation = SimulationStuff()
results = pd.DataFrame()

while simulation.time < 100:
    print(f"Current time is {simulation.time}.")
    simulation.time_step()
    stats = simulation.calculate_stats()
    print(f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}.")

print("\nSimulation complete.")
print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")