from datetime import datetime
import file_utils as fu
import parser_utils as pu


def main():
    data = fu.load_parsed_models('db_file_list.csv', 'utf-8')
    brands = ['Brother', 'Canon', 'Duplo', 'Epson', 'HP', 'OKI', 'Lexmark', 'Mimaki', 'Kyocera', 'Konica-Minolta',
              'KIP', 'Konica', 'MB', 'Minolta', 'Mutoh', 'Panasonic', 'Pantum', 'Ricoh', 'Riso', 'Roland', 'Samsung',
              'Sanyo', 'Sharp', 'Toshiba', 'Xerox', 'Zebra']
    # # commit
    pu.insert_brands(brands)
    pu.insert_models(data)
    pu.data_analysis(data)


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    main()
    print(datetime.now() - start_time)
