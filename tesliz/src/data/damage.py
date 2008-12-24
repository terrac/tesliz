def basicPhysical(unit):
    fs = unit.attributes.physical
    dam = fs.power * (fs.power * fs.belief/100)
    return dam,"physical"
def halfBasicPhysical(unit):
    dam,type = basicPhysical(unit)
    return dam/2,type
def weaponPhysical(unit):
    fs = unit.attributes.physical
    wp = unit.items.get("weapon")
    dam = wp.power * (fs.power * fs.belief/100)
    return dam,"physical" 
def basicMagical(unit):
    fs = unit.attributes.magical
    dam =fs.power * (fs.power * fs.belief/100)
    return dam,"magical"

def test(unit):
    return 999,"magical"