import argparse
import os
from collections import defaultdict


def read_arguments():
    arguments = argparse.ArgumentParser(description='Word Embeddings Using TensorFlow and Edward.')

    arguments.add_argument('--version', action='version', version='%(prog)s 1.0')

    arguments.add_argument('-display_eqs', default="/Users/kriste/work/4col/combined_4col_new.tsv"
                           , type=str, help='Adagrad initial learning rate.')

    arguments.add_argument('-anno_file', default="/Users/kriste/work/4col/nlp_pos/results/nlp/mw/sgd.fl_wi5_ei5.all.anno"
                           , type=str, help='Embedding vectors dimensions.')

    arguments.add_argument('-eq', default="Cos(alpha,alpha)"
                           , type=str, help='Equation ranking type.')

    arguments.add_argument('-word', default="Cos(alpha,rho)"
                           , type=str, help='Word ranking type.')

    arguments = arguments.parse_args()
    return arguments

def get_table_header(id, eq_type, word_type):
    # header format
    # Query Equation <id> | Rank | Eq ID | Top Equations <type> | Value | Rank | Top Words <type >

    header = "<table><tr><td>Query Equation "
    header += (id + "</td><td>Rank</td><td>Eq ID</td><td>Top Equations ")
    header += (eq_type + "</td><td>Value</td><td>Rank</td><td>Top Words ")
    header += (word_type + "</td></tr>")

    return header

def get_table_row(result, dict):
    result_html = '<tr><td class="tex"><span>{0}</span><img class="{1}" alt="{0}" onError="this.onerror=null;"/></td><td>{2}</td><td>{3}</td><td class="tex"><span>{4}</span><img class="{5}" alt="{4}" onError="this.onerror=null;"/></td><td>{6}</td><td>{7}</td><td>{8}</td></tr>'
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

def main(args):

    anno_file = open(args.anno_file)
    display_eqs_file = open(args.display_eqs)
    python_path = os.path.dirname(os.path.realpath(__file__))

    html_file = open(args.anno_file+".html",mode="w", encoding='utf-8')
    head_file = open(os.path.join(python_path,'head.html'),mode="r", encoding='utf-8')
    html_file.write(head_file.read())
    html_file.close()
    html_file = open(args.anno_file+".html",mode="a", encoding='utf-8')

    equation_tex = defaultdict(str)
    l = display_eqs_file.readline()
    while l:
        item = l.split('\t')
        equation_tex[item[0].lower()] = item[1]
        l = display_eqs_file.readline()

    l = anno_file.readline()
    html = ''
    current_eq_type = args.eq
    current_word_type = args.word
    eq_type_list = []
    word_type_list = []
    while l:
        # Eu(alpha,rho)	eqds58184q	---	1	eqds626q	---	1.2649	1	afraid	0909.4385 1412.7091 1412.7091
        item = l.strip().split('\t')
        type_list = []
        current_type = item[0]
        current_eq = item[1]
        while item[0] == current_type and item[1] == current_eq:
            if current_type ==current_eq_type:
                eq_info = item[0]+"\t"+item[1]+"\t"+item[2]+"\t"+item[3]+"\t"+item[4]+"\t"+item[5]+"\t"+item[6]
                eq_type_list.append(eq_info)
            if current_type == current_word_type:
                word_info = item[7] + "\t" + item[8] + "\t" + item[9]
                word_type_list.append(word_info)
            type_list.append(item)
            l = anno_file.readline()
            item = l.strip().split('\t')
        print("***"+l.strip()+"***"+str(len(item)))
        if (len(item)<2):
            continue
        if (item[1]!=current_eq) or ( (len(eq_type_list)!=0) and (len(word_type_list)!=0)):
            # html += get_table_header(current_eq, current_type)
            # html += get_table(type_list, equation_tex)
            # html += close_table()
            joined_list = []
            for i in range (0,len(eq_type_list)):
                join_lists = eq_type_list[i]+"\t"+word_type_list[i]
                item2 = join_lists.split("\t")
                joined_list.append(item2)
            html_file.write(get_table_header(current_eq, current_eq_type,current_word_type))
            html_file.write(get_table(joined_list, equation_tex))
            html_file.write(close_table())
            eq_type_list = []
            word_type_list = []

    tail_file = open('tail.html',mode="r", encoding='utf-8')
    html_file.write(tail_file.read())
    html_file.close()



    # Table format
    # Query Equation <id> | Rank | Eq ID | Top Equations <type> | Value | Rank | Top Words <type >
    # query equation tex/image | result equation rank | result tex/image | euclid dist | word rank | word


if __name__ == '__main__':
    arguments = read_arguments()
    main(arguments)