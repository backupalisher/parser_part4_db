import asyncio
import concurrent.futures

from db import db_utils
import global_data as gd
from erc import erc_parser
from spec import spec_parser, spec_db_utils as sdbu
from parts import parts_utils
import file_utils as fu
from datetime import datetime
from main import logger


def insert_brands(data):
    for d in data:
        db_utils.insert_brand(d)
        # print(d)


def insert_models(data):
    old_brand = ''
    brand_id = 0
    print('Analyze models...')
    for models in data:
        brand = models[0]
        model = models[1]
        # print(model)
        if brand != old_brand:
            brand_id = sdbu.get_id('brands', 'name', brand)[0][0]
            old_brand = brand

        # добавляем model в таблицу models
        model_id = db_utils.insert_model(model, brand_id)

        gd.g_data.append({
            brand: brand_id,
            model: model_id,
        })


def data_analysis(data):
    old_brand = ''
    parsed_models = fu.load_parsed_models('parsed_models.csv', 'utf-8')
    for d in data:
        brand_id = 0
        brand = d[0]
        model = d[1]
        parsed_bool = False
        # print()

        for pm in parsed_models:
            if model == pm[0]:
                parsed_bool = True
                print(model, '-', 'PARSED')
                break

        if parsed_bool:
            continue

        print(model, datetime.now().strftime("%X"))
        # logger.info(f'{model}, {datetime.now().strftime("%X")}')
        model_id = 0
        for key in gd.g_data:
            if model in key.keys():
                brand_id = key[brand]
                model_id = key[model]
                break

        # if brand != old_brand:
        #     gd.erc_data = []
        #     gd.parts_data = []
        #     gd.detail_options_data = []
        #     gd.spr_details_options_data = []
        #     old_brand = brand

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=5))

        result_loop = loop.run_until_complete(init_start(brand_id, model_id, d))
        if result_loop:
            pass
        loop.close()

        fu.save_parsed_models('parsed_models.csv', 'utf-8', model)


async def init_start(brand_id, model_id, d):
    async_tasks = []

    if d[2]:
        async_tasks.append(spec_init(model_id, d[2]))
    if d[3]:
        async_tasks.append(error_init(model_id, d[3]))
    if d[4]:
        async_tasks.append(parts_init(brand_id, model_id, d[4]))
    return await asyncio.gather(*async_tasks)


async def spec_init(model_id, data):
    await spec_parser.insert_options(model_id, data)


async def error_init(model_id, data):
    await erc_parser.insert_erc(model_id, data)


async def parts_init(brand_id, model_id, data):
    await parts_utils.insert_parts(brand_id, model_id, data)