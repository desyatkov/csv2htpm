from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup as bs
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

def generate_html(records_collection_list, brands_filtered):
    os.makedirs("result", exist_ok=True)
    this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')

    j2_env = Environment(
        loader=FileSystemLoader(this_dir),
        trim_blocks=True
    )

    def length_str(pros, cons, num):
        pros_str = str(pros)
        cons_str = str(cons)
        return len(pros_str.strip() + cons_str.strip()) > num

    def length_str_val(pros, cons):
        pros_str = str(pros)
        cons_str = str(cons)
        return '%s --- %s' % (len(pros_str.strip() + cons_str.strip()), len(pros_str.strip() + cons_str.strip()) > 140)

    def replace_dot_lodash(value):
        if not isinstance(value, str):
            value = str(value)

        return value.strip().replace('.', '-')

    j2_env.filters['length_str'] = length_str
    j2_env.filters['replace_dot_lodash'] = replace_dot_lodash
    j2_env.filters['length_str_val'] = length_str_val

    for record_key, record_val in records_collection_list.items():
        brands_name = brands_filtered[record_key]

        sorted_records = sorted(record_val, key=lambda k: max(len(str(k['text_cons'])), len(str(k['text_pros']))), reverse=True)

        output_from_parsed_template = j2_env.get_template('rows_list.html').render(parent_dict=sorted_records)

        soup = bs(output_from_parsed_template, 'html.parser')
        pretty_html = soup.prettify()

        with open(os.path.join(result_dir, "%s.html" % brands_name), "w") as fh:
            fh.write(pretty_html)

    print(records_collection_list[86][0]['text_cons'])
    print(records_collection_list[86][0]['text_pros'])


def generate_html2(records_collection_list):
    os.makedirs("result", exist_ok=True)
    this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')

    j2_env = Environment(
        loader=FileSystemLoader(this_dir),
        trim_blocks=True
    )

    temp_dict = []

    for record_key, record_val in records_collection_list.items():
        temp_dict = temp_dict + record_val

    output_from_parsed_template = j2_env.get_template('review_list2.html').render(parent_dict=temp_dict)

    with open(os.path.join(result_dir, "example.html"), "w") as fh:
        fh.write(output_from_parsed_template)
