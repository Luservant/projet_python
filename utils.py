import numpy as np


def moyenne_ponderee(groupe, col_valeur, col_poids="population"):
    """
    Calcule la moyenne pondérée d'une colonne par la population.

    Paramètres
    ----------
    groupe : pd.DataFrame
        Sous-groupe issu d'un groupby.
    col_valeur : str
        Colonne dont on veut la moyenne pondérée.
    col_poids : str
        Colonne des poids (défaut : population).
    """
    mask = groupe[col_valeur].notna() & (groupe[col_poids] > 0)
    if mask.sum() == 0:
        return np.nan
    return np.average(groupe.loc[mask, col_valeur], weights=groupe.loc[mask, col_poids])