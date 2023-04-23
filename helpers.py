import config

def is_good_god(alignment: str) -> bool:
    if alignment.lower() in config.GOD_ALIGNMENTS_GOOD_LIST:
        return True
    else:
        return False

def is_higher_than_cardinal(position: str) -> bool:
    member_position_index = config.CLAN_POSITIONS_LIST.index(position)
    cardinal_index = config.CLAN_POSITIONS_LIST.index("кардинал")
    if member_position_index >= cardinal_index:
        return True
    else:
        return False