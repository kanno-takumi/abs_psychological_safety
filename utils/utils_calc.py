#hierarchyは一度だけ計算される。
def calc_hierarchy(a1, a2, skill, age):
    hierarchy = a1 * skill + a2 * age
    return hierarchy

def calc_efficacy(a1, a2, hierarchy, efficacy, reaction, agree, t):
    if t == 0:
        efficacy = hierarchy
    if t > 0:
        efficacy = a1 * efficacy + a2 * reaction * (1 - agree)
    return efficacy
    
def calc_risk(efficacy, toughness):
    #行列で用意。
    risk = (1- toughness) * (1 - efficacy)
    return risk