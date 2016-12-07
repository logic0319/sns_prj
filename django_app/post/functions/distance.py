__all__ = ('cal_distance',)

def cal_distance(stand, element):
    lkm = abs(stand[0] - element[0])*92
    hkm = abs(stand[1] - element[1])*114
    distance = (lkm**2 + hkm**2)**0.5
    return distance

