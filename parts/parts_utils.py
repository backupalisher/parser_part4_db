import re
import file_utils as fu
from parts import parts_db_utils
from global_data import parts_data


def insert_parts(model_id, fn):
    data = fu.load_parsed_models(fn, 'utf-8')
    old_module = ''
    old_module_id = 0
    old_img = ''
    for d in data:
        module_id = 0
        pc_id = 0
        try:
            print(f'\rpart code: {d[0]} - {d[1]}', end='')
        except:
            pass
        # добавляем модуль
        if d[0]:
            module_name = re.sub(f'\(\d\u0020of\u0020\d\)|\d\u0020of\u0020\d$|[Internal components]\d$', '', d[0]).strip()
            if old_module != module_name:
                old_module = module_name
                module_id = get_id('module', module_name)
                if module_id < 1:
                    module_id = parts_db_utils.insert_dict_modules(module_name)
                    parts_data.append({
                        'id': module_id,
                        'module': module_name
                    })
                old_module_id = module_id
            else:
                module_id = old_module_id

        # добавляем в partcodes новый парткод
        if d[1]:
            pc_id = get_id('pc', d[1])
            if pc_id < 1:
                pc_id = parts_db_utils.insert_partcodes(d[1], d[3])
                parts_data.append({
                    'id': pc_id,
                    'pc': d[1]
                })

        # добавляем в справочник наименование детали
        if d[2]:
            pn_id = get_id('pn', d[2])
            if pn_id < 1:
                pn_id = parts_db_utils.insert_dict_details(d[2])
                parts_data.append({
                    'id': pn_id,
                    'pn': d[2]
                })

        # добавляем картинку модуля
        if d[4]:
            if old_img != d[4]:
                img_id = parts_db_utils.insert_dict_module_image(d[4])
                parts_db_utils.link_model_module_image(model_id, module_id, img_id)
                old_img = d[4]

        # линкуем парткод-модель-модуль
        parts_db_utils.link_model_module_partcode(pc_id, model_id, module_id)


def get_id(name, value):
    result = 0
    for d in parts_data:
        try:
            if d[name] == value:
                result = d['id']
                break
        except:
            pass
    return result
