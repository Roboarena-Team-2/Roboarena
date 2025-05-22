# Possible colors:
COLORS = {
    "boden": (180, 180, 180),       # gray (ground)
    "rand": (60, 60, 60),           # dark gray (walls)
    "lava": (255, 0, 0),            # red
    "eis": (115, 155, 208),         # light blue (ice)
    "sand": (235, 185, 120),        # orange (sand)
    "gebuesch": (0, 128, 0),        # green (bush)
}


def get_map1():
    # Initialize empty 25 x 46 inner field
    map1 = []
    for row in range(25):
        current_row = []
        for col in range(46):
            current_row.append("boden")
        map1.append(current_row)
        # map[y][x] — first index is Y (row), second is X (column)

    # Obstacles (dark gray = "rand")
    for x in range(3, 13):
        map1[3][x] = "rand"  # top left
    for y in range(10, 13):
        for x in range(20, 26):
            map1[y][x] = "rand"  # center block
    for y in range(19, 22):
        for x in range(38, 39):
            map1[y][x] = "rand"  # bottom right wall

    # Lava spots (red)
    lava_spots = [(4, 21), (2, 42), (8, 2), (14, 40), (16, 31), (21, 17)]
    for y, x in lava_spots:
        map1[y][x] = "lava"  # scattered lava tiles

    # Ice areas (light blue)
    for y in range(14, 17):
        for x in range(9, 13):
            map1[y][x] = "eis"  # bottom left
    for y in range(4, 7):
        for x in range(35, 38):
            map1[y][x] = "eis"  # top right

    # Sand zones (orange)
    for y in range(0, 4):
        for x in range(13, 15):
            map1[y][x] = "sand"  # top
    for y in range(13, 15):
        for x in range(18, 29):
            map1[y][x] = "sand"  # center wide area
    for y in range(22, 25):
        for x in range(38, 46):
            map1[y][x] = "sand"  # bottom right

    # Bush areas (green = "gebuesch")
    for y in range(18, 24):
        for x in range(3, 7):
            map1[y][x] = "gebuesch"  # bottom left area 1
    for y in range(20, 24):
        for x in range(7, 11):
            map1[y][x] = "gebuesch"  # bottom left area 2
    for y in range(2, 8):
        for x in range(29, 32):
            map1[y][x] = "gebuesch"  # vertical top right
    for y in range(18, 21):
        for x in range(22, 29):
            map1[y][x] = "gebuesch"  # center bottom

    return map1

