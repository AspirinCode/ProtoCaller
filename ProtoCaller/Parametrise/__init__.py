import ProtoCaller as _PC

if _PC.BIOSIMSPACE:
    import BioSimSpace as _BSS

import ProtoCaller.Wrappers.parmedwrapper as _pmdwrap
from . import _amber

class Params:
    def __init__(self, protein_ff=_PC.AMBERDEFAULTPROTEINFF, ligand_ff=_PC.AMBERDEFAULTLIGANDFF,
                 water_ff=_PC.AMBERDEFAULTWATERFF):
        self.protein_ff = protein_ff
        self.ligand_ff = ligand_ff
        self.water_ff = water_ff

    @property
    def protein_ff(self):
        return self._protein_ff

    @protein_ff.setter
    def protein_ff(self, val):
        val = val.strip()
        if val not in _PC.PROTEINFFS:
            raise ValueError("Value %s not supported. Supported values: " % val, _PC.PROTEINFFS)
        self._protein_ff = val

    @property
    def ligand_ff(self):
        return self._ligand_ff

    @ligand_ff.setter
    def ligand_ff(self, val):
        val = val.strip()
        if val not in _PC.LIGANDFFS:
            raise ValueError("Value %s not supported. Supported values: " % val, _PC.LIGANDFFS)
        self._ligand_ff = val

    @property
    def water_ff(self):
        return self._water_ff

    @water_ff.setter
    def water_ff(self, val):
        val = val.strip()
        if val not in _PC.WATERFFS:
            raise ValueError("Value %s not supported. Supported values: " % val, _PC.WATERFFS)
        self._water_ff = val

def parametriseAndLoadPmd(params, *args, **kwargs):
    files = parametriseFile(params, *args, **kwargs)
    return _pmdwrap.openFilesAsParmed(files)

def parametriseAndLoadBSS(params, *args, **kwargs):
    if _PC.BIOSIMSPACE:
        files = parametriseFile(params, *args, **kwargs)
        return _BSS.IO.readMolecules(files)
    else:
        raise ImportError("BioSimSpace module cannot be imported")

def parametriseFile(params, filename, molecule_type, fix_charge=True, id=None, *args, **kwargs):
    if id is None: id = molecule_type
    files = []

    if molecule_type == "protein":
        if params.protein_ff in _PC.AMBERPROTEINFFS:
            files = _amber.amberWrapper(params, filename, molecule_type, id, *args, **kwargs)
    elif molecule_type in ["ligand", "cofactor"]:
        if params.ligand_ff in _PC.AMBERLIGANDFFS:
            files = _amber.amberWrapper(params, filename, molecule_type, id, *args, **kwargs)
    elif molecule_type in ["water", "simple_anion", "complex_anion", "simple_cation", "complex_cation"]:
        if params.water_ff in _PC.AMBERWATERFFS:
            files = _amber.amberWrapper(params, filename, molecule_type, id, *args, **kwargs)
    else:
        raise ValueError("Invalid argument: %s. Argument must be one of: protein, ligand, cofactor, simple_anion, "
                         "complex_anion, simple_cation, complex_cation or water." % molecule_type)

    if files:
        return _pmdwrap.fixCharge(files) if fix_charge else files
    else:
        raise ValueError("No force fields available for the input system")
