import sqlite3
import json
from models import Snake

def get_all_snakes(query_params):
    with sqlite3.connect("./assessment.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sort_by = ""
        where_clause = ""
        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "species":
                if qs_value == '1':
                    sort_by = " ORDER BY sp.name"
                    where_clause = f"WHERE s.species_id = {qs_value}"
                elif qs_value == '2':
                    sort_by = " ORDER BY sp.name"
                    where_clause = f"WHERE s.species_id = {qs_value}"
                elif qs_value == '3':
                    sort_by = " ORDER BY sp.name"
                    where_clause = f"WHERE s.species_id = {qs_value}"
                elif qs_value == '4':
                    sort_by = " ORDER BY sp.name"
                    where_clause = f"WHERE s.species_id = {qs_value}"
                elif qs_value == '5':
                    sort_by = " ORDER BY sp.name"
                    where_clause = f"WHERE s.species_id = {qs_value}"


            # elif qs_key == "status":
            #     if qs_value == 'Treatment':
            #         sort_by = " ORDER BY status"
            #         where_clause = f"WHERE a.status = \'{qs_value}\'"
        # else:
        #     where_clause = ""


        sql_to_execute = f"""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color,
            sp.id,
            sp.name
        FROM Snakes s
        JOIN `Species` sp
            on sp.id = s.species_id
            {where_clause}
            {sort_by}
        """
        db_cursor.execute(sql_to_execute)
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
            s.color,
            sp.id,
            sp.name
        FROM Snakes s
        JOIN `Species` sp
            on sp.id = s.species_id
        WHERE s.id = ? and s.species_id != 2
        """, ( id, ))
        data = db_cursor.fetchone()
        if data is None:
            return ""
        else:
            snake = Snake(data['id'], data['name'], data['owner_id'], data['species_id'], data['gender'], data['color'])
    return snake.__dict__

def create_snake(new_snake):
    with sqlite3.connect("./assessment.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Snakes
            ( name, owner_id, species_id, gender, color )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_snake['name'], new_snake['owner_id'],
                new_snake['species_id'], new_snake['gender'],
                new_snake['color'], ))

        id = db_cursor.lastrowid

        new_snake['id'] = id
    return new_snake