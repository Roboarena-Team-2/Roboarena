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
    # Initialize empty 23 x 46 inner field
    map1 = []
    for row in range(18):
        current_row = []
        for col in range(36):
            current_row.append("boden")
        map1.append(current_row)
        # map[y][x] — first index is Y (row), second is X (column)

    # Obstacles (dark gray = "rand")
    for x in range(1, 11):
        map1[3][x] = "rand"  # top left
    for y in range(8, 11):
        for x in range(16, 22):
            map1[y][x] = "rand"  # center block
    for y in range(13, 15):
        for x in range(29, 30):
            map1[y][x] = "rand"  # bottom right wall

    # Lava spots (red)
    lava_spots = [(4, 20), (1, 33), (8, 2), (11, 32), (12, 27), (16, 16)]
    for y, x in lava_spots:
        map1[y][x] = "lava"  # scattered lava tiles

    # Ice areas (light blue)
    for y in range(8, 11):
        for x in range(9, 13):
            map1[y][x] = "eis"  # bottom left
    for y in range(3, 6):
        for x in range(30, 33):
            map1[y][x] = "eis"  # top right

    # Sand zones (orange)
    for y in range(0, 4):
        for x in range(11, 13):
            map1[y][x] = "sand"  # top
    for y in range(11, 13):
        for x in range(14, 25):
            map1[y][x] = "sand"  # center wide area
    for y in range(15, 18):
        for x in range(29, 36):
            map1[y][x] = "sand"  # bottom right

    # Bush areas (green = "gebuesch")
    for y in range(11, 17):
        for x in range(2, 6):
            map1[y][x] = "gebuesch"  # bottom left area 1
    for y in range(13, 16):
        for x in range(6, 10):
            map1[y][x] = "gebuesch"  # bottom left area 2
    for y in range(1, 7):
        for x in range(25, 27):
            map1[y][x] = "gebuesch"  # vertical top right
    for y in range(14, 17):
        for x in range(19, 26):
            map1[y][x] = "gebuesch"  # center bottom

    return map1
