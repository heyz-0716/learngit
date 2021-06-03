from CoolProp.CoolProp import PropsSI
pressure = 101325
temperature = 373.15
fld = ['acetone.fld']
H = PropsSI('H','P',pressure,'T',temperature,'water')
print(H)