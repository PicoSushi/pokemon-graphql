# coding: utf-8
import sqlite3
from contextlib import closing
import json

dbname = 'pokemon.db'


def create_table(cursor):
    for create_table in [
        'DROP TABLE IF EXISTS pokemon;', '''
        CREATE TABLE pokemon (
        _id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        form TEXT,
        is_mega_evolution BOOLEAN,
        stats JSON
        );
            ''', 'DROP TABLE IF EXISTS pokemon_evolution_pokemon;', '''
        CREATE TABLE pokemon_evolution_pokemon (
        pokemon_from_id INTEGER,
        pokemon_to_id INTEGER,
        FOREIGN KEY(pokemon_from_id) REFERENCES pokemon(id),
        FOREIGN KEY(pokemon_to_id) REFERENCES pokemon(id)
        );
            ''', 'DROP TABLE IF EXISTS ability;', '''
        CREATE TABLE ability (
        _id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        label TEXT
        );
            ''', 'DROP TABLE IF EXISTS pokemon_ability;', '''
        CREATE TABLE pokemon_ability (
        pokemon_id INTEGER,
        ability_id INTEGER,
        FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
        FOREIGN KEY(ability_id) REFERENCES ability(id)
        );
            ''', 'DROP TABLE IF EXISTS pokemon_hidden_ability;', '''
        CREATE TABLE pokemon_hidden_ability (
        pokemon_id INTEGER,
        ability_id INTEGER,
        FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
        FOREIGN KEY(ability_id) REFERENCES ability(id)
        );
            ''', 'DROP TABLE IF EXISTS type;', '''
        CREATE TABLE type (
        _id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        label TEXT
        );
            ''', 'DROP TABLE IF EXISTS pokemon_type;', '''
        CREATE TABLE pokemon_type (
        pokemon_id INTEGER,
        type_id INTEGER,
        FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
        FOREIGN KEY(type_id) REFERENCES type(id)
        );
        '''
    ]:
        cursor.execute(create_table)


def main():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table(c)

        with open('pokemon_data/data/pokemon_data.json', 'r') as f:
            pokemons = json.load(f)

        all_types = []
        all_abilities = []
        all_evolutions = []

        for pokemon in pokemons:
            c.execute(
                'INSERT INTO pokemon (name, form, is_mega_evolution, stats) VALUES (?, ?, ?, ?)',
                (
                    pokemon['name'],
                    pokemon['form'],
                    pokemon['isMegaEvolution'],
                    str(pokemon['stats']),
                ),
            )
            types = pokemon['types']
            for t in types:
                if t not in all_types:
                    c.execute('INSERT INTO type (label) VALUES (?)', (t, ))
                    all_types.append(t)
                # c.execute('INSERT INTO pokemon_type ()')
            abilities = pokemon['abilities']
            for a in abilities:
                if a not in all_abilities:
                    c.execute('INSERT INTO ability (label) VALUES (?)', (a, ))
                    all_abilities.append(a)

            hidden_abilities = pokemon['hiddenAbilities']
            for a in hidden_abilities:
                if a not in all_abilities:
                    c.execute('INSERT INTO ability (label) VALUES (?)', (a, ))
                    all_abilities.append(a)

            stats = pokemon['stats']

        conn.commit()


if __name__ == '__main__':
    main()
