from db import db
import re
import file_utils as fu
from spec import spec_db_utils as sdbu
from global_data import dict_model_options_data, model_options_data


def insert_options(model_id, fn):
    model_option_id = 0
    caption_parent_id = 0
    dict_option_name_id = 0
    dict_option_value_id = 0
    sub_caption_parent_id = 0

    data = fu.load_parsed_models(fn, 'Windows-1251')
    for d in data:
        if d:
            try:
                print(f'\rspecifications: {d[0]} - {d[1]}', end='')
            except:
                pass

            name = d[0]
            value = re.sub(r'(\smm+$)|(\sмм+$)|(\sстр+$)|(\sстр/мин$)|(\sкг$)|'
                           r'(\sВт$)|(\sлистов$)|(\sгг$)|(\sс$)|(\sсек$)', '', d[1])
            if name == 'main_image' or name == 'image':
                if name == 'main_image':
                    db.i_request(f'UPDATE models SET main_image = \'{value}\' WHERE id = {model_id}')
                else:
                    db.i_request(f'UPDATE models SET image = concat( s.image || \'{value}\'  || \';\') '
                                 f'FROM (SELECT image FROM models WHERE id = {model_id}) s WHERE models.id = {model_id}')
            else:
                if name != 'Model':
                    dict_option_name_id = set_convert({k for k, v in dict_model_options_data if v == name})
                    if dict_option_name_id < 1:
                        dict_option_name_id = sdbu.insert_dictionary_model_options(name)
                        dict_model_options_data.append((dict_option_name_id, name))

                    dict_option_value_id = set_convert({k for k, v in dict_model_options_data if v == value})
                    if dict_option_value_id < 1:
                        dict_option_value_id = sdbu.insert_dictionary_model_options(value)
                        dict_model_options_data.append((dict_option_value_id, value))

            if (name == 'Caption') | (name == 'Status'):
                caption_parent_id = search_model_options_data(dict_option_name_id, dict_option_value_id)
                if caption_parent_id < 1:
                    caption_parent_id = sdbu.insert_link_dictionary_model_options(dict_option_name_id, dict_option_value_id, 'Null')
                    model_options_data.append([caption_parent_id, dict_option_name_id, dict_option_value_id])
                sdbu.link_model_options(model_id, caption_parent_id)

            elif name == 'SubCaption':
                sub_caption_parent_id = search_model_options_data(dict_option_name_id, dict_option_value_id)
                if sub_caption_parent_id < 1:
                    sub_caption_parent_id = sdbu.insert_link_dictionary_model_options(dict_option_name_id, dict_option_value_id, caption_parent_id)
                    model_options_data.append([sub_caption_parent_id, dict_option_name_id, dict_option_value_id])
                sdbu.link_model_options(model_id, sub_caption_parent_id)

            elif name == 'EndSubCaption':
                sub_caption_parent_id = 0
            else:
                if sub_caption_parent_id:
                    model_option_id = sdbu.insert_link_dictionary_model_options(dict_option_name_id, dict_option_value_id, sub_caption_parent_id)
                else:
                    model_option_id = sdbu.insert_link_dictionary_model_options(dict_option_name_id, dict_option_value_id, caption_parent_id)

            if model_option_id and model_id:
                sdbu.link_model_options(model_id, model_option_id)


def set_convert(s):
    if len(s) < 1:
        v = 0
    else:
        v = list(s)[0]
    return v


def search_model_options_data(dict_option_name_id, dict_option_value_id):
    result = 0
    for item in model_options_data:
        if item[1] == dict_option_name_id:
            if item[2] == dict_option_value_id:
                result = item[0]
                break
    return result
