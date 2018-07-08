
from entity import get_blocking_entities_at_location
from renderer import *
from input_handler import *
from map_objects.game_map import *
from fov import *
from vector import *

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 3

    colors = {
        'dark_wall'     : libtcod.Color(0, 0, 100),
        'dark_ground'   : libtcod.Color(50, 50, 150),
        'light_wall'    : libtcod.Color(130, 110, 50),
        'light_ground'  : libtcod.Color(200, 180, 50),
    }

    ego = Entity(0, 0, '@', libtcod.white, 'Ego', False)
    entities = [ego]

    con = libtcod.console_new(screen_width, screen_height)
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, ego, entities,
                      max_monsters_per_room)

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
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

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities)

        action = process_input(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        light = action.get('light')

        if light:
            for y in range(game_map.height):
                for x in range(game_map.width):
                    game_map.tiles[x][y].explored = True
                    fov_recompute = True


        if move:
            dst = Vector2i(ego.x + move[0], ego.y + move[1])
            if not game_map.is_blocked(dst.x, dst.y) and not get_blocking_entities_at_location(entities, dst):
                ego.move(move[0], move[1])
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()



