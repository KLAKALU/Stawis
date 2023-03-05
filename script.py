__all__ = ['script']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['al'])
@Js
def PyJsHoisted_al_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get('window').callprop('alert', Js('存在しないISBNが入力されました'))
PyJsHoisted_al_.func_name = 'al'
var.put('al', PyJsHoisted_al_)
pass
pass


# Add lib to the module scope
script = var.to_python()