
class Tile:
    def __init__(self, blocked, blocked_sight=None):
        """
        A map tile. If it is a blocking tile, it could also block sight behind it
        for example, if this were a wall.
        :param blocked: If this is a blocking tile
        :param blocked_sight: If this tile blocks line of sight for things behind it
        """
        self.blocked = blocked

        # If a tile is blocked, it should also be blocked sight
        if blocked_sight is None:
            self.blocked_sight = blocked
        else:
            self.blocked_sight = blocked_sight

