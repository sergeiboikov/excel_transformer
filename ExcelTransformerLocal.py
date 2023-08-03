import os.path
import sys
import yaml
import pandas as pd
from transformer import *


def _check_settings(config: dict, file_basename: str) -> bool:
    """
    Check that config file is correct

    :param config: Dictionary from YAML config
    :type config: object
    :param file_basename: Basename of file for validation
    :type file_basename: str
    :return: result of checking config file
    :rtype: bool
    """

    print("Get config file validation.")
    if 'filename' in config and config.get('filename') == file_basename:
        result = True
    else:
        print("Wrong 'filename' value in YAML config.")
        result = False

    if 'transforms' in config:
        result = True
    else:
        result = False

    return result


def set_settings(config: str, file_basename: str) -> dict:

    settings = {}

    print("Get transforms config " + config)
    try:
        stream = open(config, 'r')
    except IOError as e:
        print(e)
        exit(1)
    config = yaml.safe_load(stream)
    is_config_valid = _check_settings(config, file_basename)

    if not is_config_valid:
        raise Exception(f'Incorrect config for file: {file_basename}')

    # Make sure that the yaml file follows the rules
    settings['filename'] = config.get('filename')
    settings['sheet'] = config.get('sheet')
    settings['transforms'] = config.get('transforms')

    return settings


def _transform_df(df, transform_type, errors):
    transforms_class_map = {
        'DeleteDuplicatesByKeys': DeleteDuplicatesTransformer.DeleteDuplicatesTransformer
    }
    transform_name = list(transform_type.keys())[0]
    transform_data = list(transform_type.values())[0]
    transformer = transforms_class_map[transform_name](transform_data)
    result = transformer.transform(df)
    print(f'transform_name={transform_name}')
    print(f'transform_data={transform_data}')
    print(f'transformer={transformer}')
    print(f'result={result}')


def transform(settings: dict, excel_file: str, sheet_name: str, target_dir: str):

    errors = []

    print("Transform Excel Sheet " + sheet_name)
    excel_data = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(excel_data)
    for transform_type in settings['transforms']:
        _transform_df(excel_data, transform_type, errors)


if __name__ == '__main__':
    config = r'D:\GIT\PYTHON\excel_transformer\example\TSS_form.yml'
    xlsx_file = r'D:\GIT\PYTHON\excel_transformer\example\TSS_form.xlsx'
    target_dir = r'D:\GIT\PYTHON\excel_transformer\example'

    file_basename = os.path.basename(xlsx_file)
    settings = set_settings(config, file_basename)

    print(settings)
    file_basename = settings['filename']
    sheet_name = settings['sheet']

    try:
        results = transform(settings, xlsx_file, sheet_name, target_dir)
    except Exception as e:
        print(f'Error occured: {str(e)}')
