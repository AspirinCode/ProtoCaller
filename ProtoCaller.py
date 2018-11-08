import const as _const

import ensemble as _ensemble
import subdir as _subdir

#proteins = ["1BJI", "1A0O", "1AZ5"]

#e.g. Neuraminidase
with _subdir.Subdir("Temp", overwrite=True):
    protein = "1BJI"
    morphs = [["C1(=CC=CC=C1)CN(CC)CC", "C1(=CC=CC=C1)CN(CC)C"]]
    ligand_id = "479G"
    ensemble = _ensemble.Ensemble("GROMACS", protein=protein, morphs=morphs, ligand_id=ligand_id, box_length=6)
    ensemble.filterPDB(ligands=None, waters="site")
    ensemble.preparePDB(add_missing_atoms="modeller")
    ensemble.parametrisePDB()
    ensemble.parametriseLigands()
    ensemble.prepareComplexes()