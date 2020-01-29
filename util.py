def hex2rgb(hex_val):
    return int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16)


def rgb2hex(rgb):
    hex_val = ""
    for i in range(3):
        value = str(hex(rgb[i]))
        if len(value) == 4:
            hex_val += value[2:4]
        else:
            hex_val += "0" + value[2]
    return hex_val
