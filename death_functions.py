
import tcod as libtcod
from renderer import RenderOrder
from game_messages import Message

from game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died!', libtcod.dark_red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} has been slain!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.render_order = RenderOrder.CORPSE
    monster.name = 'remains of ' + monster.name

    return Message(death_message, libtcod.orange)

