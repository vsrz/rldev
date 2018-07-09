import tcod as libtcod



def process_input(key):
    ch = chr(key.c)

    if key.vk == libtcod.KEY_UP or ch == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or ch == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or ch == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or ch == 'l':
        return {'move': (1, 0)}
    elif ch == 'y':
        return {'move' : (-1, -1)}
    elif ch == 'u':
        return {'move' : (1, -1)}
    elif ch == 'b':
        return {'move' : (-1, 1)}
    elif ch == 'n':
        return {'move' : (1, 1)}

    if ch == 'z':
        return { 'light' : True }


    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


