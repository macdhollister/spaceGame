planets_without_factions = [
        {
            'name': 'planet_a',
            'size': 's',
            'resources': 4,
            'owner': None,
            'facilities': [],
            'connections': ['planet_b', 'planet_c']
        },
        {
            'name': 'planet_b',
            'size': 'm',
            'resources': 3,
            'owner': None,
            'facilities': [],
            'connections': ['planet_a', 'planet_c']
        },
        {
            'name': 'planet_c',
            'size': 'l',
            'resources': 2,
            'owner': None,
            'facilities': [],
            'connections': ['planet_a', 'planet_b']
        }
    ]

planets_with_single_faction = [
        {
            'name': 'planet_a',
            'size': 's',
            'resources': 4,
            'owner': 'faction_1',
            'facilities': [],
            'connections': ['planet_b', 'planet_c']
        },
        {
            'name': 'planet_b',
            'size': 'm',
            'resources': 3,
            'owner': None,
            'facilities': [],
            'connections': ['planet_a', 'planet_c']
        },
        {
            'name': 'planet_c',
            'size': 'l',
            'resources': 2,
            'owner': None,
            'facilities': [],
            'connections': ['planet_a', 'planet_b']
        }
    ]
