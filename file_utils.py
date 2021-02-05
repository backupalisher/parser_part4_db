import csv
import os
import pandas


def load_parsed_models(file_name, code):
    try:
        parsed_models_list = pandas.read_csv(file_name, encoding=code, sep=';', header=None)
        parsed_models_list = parsed_models_list.values.tolist()
    except:
        parsed_models_list = []
    return parsed_models_list


def save_parsed_models(file_name, code, model):
    df = pandas.DataFrame([model])
    df.to_csv(file_name, encoding=code, index=False, mode='a', header=False, sep=";")
