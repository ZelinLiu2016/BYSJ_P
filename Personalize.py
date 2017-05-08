def airline_mat(best):
    file = open('airlines','r')
    dict = {}
    for i in file.read().split('\n'):
        dict[i] = 0
    dict[best] = 1
    return dict

def cabin_mat(best):
    file = open('cabins', 'r')
    dict = {}
    for i in file.read().split('\n'):
        dict[i] = 0
    dict[best] = 1
    return dict


def get_airways(sp,ep):
    #TODO: do not use hard code
    if (sp == 'SHA' and ep == 'SZX'):
        return [{"SHA":"TYO","TYO":"SZX"},{"SHA":"SZX"}]
    else:
        return [{sp:ep}]