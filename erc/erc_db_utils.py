import re
from db import db


def insert_error_code(code_array: dict):
    init_code_array = {'code': '0', 'display': '0', 'image_id': '0', 'description_id': '0', 'causes_id': '0', 'remedy_id': '0'}
    for key, value in code_array.items():
        init_code_array[key] = str(value)
    cols = ", ".join(list(init_code_array.keys()))
    vals = ", ".join(list(init_code_array.values()))

    q = db.i_request(f"INSERT INTO error_codes ({cols}) VALUES ({vals}) "
                     f"ON CONFLICT ({cols}) DO UPDATE SET code = excluded.code RETURNING id ")
    if q:
        return q[0][0]
    else:
        return 0


# перед тем как добавить проверяем на дубликаты
def insert_dict_error_code(dict_table, name, param):
    q = db.i_request(f"WITH s as (SELECT id FROM {dict_table} WHERE LOWER({name}) = LOWER('{param}')), "
                     f"i as (INSERT INTO {dict_table} ({name}) SELECT '{param}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) returning id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def insert_link_model_error_code(model_id, error_code_id):
    db.i_request(f'WITH s as (SELECT 1 FROM link_model_error_code '
                 f'WHERE model_id = {model_id} AND error_code_id = {error_code_id}), i as '
                 f'(INSERT INTO link_model_error_code (model_id, error_code_id) '
                 f'SELECT {model_id}, {error_code_id} WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) '
                 f'SELECT * FROM i UNION ALL SELECT * FROM s')


def update_code(erc_code_id, name, dict_id):
    db.i_request(f"UPDATE error_codes SET {name} = {dict_id} WHERE id = {erc_code_id}")
