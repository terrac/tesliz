def basicPhysical(unit):
    fs = unit.attributes.physical
    dam = fs.power * (fs.power * fs.belief/100)
    return dam,"physical" 
def basicMagical(unit):
    fs = unit.attributes.physical
    dam =fs.power * (fs.power * fs.belief/100)
    return dam,"magical"