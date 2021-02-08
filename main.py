from datetime import datetime
import file_utils as fu
import parser_utils as pu
import re


def main():
    # data = fu.load_parsed_models('db_file_list.csv', 'utf-8')
    # brands = ['Brother', 'Canon', 'Duplo', 'Epson', 'HP', 'OKI', 'Lexmark', 'Mimaki', 'Kyocera', 'Konica-Minolta',
    #           'KIP', 'Konica', 'MB', 'Minolta', 'Mutoh', 'Panasonic', 'Pantum', 'Ricoh', 'Riso', 'Roland', 'Samsung',
    #           'Sanyo', 'Sharp', 'Toshiba', 'Xerox', 'Zebra']
    # # commit
    # pu.insert_brands(brands)
    # pu.insert_models(data)
    # pu.data_analysis(data)
    l = 'ADF & DOCUMENT COVERS -'
    bad_list = [f'\(\d\u0020of\u0020\d\)|',
                f'\d\u0020of\u0020\d|',
                f'\(\dof\d\)|',
                f'(?<=Base\u0020)\d$',
                f'(?<=Base)\d$',
                f'(?<=Electrical\u0020)\d$',
                f'(?<=Electrical)\d$',
                f'(?<=ARDF\u0020)\d$',
                f'(?<=ARDF)\d$',
                f'(?<=components\u0020)\d$|',
                f'(?<=ADF\u0020)\d$|',
                f'(?<=ADF)\d$|',
                f'(?<=PANEL\u0020)\d$|',
                f'(?<=PANEL)\d$|',
                f'\d/\d$|',
                f'\W$|',
                f'\(\d/\d\)|',
                f'\(\d\u0020/\u0020\d\)|',
                f'(?<=sheet tray insert\u0020)\d$|',
                f'(?<=sheet tray insert)\d$|',
                f'(?<=maker\u0020)\d$|',
                f'(?<=maker)\d$|',
                f'(?<=Folder\u0020)\d$|',
                f'(?<=Folder)\d$|',
                f'(?<=ADU\u0020)\d$|',
                f'(?<=ADU)\d$|',
                f'(?<=pick\u0020)\d$|',
                f'(?<=pick)\d$|',
                f'(?<=CASSETTE\u0020)\d$|',
                f'(?<=CASSETTE)\d$|',
                f'(?<=SECTION\u0020)\(\d\)$|',
                f'(?<=SECTION)\(\d\)$|',
                f'(?<=Assembly\u0020)\(\d\)$|',
                f'(?<=Assembly)\(\d\)$|',
                f'(?<=Assembly\u0020)\d$|',
                f'(?<=Assembly)\d$|',
                f'(?<=Area\u0020)\(\d\)$|',
                f'(?<=Area)\(\d\)$|',
                f'(?<=Area\u0020)\d$|',
                f'(?<=Area)\d$|',
                f'(?<=Option\u0020)\d$|',
                f'(?<=Option)\d$|',
                f'(?<=SECTION\u0020)\d$|',
                f'(?<=SECTION)\d$|',
                f'(?<=Carriage\u0020)\(\d\)$|',
                f'(?<=Carriage)\(\d\)$|',
                f'(?<=Carriage\u0020)\d$|',
                f'(?<=Carriage)\d$|',
                f'(?<=diagram\u0020)\d$|',
                f'(?<=diagram)\d$|',
                f'(?<=Paper pick\u0020)\d$|',
                f'(?<=Paper pick)\d$|',
                f'(?<=Tray\u0020)\d$|',
                f'(?<=Tray)\d$|',
                f'(?<=HARDWARE\u0020)\d$|',
                f'(?<=HARDWARE)\d$|',
                f'(?<=ETC\.\u0020)\d$|',
                f'(?<=ETC\.)\d$|',
                f'(?<=DOOR ASSEMBLY\u0020)\d$|',
                f'(?<=DOOR ASSEMBLY)\d$|',
                f'(?<=ASSEMBLY, RIGHT\u0020)\d$|',
                f'(?<=ASSEMBLY, RIGHT)\d$|',
                f'(?<=Feed\u0020)\(\d\)$|',
                f'(?<=Feed)\(\d\)$|',
                f'(?<=unit\u0020)\(\d\)$|',
                f'(?<=unit)\(\d\)$|',
                f'(?<=unit\u0020)\d$|',
                f'(?<=unit)\d$|',
                f'(?<=Feed\u0020)\d$|',
                f'(?<=Feed)\d$|',
                f'(?<=LABELS\u0020)\d$|',
                f'(?<=LABELS)\d$|',
                f'(?<=Frame\u0020)\d$|',
                f'(?<=Frame)\d$|',
                f'(?<=CASSETTE\u0020)\(\d\)$|',
                f'(?<=CASSETTE)\(\d\)$|',
                f'\(\u0020\d\u0020/\u0020\d\u0020\)$|',
                f'\(\d\)$|',
                f'\(\u0020\d\u0020\)$|',
                f'(?<=insert\u0020)\d$|',
                f'(?<=insert)\d$|',
                f'(?<=ASSY\u0020)\d$|',
                f'(?<=ASSY)\d$|',
                f'(?<=ASSEMBLY\u0020)\d$|',
                f'(?<=ASSEMBLY)\d$|',
                f'(?<=ASSEMBLY\u0020)\(\d\)$|',
                f'(?<=ASSEMBLY)\(\d\)$|',
                f'(?<=sensors\u0020)\d$|',
                f'(?<=sensors)\d$|',
                f'(?<=\(Registration Section\))\d$|',
                f'(?<=assemblies\u0020)\d$|',
                f'(?<=assemblies)\d$|',
                f'(?<=PLATE\u0020)\d$|',
                f'(?<=PLATE)\d$|',
                f'(?<=Covers\u0020)\d$|',
                f'(?<=Covers)\d$|',
                f'(?<=components)\(\d\)$|',
                f'(?<=components\u0020)\(\d\)$|',
                f'(?<=components\u0020)\d$|',
                f'(?<=components)\d$']
    for bl in bad_list:
        l = re.sub(f'{bl}', '', l, flags=re.IGNORECASE).strip()

    l = re.sub(f'[\u0020]\W', '', l).strip()
    l = re.sub(f'\u0020{2,}', '\u0020', l).strip()

    print(l)


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    main()
    print(datetime.now() - start_time)
