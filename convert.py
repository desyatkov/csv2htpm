#!/usr/bin/python

import pandas as pd
import utils
import pprint
from generate_html import generate_html

BRAND_PREFIX_FIELD = 'S5C'
SCORE_VALUES_NAME = 'Q2_OVERALL_1'

# GET FILE WITH FIELDS DATA(brands, score values)
df_brands = pd.read_csv('csvFiles/fields-real.csv', delimiter=',', index_col=0, usecols=['Variable Name', 'Label'])
brands_records = df_brands.to_dict('split')
brands_split = dict(zip(brands_records['index'], brands_records['data']))

# brand code and name ex: {1: 888 ...}
brands_filtered = utils.dict_filtering(brands_split, filter_val=BRAND_PREFIX_FIELD)

# Score id and name ex: {   1: 'Ease of Use' ...}
overall_fields_name = utils.get_overall_names(brands_split, score_field_name=SCORE_VALUES_NAME)

# GET USER DATA
user_data = pd.read_csv('csvFiles/data-real.csv', delimiter=',')
user_data_dict = user_data.to_dict('records')
user_data.info(memory_usage='deep')

SCORE_WEIGHTS = [20, 20, 20, 20, 20]
BRAND_3_TAGS = ('BRAND_1_TAG', 'BRAND_2_TAG', 'BRAND_3_TAG')
PERMANENT_FIELDS = ("ResponseId", "Gender", "Age", "FIRST_NAME", "COUNTY", "AGE_TAG", "Regions")

# COLLECTED DATA
records_collection_list = utils.get_records(user_data_dict, BRAND_3_TAGS, PERMANENT_FIELDS, SCORE_WEIGHTS)

# Each brand avg score
avg_rating_per_brand = utils.get_avg_score(records_collection_list, brands_filtered)

pp = pprint.PrettyPrinter(indent=4)
# print(records_collection_list.keys())
# pp.pprint(records_collection_list[86])
# pp.pprint({inx: overall_fields_name[inx] for inx in range(1, 6)})

df = pd.DataFrame(avg_rating_per_brand)\
    .drop(index='val_list')\
    .rename(index={inx: overall_fields_name[inx] for inx in range(1, 6)})

df_transposed = df.T

export_csv = df_transposed.to_csv(r'export_dataframe.csv', header=True, index=True)

print(df_transposed)

generate_html(records_collection_list, brands_filtered)

