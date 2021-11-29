import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import pandas as pd
from pathlib import Path
# Generation of Erdos-Renyi graph with edge probability p
Path('Datasets/ER').mkdir(exist_ok=True)

"""
If the average degree is 10 for a 100 node network, then #edges = 10 * 100 / 2 = 500
p = 500/(50 * 99) = 10/99  

If the average degree is 30 for a 500 node network, then #edges = 30 * 500 / 2 = 7500
p = 7500/(250 * 499) = 30/499
"""
for num in range(256):
    g = nx.erdos_renyi_graph(500, 30/499)
    model = ep.SIRModel(g)
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter('gamma', 0.005)
    cfg.add_model_parameter("fraction_infected", 0.05) # Start with 5 infected nodes
    model.set_initial_status(cfg)

    # Simulation execution
    iterations = model.iteration_bunch(90)
    old_status = list(iterations[0]['status'].values())
    epidemic_spread = [old_status]
    for i in range(1, 90):
        update_keys = list(iterations[i]['status'].keys())
        update_values = list(iterations[i]['status'].values())
        next_status = old_status[:]
        for j, node_number in enumerate(update_keys):
            next_status[node_number] = update_values[j]
        epidemic_spread.append(next_status[:])
        old_status = next_status[:]
    df = pd.DataFrame(epidemic_spread)
    df.to_csv(f"Datasets/ER/500_nodes/test{num}.csv")
    nx.write_gexf(g, f"Datasets/ER/500_nodes/test{num}.gexf")
    print(num)


