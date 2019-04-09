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

    for record_key, record_val in records_collection_list.items():
        brands_name = brands_filtered[record_key]
        output_from_parsed_template = j2_env.get_template('review_list.html').render(parent_dict=record_val)

        soup = bs(output_from_parsed_template, 'html.parser')
        pretty_html = soup.prettify()

        with open(os.path.join(result_dir, "%s.html" % brands_name), "w") as fh:
            fh.write(pretty_html)
