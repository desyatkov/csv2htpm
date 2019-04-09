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

