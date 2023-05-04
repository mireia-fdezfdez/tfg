from utils import *

# recollim tots els fitxers en un únic llistat
escenaris = [file for file in os.scandir("Scenarios")]

# inicialització dels datasets finals
final_dataset_entr = pd.DataFrame(columns=["Node", "NumCont", "DURC", "ICT", "EC", "Escenari"])
final_dataset_val = pd.DataFrame(columns=["Node", "NumCont", "DURC", "ICT", "EC", "Escenari"])

# itera per tots els fitxers i extreu les dades
for xarxa, escenari in zip(escenaris, range(1, len(escenaris) + 1)):
    dataset = pd.read_csv(xarxa, sep=" ", header=None)
    dataset.columns = ["Time", "CONN", "Node", "Node2", "Type"]
    dataset.drop(["CONN"], axis=1, inplace=True)

    # afegim el "Node2" a la columna "Node" per a tenir en compte la connexió en les dues direccions
    dataset = dues_direccions(dataset)
    print("Dades de l'escenari", escenari, "modificades.")

    ratio_validacio = 0.2
    nodes_escenari = dataset.Node.unique()

    nodes_validacio = []
    for _ in range(int(max(nodes_escenari) * ratio_validacio)):
        nodes_validacio.append(random.choice(nodes_escenari))

    entrenament = dataset[~dataset.Node.isin(nodes_validacio)]
    validacio = dataset[dataset.Node.isin(nodes_validacio)]

    one_file_entr = entrenament.groupby(['Node'])["Node2"].size().reset_index(name='NumCont')
    one_file_val = validacio.groupby(['Node'])["Node2"].size().reset_index(name='NumCont')

    temps_train = entrenament.groupby(['Node', 'Node2']).agg(pair_DURC=("Time", mitjana_duracio_conns),
                                                             pair_ICT=("Time", mitjana_entre_conns)).reset_index()
    final_attrs_train = temps_train.groupby(['Node']).agg(DURC=("pair_DURC", np.mean), ICT=("pair_ICT", np.mean)).reset_index()
    temps_test = validacio.groupby(['Node', 'Node2']).agg(pair_DURC=("Time", mitjana_duracio_conns),
                                                          pair_ICT=("Time", mitjana_entre_conns)).reset_index()
    final_attrs_test = temps_test.groupby(['Node']).agg(DURC=("pair_DURC", np.mean), ICT=("pair_ICT", np.mean)).reset_index()

    ec_entrenament = entrenament.groupby(['Node'], as_index=False).apply(centralitat_elastica)
    ec_validacio = validacio.groupby(['Node'], as_index=False).apply(centralitat_elastica)

    one_file_entr = one_file_entr.merge(final_attrs_train, how='inner')
    one_file_entr = one_file_entr.merge(ec_entrenament, how='inner')
    one_file_entr["Escenari"] = escenari

    one_file_val = one_file_val.merge(final_attrs_test, how='inner')
    one_file_val = one_file_val.merge(ec_validacio, how='inner')
    one_file_val["Escenari"] = escenari

    final_dataset_train = pd.concat([one_file_entr, final_dataset_entr], ignore_index=True)
    final_dataset_test = pd.concat([one_file_val, final_dataset_val], ignore_index=True)
    print("Escenari", escenari, "afegit!\n")

# guarda els datasets complets en un fitxer a part
final_dataset_entr.to_csv("all_scenarios_train.csv", encoding='utf-8', index=False)
final_dataset_val.to_csv("all_scenarios_test.csv", encoding='utf-8', index=False)

print("Dades guardades correctament.")
