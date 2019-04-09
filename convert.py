#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
import utils
import pprint
import numpy as np

BRAND_PREFIX_FIELD = 'S5C'
SCORE_VALUES_NAME = 'Q2_OVERALL_1'

# GET FILE WITH FIELDS DATA(brands, score values)
df_brands = pd.read_csv('csvFiles/fields-real.csv', delimiter=',', index_col=0, usecols=['Variable Name', 'Label'])
brands_records = df_brands.to_dict('split')
brands_split = dict(zip(brands_records['index'], brands_records['data']))

brands_filtered = utils.dict_filtering(brands_split, filter_val=BRAND_PREFIX_FIELD)
overall_fields_name = utils.get_overall_names(brands_split, score_field_name=SCORE_VALUES_NAME)

# GET USER DATA
user_data = pd.read_csv('csvFiles/data-real.csv', delimiter=',')
user_data_dict = user_data.to_dict('records')
user_data.info(memory_usage='deep')

SCORE_WEIGHTS = [10, 10, 20, 20, 40]
BRAND_3_TAGS = ('BRAND_1_TAG', 'BRAND_2_TAG', 'BRAND_3_TAG')
PERMANENT_FIELDS = ("ResponseId", "Gender", "Age", "FIRST_NAME", "COUNTY", "AGE_TAG", "Regions")

# COLLECTED DATA
records_collection_list = utils.get_records(user_data_dict, BRAND_3_TAGS, PERMANENT_FIELDS, SCORE_WEIGHTS)

pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(records_collection_list)


rating_default = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

per_product_avg_rating = utils.get_avg_score(records_collection_list)


pp.pprint(records_collection_list)
# pp.pprint(per_product_avg_rating)
