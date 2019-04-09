import math
import numpy as np


def dict_filtering(dict_val, filter_val='S5C'):
    filtered_dict = {}
    for key, value in dict_val.items():
        key_dict = key.replace(filter_val + "_", '')
        value_dict = value[0].replace(filter_val + ":", '')
        if key.startswith(filter_val) and len(value_dict) > 0:
            filtered_dict[int(key_dict)] = value_dict
    return filtered_dict


def get_overall_names(dict_val, count=5, score_field_name='Q2_OVERALL_1'):
    overall_names = {}
    for index in range(count):
        key = "%s_%s" % (score_field_name, index + 1)
        overall_names[index + 1] = dict_val[key][0].replace(score_field_name+':', '')
    return overall_names


def round_of_rating(number):
    return round(number * 2) / 2


def get_records(user_data_dict, three_brands=(), permanent_fields=(), weight=[20, 20, 20, 20, 20]):
    def get_overall_id(brand_id=0, overall_id=0):
        return "Q2_OVERALL_%s_%s" % (brand_id, overall_id)

    def get_text_key(brand_id):
        return ["Q3_%s" % int(brand_id), "Q4_%s" % int(brand_id)]

    result_data = {}
    for user_item in user_data_dict:
        for tag in three_brands:
            item = {}
            score_list = []

            if not math.isnan(float(user_item[tag])):
                text_keys = get_text_key(user_item[tag])

                for fields in permanent_fields:
                    item[fields] = user_item[fields]
                    item['overall'] = {}

                item['text_pros'] = user_item[text_keys[0]]
                item['text_cons'] = user_item[text_keys[1]]

                for inx in range(1, 6):
                    overall_field_name = get_overall_id(int(user_item[tag]), inx)
                    value_list = user_item[overall_field_name].split(' - ')
                    item['overall'][inx] = {'value': value_list[0], 'textual': value_list[1]}
                    score_list.append(int(value_list[0]))

                item['overall']['overall_weights'] = weight
                item['overall']['overall_list'] = score_list
                item['overall']['overall_average'] = np.average(score_list)
                item['overall']['overall_average_weight'] = np.average(score_list, weights=weight)
                item['overall']['overall_average_score'] = round_of_rating(item['overall']['overall_average'])

                result_data.setdefault(int(user_item[tag]), []).append(item)
    return result_data


def get_avg_score(records_collection_list, brands_filtered):
    per_product_avg_rating = {}
    for key, value in records_collection_list.items():
        per_product_avg_row = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        list_length = len(value)

        for item in value:
            for idx in range(1, 6):
                per_product_avg_row[idx] += int(item['overall'][idx]['value'])
        for x, y in per_product_avg_row.items():
            per_product_avg_row[x] = round((y / list_length) * 2, 1)

        per_product_avg_rating[key] = per_product_avg_row

        per_product_avg_rating[key]['val_list'] = list(per_product_avg_row.values())
        per_product_avg_rating[key]['rev_length'] = list_length
        per_product_avg_rating[key]['avg_score'] = round(np.average(per_product_avg_rating[key]['val_list']), 1)
        per_product_avg_rating[key]['brand_name'] = brands_filtered[key]

    return per_product_avg_rating
