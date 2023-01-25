import sqlite3
import json
from models import Snake

def get_all_snakes():
    with sqlite3.connect("./assessment.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
        FROM Snakes s
        """)
        snakes = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            snake = Snake(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])
            snakes.append(snake.__dict__)
    return snakes


def get_single_snake(id):
    with sqlite3.connect("./assessment.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
        FROM Snakes s
        WHERE s.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        snake = Snake(data['id'], data['name'], data['owner_id'], data['species_id'], data['gender'], data['color'])
    return snake.__dict__
