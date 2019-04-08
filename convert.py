#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
import pprint
import utils

BRAND_PREFIX_FIELD = 'S5C'
SCORE_VALUES_NAME = 'Q2_OVERALL_1'

# df = pd.read_csv('csvFiles/data.csv', delimiter=',')
# records = df.to_dict('records')

# GET FILE WITH FIELDS DATA(brands, score values)
df_brands = pd.read_csv('csvFiles/fields.csv', delimiter=',', index_col=0, usecols=['Variable Name', 'Label'])
brands_records = df_brands.to_dict('split')
brands_split = dict(zip(brands_records['index'], brands_records['data']))

brands_split_filtered = utils.dict_filtering(brands_split, filter_val=BRAND_PREFIX_FIELD)
overall_fields_name = utils.get_overall_names(brands_split, score_field_name=SCORE_VALUES_NAME)
