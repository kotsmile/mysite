def k(wg):
    if wg < 15:
        return 0.9
    elif 15 <= wg < 17:
        return 1.0
    elif wg >= 17:
        return 1.1


def brock_index(h, w, wg, cg, a, gender):
    if 155 <= h <= 185:
        if gender == 'f':
            return (h - 100) * 0.85
        elif gender == 'm':
            return (h - 100) * 0.9
    return -1


def brock_age(h, w, wg, cg, a, gender):
    if a < 40:
        return h - 110
    elif a >= 40:
        return h - 100


def brock_brugsha_index(h, w, wg, cg, a, gender):
    if h < 165:
        return h - 100
    elif 165 <= h < 175:
        return h - 105
    elif h >= 175:
        return h - 110
    return -1


def mochamed_fromula(h, w, wg, cg, a, gender):
    return h ** 2 * 0.00225


def brock_index_k(h, w, wg, cg, a, gender):

    if h < 155:
        return (h - 95) * k(wg)
    elif 155 <= h < 175:
        return (h - 100) * k(wg)
    elif h >= 175:
        return (h - 110) * k(wg)
    return -1


def born_index(h, w, wg, cg, a, gender):
    return h * cg / 240


def monerota_formula(h, w, wg, cg, a, gender):
    return (h - 100 + 4 * wg) / 2


def kreffer_formula(h, w, wg, cg, a, gender):
    return (h - 100 + a / 10) * 0.9 * k(wg)


def strach_formula(h, w, wg, cg, a, gender):
    return 50 + 0.75 * (h - 150) + (a - 20) / 4


def lorenz_fromula(h, w, wg, cg, a, gender):
    if gender == 'm':
        return h - 100 - (h - 150) / 4
    elif gender == 'f':
        return h - 100 - (h - 150) / 2


def haliva_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 45.5 + 2.2 * (0.393701 * h - 60)
    elif gender == 'm':
        return 48 + 2.7 * (0.393701 * h - 60)


def nagshra_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 45.3 + 2.27 * (0.393701 * h - 60)
    elif gender == 'm':
        return 48 + 2.7 * (0.393701 * h - 60)


def cooper_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 0.624 * h - 48.9
    elif gender == 'm':
        return 0.713 * h - 58


def potton_index(h, w, wg, cg, a, gender):
    if gender == 'f':
        return h - 100 - h / 100
    elif gender == 'm':
        return h - 100 - h / 200


def devin_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 45.5 + 2.3 * (0.393701 * h - 60)
    elif gender == 'm':
        return 50 + 2.3 * (0.393701 * h - 60)


def robbinson_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 49 + 1.7 * (0.393701 * h - 60)
    elif gender == 'm':
        return 52 + 1.9 * (0.393701 * h - 60)


def miller_fromula(h, w, wg, cg, a, gender):
    if gender == 'f':
        return 53.1 + 1.36 * (0.393701 * h - 60)
    elif gender == 'm':
        return 56.2 + 1.41 * (0.393701 * h - 60)
