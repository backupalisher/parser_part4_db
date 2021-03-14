from db import db


def insert_dictionary_model_options(data):
    q = db.i_request(f"WITH s as (SELECT id FROM dictionary_model_options "
                     f"WHERE LOWER(text_ru) = LOWER('{data}')), i as "
                     f"(INSERT INTO dictionary_model_options (text_ru) SELECT '{data}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def insert_link_dictionary_model_options(dictionary_model_caption_id, dictionary_model_option_id, parent_id):
    q = db.i_request(f"WITH s as (SELECT id FROM link_dictionary_model_options WHERE "
                     f"dictionary_model_caption_id = {dictionary_model_caption_id} AND "
                     f"dictionary_model_option_id = {dictionary_model_option_id} AND "
                     f"parent_id = {parent_id}), "
                     f"i as (INSERT INTO link_dictionary_model_options (dictionary_model_caption_id, "
                     f"dictionary_model_option_id, parent_id) "
                     f"SELECT {dictionary_model_caption_id}, {dictionary_model_option_id}, {parent_id} "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) returning id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def link_model_options(model_id, link_dictionary_model_options_id):
    db.i_request(f"WITH s as (SELECT 1 FROM link_model_options "
                 f"WHERE model_id = {model_id} AND link_dictionary_model_options_id = {link_dictionary_model_options_id}), i as "
                 f"(INSERT INTO link_model_options (model_id, link_dictionary_model_options_id) "
                 f"SELECT {model_id}, {link_dictionary_model_options_id} "
                 f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) select * from i union all select * from s")


def get_id(table_name, where_name, param):
    return db.i_request(f"SELECT id FROM {table_name} WHERE {where_name} = '{param}'")
