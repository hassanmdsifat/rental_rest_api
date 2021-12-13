from datetime import datetime


def convert_str_to_date(value, output_format='%Y-%m-%d'):
    return datetime.strptime(value, output_format)