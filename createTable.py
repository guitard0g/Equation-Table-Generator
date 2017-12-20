import argparse
from collections import defaultdict

def get_table_header(id, type):
    # header format
    # Query Equation <id> | Rank | Eq ID | Top Equations <type> | Value | Rank | Top Words <type >

    header = "<table><tr><td>Query Equation "
    header += (id + "</td><td>Rank</td><td>Eq ID</td><td>Top Equations ")
    header += (type + "</td><td>Value</td><td>Rank</td><td>Top Words ")
    header += (type + "</td></tr>")

    return header

def get_table_row(result, dict):
    result_html = '<tr><td class="tex"><span>{0}</span><img class="{1}" style="display:none;" alt="{0}" onError="this.onerror=null;"/></td><td>{2}</td><td>{3}</td><td class="tex"><span>{4}</span><img class="{5}" style="display:none;" alt="{4}" onError="this.onerror=null;"/></td><td>{6}</td><td>{7}</td><td>{8}</td></tr>'
    # {4} in span, {5} in img
    return result_html.format(dict[result[1]], result[1], result[3], result[4], dict[result[4]], result[4], result[6], result[7], result[8])
    # "http://www.columbia.edu/~kk3161/"+result[1]+".png"

def get_table(data, dict):
    table_data = ""
    for item in data:
        table_data += get_table_row(item, dict)
    return table_data

def close_table():
    return "</table>"

def main():
    parser = argparse.ArgumentParser(description='Usage for creating an equation table.')
    parser.add_argument("anno_file",help="Name of annotation file")
    # parser.add_argument("query_eqs",help="Path to query equation tsv file")
    parser.add_argument("display_eqs",help="Path to display equation tsv file")
    args = parser.parse_args()
    anno_file = open(args.anno_file)
    query_eqs_file = open(args.query_eqs)
    display_eqs_file = open(args.display_eqs)
    # anno_file = open('results_small.anno')
    # query_eqs_file = open('queryEquations.tsv')
    # display_eqs_file = open('display_eq.tsv', encoding='latin-1')
    html_file = open('table.html',mode="w", encoding='utf-8')
    head_file = open('head.html',mode="r", encoding='utf-8')
    html_file.write(head_file.read())
    html_file.close()
    html_file = open('table.html',mode="a", encoding='utf-8')

    equation_tex = defaultdict(str)
    l = display_eqs_file.readline()
    while l:
        item = l.split('\t')
        equation_tex[item[0].lower()] = item[1]
        l = display_eqs_file.readline()

    l = anno_file.readline()
    html = ''
    while l:
        item = l.split('\t')
        type_list = []
        current_type = item[0]
        current_eq = item[1]
        while item[0] == current_type and item[1] == current_eq:
            type_list.append(item)
            l = anno_file.readline()
            item = l.split('\t')
        # html += get_table_header(current_eq, current_type)
        # html += get_table(type_list, equation_tex)
        # html += close_table()
        html_file.write(get_table_header(current_eq, current_type))
        html_file.write(get_table(type_list, equation_tex))
        html_file.write(close_table())

    tail_file = open('tail.html',mode="r", encoding='utf-8')
    html_file.write(tail_file.read())
    html_file.close()



    # Table format
    # Query Equation <id> | Rank | Eq ID | Top Equations <type> | Value | Rank | Top Words <type >
    # query equation tex/image | result equation rank | result tex/image | euclid dist | word rank | word


if __name__ == "__main__":
    main()