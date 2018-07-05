from entity import Entity
from renderer import *
from input_handler import *
from map_objects.game_map import *
from fov import *

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall'     : libtcod.Color(0, 0, 100),
        'dark_ground'   : libtcod.Color(50, 50, 150),
        'light_wall'    : libtcod.Color(130, 110, 50),
        'light_ground'  : libtcod.Color(200, 180, 50),
    }

    # ego = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    # npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2), '@', libtcod.yellow)
    ego = Entity(0, 0, '@', libtcod.white)
    actors = [ego]

    con = libtcod.console_new(screen_width, screen_height)
    fov_recompute = True
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, ego, actors, 3)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, ego.x, ego.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, actors, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        libtcod.console_flush()
        clear_all(con, actors)

        action = process_input(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        light = action.get('light')

        if light:
            for y in range(game_map.height):
                for x in range(game_map.width):
                    game_map.tiles[x][y].explored = True


        if move and not game_map.is_blocked(ego.x + move[0], ego.y + move[1]):
            ego.move(move[0],move[1])

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()



