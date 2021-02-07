import file_utils as fu
import erc.erc_db_utils as erc_db


def insert_erc(model_id, fn):
    data = fu.load_parsed_models(fn, 'utf-8')
    code_data = {}
    for d in data:
        if d[0] == 'Code':
            if d[1] and str(d[1]) != 'nan':
                if code_data:
                    error_code_id = erc_db.insert_error_code(dict(code_data))
                    if error_code_id:
                        erc_db.insert_link_model_error_code(model_id, error_code_id)

                print(f'\rerror code: {d[1]}', end='')
                code_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                code_data.update({'code': code_id})
            else:
                code_data.update({'code': 0})

        elif d[0] == 'Display':
            if d[1] and str(d[1]) != 'nan':
                display_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                code_data.update({'display': display_id})
            else:
                code_data.update({'display': 0})

        elif d[0] == 'Image':
            if d[1] and str(d[1]) != 'nan':
                spr_image_id = erc_db.insert_dict_error_code('dictionary_error_code_image', 'image', d[1])
                code_data.update({'image_id': spr_image_id})
            else:
                code_data.update({'remedy_id': 0})

        elif d[0] == 'Description':
            if d[1] and str(d[1]) != 'nan':
                spr_erc_code_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                code_data.update({'description_id': spr_erc_code_id})
            else:
                code_data.update({'remedy_id': 0})

        elif d[0] == 'Causes':
            if d[1] and str(d[1]) != 'nan':
                spr_erc_code_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                code_data.update({'causes_id': spr_erc_code_id})
            else:
                code_data.update({'causes_id': 0})

        elif d[0] == 'Remedy':
            if d[1] and str(d[1]) != 'nan':
                spr_erc_code_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                code_data.update({'remedy_id': spr_erc_code_id})
            else:
                code_data.update({'remedy_id': 0})
