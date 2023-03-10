from utils import *

# recollim tots els fitxers en un únic llistat
escenaris = [file for file in os.scandir("Scenarios")]
# escenaris = [open("Scenario01.txt"), open("Scenario04.txt")]

# inicialització del dataset final
final_dataset = pd.DataFrame(columns=["Node", "NumCont", "DURC", "ICT", "Escenari"])

# itera per tots els fitxers i extreu les dades
for xarxa, escenari in zip(escenaris, range(1, len(escenaris) + 1)):
    dataset = pd.read_csv(xarxa, sep=" ", header=None)
    dataset.columns = ["Time", "CONN", "Node", "Node2", "Type"]
    dataset.drop(["CONN"], axis=1, inplace=True)

    # afegim el "Node2" a la columna "Node" per a tenir en compte la connexió en les dues direccions
    dataset = both_ways(dataset)
    print("Data from", escenari, "modified.")

    one_file = dataset.groupby(['Node'])["Node2"].size().reset_index(name='NumCont')

    temps = dataset.groupby(['Node', 'Node2']).agg(pair_DURC=("Time", mean_conn_duration),
                                                   pair_ICT=("Time", mean_btw_conns)).reset_index()
    final_attrs = temps.groupby(['Node']).agg(DURC=("pair_DURC", np.mean), ICT=("pair_ICT", np.mean)).reset_index()

    one_file = one_file.merge(final_attrs, how='inner')
    one_file["Escenari"] = escenari

    final_dataset = pd.concat([one_file, final_dataset], ignore_index=True)
    print("File", escenari, "done!\n")

# guarda el dataset complet en un fitxer a part
final_dataset.to_csv("all_scenarios_bo.csv", encoding='utf-8', index=False)
print("Dataset successfully saved.")
