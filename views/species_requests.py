import sqlite3
import json
from models import Species

def get_all_specieses():
    with sqlite3.connect("./assessment.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.name
        FROM species s
        """)
        specieses = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            species = Species(row['id'], row['name'])
            specieses.append(species.__dict__)
    return specieses


def get_single_species(id):
    with sqlite3.connect("./assessment.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.name
        FROM species s
        WHERE s.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        species = Species(data['id'], data['name'])
    return species.__dict__
