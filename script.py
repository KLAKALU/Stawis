__all__ = ['script']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['alert'])
@Js
def PyJsHoisted_alert_(name, this, arguments, var=var):
    var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
    var.registers(['name'])
    var.get('console').callprop('log', var.get('name'))
PyJsHoisted_alert_.func_name = 'alert'
var.put('alert', PyJsHoisted_alert_)
pass
pass


# Add lib to the module scope
script = var.to_python()