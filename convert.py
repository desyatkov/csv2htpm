#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
import utils
import pprint
import math

BRAND_PREFIX_FIELD = 'S5C'
SCORE_VALUES_NAME = 'Q2_OVERALL_1'


# GET FILE WITH FIELDS DATA(brands, score values)
df_brands = pd.read_csv('csvFiles/fields-real.csv', delimiter=',', index_col=0, usecols=['Variable Name', 'Label'])
brands_records = df_brands.to_dict('split')
brands_split = dict(zip(brands_records['index'], brands_records['data']))

brands_filtered = utils.dict_filtering(brands_split, filter_val=BRAND_PREFIX_FIELD)
overall_fields_name = utils.get_overall_names(brands_split, score_field_name=SCORE_VALUES_NAME)

# GET USER DATA

# __USER RELATES 3 BRANDS
result_data = {}
BRAND_3_TAGS = ('BRAND_1_TAG', 'BRAND_2_TAG', 'BRAND_3_TAG')

# __OVERALL 5 values
def get_overall_id(brand_id=0, overall_id=0):
    return "Q2_OVERALL_%s_%s" % (brand_id, overall_id)

# __USER PERMANENT FIELDS


PERMANENT_FIELDS = ("ResponseId", "Gender", "Age", "FIRST_NAME", "COUNTY", "AGE_TAG", "Regions")
user_data = pd.read_csv('csvFiles/data.csv', delimiter=',')
user_data_dict = user_data.to_dict('records')
user_data.info(memory_usage='deep')

pp = pprint.PrettyPrinter(indent=4)

for user_item in user_data_dict:                # row__review
    for tag in BRAND_3_TAGS:                    # brand
        item = {}
        overall = {}
        for fields in PERMANENT_FIELDS:         # fields
            item[fields] = user_item[fields]
            item['overall'] = {}

        if not math.isnan(float(user_item[tag])):
            for inx in range(1, 6):
                overall_field_name = get_overall_id(int(user_item[tag]), inx)
                value_list = user_item[overall_field_name].split(' - ')
                item['overall'][inx] = {'value': value_list[0], 'textual': value_list[1]}

            result_data.setdefault(int(user_item[tag]), []).append(item)

# print(tag, user_item[tag])
pp.pprint(result_data)
