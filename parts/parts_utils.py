import re

from asgiref.sync import sync_to_async

import file_utils as fu
import generat_article_code as gac
from parts import parts_db_utils
from global_data import parts_data


@sync_to_async
def insert_parts(brand_id, model_id, fn):
    data = fu.load_parsed_models(fn, 'utf-8')
    old_module = ''
    old_module_id = 0
    old_img = ''
    for d in data:
        module_id = 0
        pn_id = 0
        pc_id = 0
        # try:
        #     print(f'\rpart code: {d[0]} - {d[1]}', end='')
        # except:
        #     pass
        # добавляем модуль
        if d[0] and str(d[0]) != 'nan':
            module_name = d[0]
            bad_list = [f'\(\d\u0020of\u0020\d\)|',
                        f'\d\u0020of\u0020\d|',
                        f'\(\dof\d\)|',
                        f'(?<=Base\u0020)\d$|',
                        f'(?<=Base)\d$|',
                        f'(?<=Electrical\u0020)\d$|',
                        f'(?<=Electrical)\d$|',
                        f'(?<=ARDF\u0020)\d$|',
                        f'(?<=ARDF)\d$|',
                        f'(?<=components\u0020)\d$|',
                        f'(?<=ADF\u0020)\d$|',
                        f'(?<=ADF)\d$|',
                        f'(?<=PANEL\u0020)\d$|',
                        f'(?<=PANEL)\d$|',
                        f'\d/\d$|',
                        f'\(\d/\d\)|',
                        f'\(\d\)$|',
                        f'\(\d\u0020/\u0020\d\)|',
                        f'(?<=sheet tray insert\u0020)\d$|',
                        f'(?<=sheet tray insert)\d$|',
                        f'(?<=maker\u0020)\d$|',
                        f'(?<=maker)\d$|',
                        f'(?<=Folder\u0020)\d$|',
                        f'(?<=Folder)\d$|',
                        f'(?<=ADU\u0020)\d$|',
                        f'(?<=ADU)\d$|',
                        f'(?<=pick\u0020)\d$|',
                        f'(?<=pick)\d$|',
                        f'(?<=CASSETTE\u0020)\d$|',
                        f'(?<=CASSETTE)\d$|',
                        f'(?<=SECTION\u0020)\(\d\)$|',
                        f'(?<=SECTION)\(\d\)$|',
                        f'(?<=Assembly\u0020)\(\d\)$|',
                        f'(?<=Assembly)\(\d\)$|',
                        f'(?<=Assembly\u0020)\d$|',
                        f'(?<=Assembly)\d$|',
                        f'(?<=Area\u0020)\(\d\)$|',
                        f'(?<=Area)\(\d\)$|',
                        f'(?<=Area\u0020)\d$|',
                        f'(?<=Area)\d$|',
                        f'(?<=Option\u0020)\d$|',
                        f'(?<=Option)\d$|',
                        f'(?<=SECTION\u0020)\d$|',
                        f'(?<=SECTION)\d$|',
                        f'(?<=Carriage\u0020)\(\d\)$|',
                        f'(?<=Carriage)\(\d\)$|',
                        f'(?<=Carriage\u0020)\d$|',
                        f'(?<=Carriage)\d$|',
                        f'(?<=diagram\u0020)\d$|',
                        f'(?<=diagram)\d$|',
                        f'(?<=Paper pick\u0020)\d$|',
                        f'(?<=Paper pick)\d$|',
                        f'(?<=Tray\u0020)\d$|',
                        f'(?<=Tray)\d$|',
                        f'(?<=HARDWARE\u0020)\d$|',
                        f'(?<=HARDWARE)\d$|',
                        f'(?<=ETC\.\u0020)\d$|',
                        f'(?<=ETC\.)\d$|',
                        f'(?<=DOOR ASSEMBLY\u0020)\d$|',
                        f'(?<=DOOR ASSEMBLY)\d$|',
                        f'(?<=ASSEMBLY, RIGHT\u0020)\d$|',
                        f'(?<=ASSEMBLY, RIGHT)\d$|',
                        f'(?<=Feed\u0020)\(\d\)$|',
                        f'(?<=Feed)\(\d\)$|',
                        f'(?<=unit\u0020)\(\d\)$|',
                        f'(?<=unit)\(\d\)$|',
                        f'(?<=unit\u0020)\d$|',
                        f'(?<=unit)\d$|',
                        f'(?<=Feed\u0020)\d$|',
                        f'(?<=Feed)\d$|',
                        f'(?<=LABELS\u0020)\(\d\)$|',
                        f'(?<=LABELS)\(\d\)$|',
                        f'(?<=LABELS\u0020)\d$|',
                        f'(?<=LABELS)\d$|',
                        f'(?<=Frame\u0020)\d$|',
                        f'(?<=Frame)\d$|',
                        f'(?<=CASSETTE\u0020)\(\d\)$|',
                        f'(?<=CASSETTE)\(\d\)$|',
                        f'\(\u0020\d\u0020/\u0020\d\u0020\)$|',
                        f'\(\d\)$|',
                        f'\(\u0020\d\u0020\)$|',
                        f'(?<=insert\u0020)\d$|',
                        f'(?<=insert)\d$|',
                        f'(?<=ASSY\u0020)\d$|',
                        f'(?<=ASSY)\d$|',
                        f'(?<=ASSEMBLY\u0020)\d$|',
                        f'(?<=ASSEMBLY)\d$|',
                        f'(?<=ASSEMBLY\u0020)\(\d\)$|',
                        f'(?<=ASSEMBLY)\(\d\)$|',
                        f'(?<=sensors\u0020)\d$|',
                        f'(?<=sensors)\d$|',
                        f'(?<=\(Registration Section\))\d$|',
                        f'(?<=assemblies\u0020)\d$|',
                        f'(?<=assemblies)\d$|',
                        f'(?<=PLATE\u0020)\d$|',
                        f'(?<=PLATE)\d$|',
                        f'(?<=Covers\u0020)\d$|',
                        f'(?<=Covers)\d$|',
                        f'(?<=components)\(\d\)$|',
                        f'(?<=components\u0020)\(\d\)$|',
                        f'(?<=components\u0020)\d$|',
                        f'(?<=components)\d$|',
                        f'^\W{1,}|\W{1,}$']

            for bl in bad_list:
                module_name = re.sub(f'{bl}', '', module_name, flags=re.IGNORECASE).strip()

            module_name = re.sub(f'\u0020{2,}', '\u0020', module_name).strip()
            module_name = re.sub(f'^\W{1,}|\W{1,}$', '', module_name).strip()
            module_name = re.sub(f'^\W{1,}|\W{1,}$', '', module_name).strip()

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

        # добавляем в справочник наименование детали
        if d[2] and str(d[2]) != 'nan':
            pc_name = re.sub(f'^\W{1,}|\W{1,}$', '', d[2]).strip()
            if pc_name:
                pn_id = get_id('pn', pc_name)
                if pn_id < 1:
                    pn_id = parts_db_utils.insert_dict_details(pc_name)
                    parts_data.append({
                        'id': pn_id,
                        'pn': pc_name
                    })

        # добавляем картинку модуля
        if d[4] and str(d[4]) != 'nan':
            if old_img != d[4]:
                img_id = parts_db_utils.insert_dict_module_image(d[4])
                parts_db_utils.link_model_module_image(model_id, module_id, img_id)
                old_img = d[4]

        # добавляем в partcodes новый парткод
        if d[1] and str(d[1]) != 'nan':
            if isinstance(d[1], float):
                d1 = str(int(d[1]))
            else:
                d1 = str(d[1])
            pc_code = re.sub(f'^\W{1,}|\W{1,}$', '', d1).strip()
            if pc_code:
                pc_id = get_id('pc', pc_code)
                if pc_id < 1:
                    pc_id = parts_db_utils.insert_partcodes(pc_code, d[3], pn_id, brand_id)
                    parts_data.append({
                        'id': pc_id,
                        'pc': pc_code
                    })
            elif pn_id:
                article_code = gac.generate_article_partcode()
                pc_id = parts_db_utils.insert_partcodes_article(article_code, d[3], pn_id, brand_id)
        elif pn_id:
            article_code = gac.generate_article_partcode()
            pc_id = parts_db_utils.insert_partcodes_article(article_code, d[3], pn_id, brand_id)

        # линкуем парткод-модель-модуль
        if pc_id and pn_id:
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
