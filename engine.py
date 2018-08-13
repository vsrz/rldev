
from entity import get_blocking_entities_at_location
from renderer import *
from input_handler import *
from map_objects.game_map import *
from fov import *
from vector import *
from game_states import GameStates
from components.fighter import Fighter
from death_functions import *
from game_messages import MessageLog

def main():
    # Screen
    screen_width = 80
    screen_height = 50

    # Map
    map_width = 80
    map_height = 43

    # Room generation
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 3

    # Health bar
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Message log
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    message_log = MessageLog(message_x, message_width, message_height)

    colors = {
        'dark_wall'     : libtcod.Color(0, 0, 100),
        'dark_ground'   : libtcod.Color(50, 50, 150),
        'light_wall'    : libtcod.Color(130, 110, 50),
        'light_ground'  : libtcod.Color(200, 180, 50),
    }

    ego = Entity(0, 0, '@', libtcod.white, 'Ego', False, fighter=Fighter(hp=30, defense=2, power=5),
                 render_order=RenderOrder.ACTOR)
    entities = [ego]

    # Main window
    con = libtcod.console_new(screen_width, screen_height)

    # Panel window
    panel = libtcod.console_new(screen_width, panel_height)

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
    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)


        if fov_recompute:
            recompute_fov(fov_map, ego.x, ego.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, panel, entities, ego, game_map, fov_map, fov_recompute, message_log,
                   screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors)
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


        player_turn_events = []
        if move and game_state == GameStates.PLAYERS_TURN:
            dst = Vector2i(ego.x + move[0], ego.y + move[1])
            if not game_map.is_blocked(dst.x, dst.y):
                target = get_blocking_entities_at_location(entities, dst)
                if target:
                    attack_results = ego.fighter.attack(target)
                    player_turn_events.extend(attack_results)
                else:
                    ego.move(move[0], move[1])

                game_state = GameStates.ENEMY_TURN
                fov_recompute = True

        if exit:
            return True

        for event in player_turn_events:
            message = event.get('message')
            dead_entity = event.get('dead')

            if message:
                message_log.add_message(message)
            if dead_entity:
                if dead_entity == ego:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)



        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_events = entity.ai.take_turn(ego, fov_map, game_map, entities)
                    for event in enemy_turn_events:
                        message = event.get('message')
                        dead_entity = event.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == ego:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            print(message)
                            if game_state == GameStates.PLAYER_DEAD:
                                break;
                    if game_state == GameStates.PLAYER_DEAD:
                        break;
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()



