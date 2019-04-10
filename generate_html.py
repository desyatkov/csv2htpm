from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup as bs
import os


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

    def replace_dot_lodash(value):
        if not isinstance(value, str):
            value = str(value)

        return value.strip().replace('.', '-')

    j2_env.filters['length_str'] = length_str
    j2_env.filters['replace_dot_lodash'] = replace_dot_lodash

    for record_key, record_val in records_collection_list.items():
        brands_name = brands_filtered[record_key]
        output_from_parsed_template = j2_env.get_template('rows_list.html').render(parent_dict=record_val)

        soup = bs(output_from_parsed_template, 'html.parser')
        pretty_html = soup.prettify()

        with open(os.path.join(result_dir, "%s.html" % brands_name), "w") as fh:
            fh.write(pretty_html)


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
