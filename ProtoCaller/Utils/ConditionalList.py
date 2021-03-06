class ConditionalList(list):
    """
    A class that conditionally accepts new elements based on user-defined functions.

    Parameters
    ----------
    input_list : list
       Name of the input list.
    checkfuncs
        Positional arguments which need to be callable. These are the functions which are used to check any added
        element. These should throw an error if the element should not be a part of the list.
    transformfunc
        A callable which optionally transforms the input after the checks and before addition to the list.
    """
    def __init__(self, input_list, *checkfuncs, transformfunc=None):
        if checkfuncs is None: checkfuncs = []
        if not isinstance(input_list, list):
            input_list = [input_list]
        for checkfunc in checkfuncs:
            if not hasattr(checkfunc, "__call__"):
                raise TypeError("Need to pass a callable function as a parameter")
            for item in input_list:
                checkfunc(item)
        if transformfunc is not None:
            input_list = [transformfunc(x) for x in input_list]
        list.__init__(self, input_list)
        self._checkfuncs = list(checkfuncs)
        self._transformfunc = transformfunc

    def __getattribute__(self, item):
        if item in ["__add__", "__iadd__", "append", "extend", "insert", "remove"]:
            return self._check(super().__getattribute__(item))
        return super().__getattribute__(item)

    def _check(self, listfunc):
        def decorated(*args):
            if self:
                items = args[-1]
                if not isinstance(items, list):
                    items = [items]
                for checkfunc in self._checkfuncs:
                    for item in items:
                        checkfunc(item)
                if self._transformfunc is not None:
                    items = [self._transformfunc(x) for x in items]
                    return listfunc(*args[:-1], items)
            return listfunc(*args)
        return decorated
