
def Attack(unit1):    
        det = lambda abil: True
        return getBest(unit1,det)
#def CloseAttack(unit1):
#        det = lambda abil1,abil2: abil2.range < 3 and abil1.value > abil2.value
#        return getBest(unit1,det)
#def ProjectileAttack(unit1):
#        det = lambda abil1,abil2: abil2.range > 3 and abil1.value > abil2.value
#        return getBest(unit1,det)
#def SplashAttack(unit1):
#        det = lambda abil1,abil2: abil2.splash > 3 and abil1.value < abil2.value
#        return getBest(unit1,det)
         
def Healing(unit1):
        det = lambda abil: abil.type == "healing"
        return getBest(unit1,det)




