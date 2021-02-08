from db import db


def insert_dict_modules(param):
    q = db.i_request(f"WITH s as (SELECT id FROM dictionary_modules "
                     f"WHERE LOWER(name_en) = LOWER('{param}')), i as "
                     f"(INSERT INTO dictionary_modules (name_en) SELECT '{param}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def insert_partcodes(param, description, pn_id, brand_id):
    q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                     f"WHERE LOWER(code) = LOWER('{param}') AND manufacturer = {brand_id}), i as "
                     f"(INSERT INTO partcodes (code, description, manufacturer, dictionary_partcode_id) "
                     f"SELECT '{param}', '{description}', {brand_id}, {pn_id}"
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def insert_dict_details(param):
    q = db.i_request(f"WITH s as (SELECT id FROM dictionary_partcode "
                     f"WHERE LOWER(name_en) = LOWER('{param}')), i as "
                     f"(INSERT INTO dictionary_partcode (name_en) SELECT '{param}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def insert_dict_module_image(param):
    q = db.i_request(f"WITH s as (SELECT id FROM dictionary_module_image "
                     f"WHERE image = '{param}'), i as "
                     f"(INSERT INTO dictionary_module_image (image) SELECT '{param}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def link_model_module_image(model_id, module_id, img_id):
    db.i_request(f"WITH s as (SELECT 1 FROM link_model_module_image "
                 f"WHERE model_id = {model_id} AND dictionary_module_id = {module_id} AND dictionary_module_image_id = {img_id}), "
                 f"i as (INSERT INTO link_model_module_image (model_id, dictionary_module_id, dictionary_module_image_id) "
                 f"SELECT {model_id}, {module_id}, {img_id} WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) "
                 f"SELECT * FROM i UNION ALL SELECT * FROM s")


def link_model_module_partcode(pc_id, model_id, module_id):
    db.i_request(f'WITH s as (SELECT 1 FROM link_model_module_partcode '
                 f'WHERE partcode_id = {pc_id} AND model_id = {model_id} AND module_id = {module_id}), i as '
                 f'(INSERT INTO link_model_module_partcode (partcode_id, model_id, module_id) '
                 f'SELECT {pc_id}, {model_id}, {module_id} WHERE NOT EXISTS '
                 f'(SELECT 1 FROM s) RETURNING 0) SELECT * FROM i UNION ALL SELECT * FROM s')


def insert_partcodes_article(article_code, description, pn_id, brand_id):
    q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                     f"WHERE LOWER(article_code) = LOWER('{article_code}') AND manufacturer = {brand_id}), i as "
                     f"(INSERT INTO partcodes (article_code, description, manufacturer, dictionary_partcode_id) "
                     f"SELECT '{article_code}', '{description}', {brand_id}, {pn_id}"
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]