import astroid
from collections.abc import Sequence, Mapping

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_function_id_from_call(call_node: astroid.Call,
                              _globals: "Mapping[str, Sequence[astroid.Expr]] | None" = None,
                              search_globals: bool = True,
                              cache_result: bool = True) -> str:
    """Retrieves the full name of a function."""
    # TODO: Do something with imports in globals to resolve aliases.

    if not isinstance(call_node, astroid.Call):
        raise ValueError("The provided node is not an astroid.Call object.")
    
    # Uses cached results if possible.
    if cache_result:
        full_name = getattr(call_node, 'full_name', None)
        if full_name:
            return full_name

    func = call_node.func
    if not isinstance(func, (astroid.Attribute, astroid.Name)):
        raise ValueError("Provided astroid.Call.func object is not astroid.Attribute or astroid.Name")
    
    parts = []
    
    # Resolves attributes untili name is found.
    current = func
    while isinstance(current, astroid.Attribute):
        parts.insert(0, current.attrname)
        current = current.expr
    if isinstance(current, astroid.Name):
        parts.insert(0, current.name)

    # Loads globals if necessary/wanted
    if _globals is None and search_globals:
        module = get_expr_module(call_node)
        # TODO: This should probably not be called globals, nor should it only consider globals (think about function scope etc.)
        _globals = module.globals

    # Resolves the root using globals (e.g., when its an imported call or a call on an object).
    root = parts[0]
    if not _globals is None and root in _globals:
        # NOTE: I assume there's only one related global; not sure in what cases there would be multiple, though.
        global_root = _globals[root][0]
        # NOTE: I assume this is an assign with a call as the value, not an import. This is completely unreasonable.
        if isinstance(global_root, astroid.AssignName):
            global_root = global_root.parent.value
            root_name = get_function_id_from_call(global_root, _globals)
            parts = parts[1:]
            parts.insert(0, root_name)
    
    full_name = ".".join(parts)

    if cache_result:
        setattr(call_node, "full_name", full_name)

    return full_name
    

def get_expr_module(expr: astroid.Expr) -> astroid.Module:
    current = expr
    while not isinstance(current, astroid.Module):
        current = current.parent
    return current


def build_kwargs(call_node: astroid.Call, keys: Sequence[str]) -> Mapping[str, astroid.Expr]:
    kwargs = {}
    kwargs.update({kw.arg: kw.value for kw in call_node.keywords})
    for key, value in zip(keys, call_node.args):
        if key in kwargs:
            raise ValueError("Passed keyword is already specified.")
        kwargs[key] = value
    # NOTE: This does not support astroid.Call.kwargs (yet), so these arguments are missing.
    return kwargs
