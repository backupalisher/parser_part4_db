from asgiref.sync import sync_to_async
import file_utils as fu
import erc.erc_db_utils as erc_db
from global_data import erc_data


@sync_to_async
def insert_erc(model_id, fn):
    data = fu.load_parsed_models(fn, 'utf-8')
    code_data = {}
    for i, d in enumerate(data):
        if d[0] == 'Code':
            if d[1] and str(d[1]) != 'nan':
                if code_data:
                    error_code_id = erc_db.insert_error_code(dict(code_data))
                    if error_code_id:
                        erc_db.insert_link_model_error_code(model_id, error_code_id)

                # print(f'\rerror code: {d[1]}', end='')
                code_id = get_erc_id(d[0], d[1])
                if code_id < 1:
                    code_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                    code_data.update({'code': code_id})
                    erc_data.append({
                        'id': code_id,
                        'Code': d[1]
                    })
            else:
                code_data.update({'code': 0})

        elif d[0] == 'Display':
            if d[1] and str(d[1]) != 'nan':
                display_id = get_erc_id(d[0], d[1])
                if display_id < 1:
                    display_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                    code_data.update({'display': display_id})
                    erc_data.append({
                        'id': display_id,
                        'Display': d[1]
                    })
            else:
                code_data.update({'display': 0})

        elif d[0] == 'Image':
            if d[1] and str(d[1]) != 'nan':
                image_id = get_erc_id(d[0], d[1])
                if image_id:
                    image_id = erc_db.insert_dict_error_code('dictionary_error_code_image', 'image', d[1])
                    code_data.update({'image_id': image_id})
                    erc_data.append({
                        'id': image_id,
                        'Image': d[1]
                    })
            else:
                code_data.update({'remedy_id': 0})

        elif d[0] == 'Description':
            if d[1] and str(d[1]) != 'nan':
                description_id = get_erc_id(d[0], d[1])
                if description_id < 1:
                    description_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                    code_data.update({'description_id': description_id})
                    erc_data.append({
                        'id': description_id,
                        'Description': d[1]
                    })
            else:
                code_data.update({'remedy_id': 0})

        elif d[0] == 'Causes':
            if d[1] and str(d[1]) != 'nan':
                causes_id = get_erc_id(d[0], d[1])
                if causes_id < 1:
                    causes_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                    code_data.update({'causes_id': causes_id})
                    erc_data.append({
                        'id': causes_id,
                        'Causes': d[1]
                    })
            else:
                code_data.update({'causes_id': 0})

        elif d[0] == 'Remedy':
            if d[1] and str(d[1]) != 'nan':
                remedy_id = get_erc_id(d[0], d[1])
                if remedy_id < 1:
                    remedy_id = erc_db.insert_dict_error_code('dictionary_error_code', 'text_en', d[1])
                    code_data.update({'remedy_id': remedy_id})
                    erc_data.append({
                        'id': remedy_id,
                        'Remedy': d[1]
                    })
            else:
                code_data.update({'remedy_id': 0})
        if i+1 == len(data):
            error_code_id = erc_db.insert_error_code(dict(code_data))
            erc_db.insert_link_model_error_code(model_id, error_code_id)


def get_erc_id(name, value):
    result = 0
    for d in erc_data:
        try:
            if d[name] == value:
                result = d['id']
                break
        except:
            pass
    return result
