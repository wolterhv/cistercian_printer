#!/usr/bin/env python3

import sys

def flip_corner_h(corner_string):
    # [0] -> [1]
    # [1] -> [0]
    # [2] -> [3]
    # [3] -> [2]
    # [4] -> [5]
    # [5] -> [4]
    #
    # Also,
    #
    # / -> \
    # \ -> /
    flipped_string =   corner_string[1] \
                     + corner_string[0] \
                     + corner_string[3] \
                     + corner_string[2] \
                     + corner_string[5] \
                     + corner_string[4]
    if "/" in flipped_string:
        flipped_string = flipped_string.replace("/","\\")
    elif "\\" in flipped_string:
        flipped_string = flipped_string.replace("\\", "/")

    return flipped_string

def flip_corner_v(corner_string):
    # [0] -> [4]
    # [1] -> [5]
    # [2] -> [2]
    # [3] -> [3]
    # [4] -> [0]
    # [5] -> [1]
    #
    # Also,
    #
    # / -> \
    # \ -> /
    flipped_string =   corner_string[4] \
                     + corner_string[5] \
                     + corner_string[2] \
                     + corner_string[3] \
                     + corner_string[0] \
                     + corner_string[1]
    if "/" in flipped_string:
        flipped_string = flipped_string.replace("/","\\")
    elif "\\" in flipped_string:
        flipped_string = flipped_string.replace("\\", "/")

    return flipped_string

def get_joiner_10(left_string, right_string):
    if      (   ("-" == left_string[1]) or ( "-" == right_string[0]) \
             or ("/" == left_string[3]) or ("\\" == right_string[2])):
        return "+"
    else:
        return "|"

def get_joiner_54(left_string, right_string):
    if      (   ( "-" == left_string[5]) or ("-" == right_string[4]) \
             or ("\\" == left_string[3]) or ("/" == right_string[2])):
        return "+"
    else:
        return "|"

#           +-+-+
#      tens | | | units
#           +-+-+
#           . | .
#           . + .
# thousands ./|\. hundreds
#           +-+-+
#
# [0][1][0][0][1]
# [2][3] | [2][3]
# [4][5][1][4][5]
#        |
# [0][1][2][0][1]
# [2][3] | [2][3]
# [4][5][3][4][5]
#
def get_cistercian_from_integer(integer):
    thousands = 0
    hundreds = 0
    tens = 0
    units = 0

    cistercian_unit_strings = [
        "      ", # 0
        "--    ", # 1
        "    --", # 2
        "  \  +", # 3
        " +/   ", # 4
        "-+/   ", # 5
        " + | +", # 6
        "-+ | +", # 7
        " + |-+", # 8
        "-+ |-+", # 9
    ]

    integer = integer % 10000

    thousands = int(integer/1000)
    hundreds  = int((integer - 1000 * thousands) / 100)
    tens      = int((integer - 1000 * thousands - 100 * hundreds) / 10)
    units     = int((integer - 1000 * thousands - 100 * hundreds - 10 * tens) / 1)

    thousands_string = flip_corner_h(flip_corner_v(cistercian_unit_strings[thousands]))
    hundreds_string  = flip_corner_v(              cistercian_unit_strings[hundreds])
    tens_string      = flip_corner_h(              cistercian_unit_strings[tens])
    units_string     =                             cistercian_unit_strings[units]

    cistercian_string =        tens_string[0:2] +                                              "+" + units_string[0:2]    + "\n" \
                        +      tens_string[2:4] +                                              "|" + units_string[2:4]    + "\n" \
                        +      tens_string[4:6] + get_joiner_54(     tens_string,    units_string) + units_string[4:6]    + "\n" \
                        +                  "  " +                                              "|" +                 "  " + "\n" \
                        + thousands_string[0:2] + get_joiner_10(thousands_string, hundreds_string) + hundreds_string[0:2] + "\n" \
                        + thousands_string[2:4] +                                              "|" + hundreds_string[2:4] + "\n" \
                        + thousands_string[4:6] +                                              "+" + hundreds_string[4:6]

    return cistercian_string

if __name__ == "__main__":
    print(get_cistercian_from_integer(int(sys.argv[1])))
