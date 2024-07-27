import re
import random

# Updated mapping dictionary with common digraphs
cyrrilization_mapping_extended = {
    'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е',
    'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'дж',
    'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
    'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
    'u': 'у', 'v': 'в', 'w': 'в', 'x': 'икс', 'y': 'ы',
    'z': 'з',
    # Common digraphs
    'sh': 'ш', 'ch': 'ч', 'th': 'з', 'ph': 'ф', 'oo': 'у', 'ee': 'и', 'kh': 'х',
    # common trigraphs
    'sch': 'ск'
    # Capital letters are also converted to lowercase in the cyrrilization
}
for key, value in list(cyrrilization_mapping_extended.items()):
    cyrrilization_mapping_extended[key.upper()] = value.upper()


# Russian letter to its phonetic pronunciation mapping
pronunciation_map = {
    'А': 'а', 'Б': 'бэ', 'В': 'вэ', 'Г': 'гэ', 'Д': 'дэ',
    'Е': 'е', 'Ё': 'ё', 'Ж': 'жэ', 'З': 'зэ', 'И': 'и',
    'Й': 'ий', 'К': 'ка', 'Л': 'эл', 'М': 'эм', 'Н': 'эн',
    'О': 'о', 'П': 'пэ', 'Р': 'эр', 'С': 'эс', 'Т': 'тэ',
    'У': 'у', 'Ф': 'эф', 'Х': 'ха', 'Ц': 'цэ', 'Ч': 'чэ',
    'Ш': 'ша', 'Щ': 'ща', 'Ъ': 'твёрдый знак', 'Ы': 'ы', 'Ь': 'мягкий знак',
    'Э': 'э', 'Ю': 'ю', 'Я': 'я'
}

# Function to expand abbreviations in the text
def expand_abbreviations(text):
    # Regex to find sequences of uppercase Cyrillic letters
    abbreviations = re.findall(r'\b[А-ЯЁ]{2,}\b', text)

    # Expand each abbreviation using the pronunciation map
    for abbr in abbreviations:
        # Create a pronounced form of the abbreviation
        pronounced_form = ' '.join(pronunciation_map[letter] for letter in abbr if letter in pronunciation_map)
        # Replace the abbreviation with its pronounced form
        text = text.replace(abbr, pronounced_form)

    return text


def normalize_abbreviations(text):
    abbreviations_type_0 = {
        'ред.': 'редакция',
        'стр.': 'страница',
        'изд.': 'издание',
        'обл.': 'область',
        'р-н': 'район',
        'гг.': 'годов'
    }

    abbreviations_type_1 = {
        'т.к.': 'так как',
        'т.е.': 'то есть',
        'т.д.': 'так далее',
        'т.п.': 'тому подобное',
        'т.о.': 'таким образом',
        'p.s.': 'постскриптум.',
        'р.s.': 'постскриптум.',
        'п.с.': 'постскриптум.',
        'п.c.': 'постскриптум.',
        'з.ы.': 'постскриптум.',
        'н.э.': 'нашей эры',
    }

    abbreviations_type_2 = {
        'респ': 'республика',
        'просп': 'проспект',
        'пр-кт': 'проспект',
        'пр-т': 'проспект',
        'пр': 'проспект',
        'пл': 'площадь',
        'ул': 'улица',
        'г': 'город',
    }

    abbreviations_type_3 = {
        'кв': 'квартира',
        'д': 'дом',
    }

    def modify_set_0(abbreviations_set):
        return [key.replace('.', r'\.') for key in abbreviations_set]

    def modify_set_1(abbreviations_set):
        sep = ' ?'
        return [sep.join(key).replace('.', r'\.') for key in abbreviations_set]

    abbreviations_pattern_type_0 = re.compile(fr'(?i)\b({"|".join(modify_set_0(abbreviations_type_0.keys()))})(?!\w)( \w)?')
    abbreviations_pattern_type_1 = re.compile(fr'(?i)\b({"|".join(modify_set_1(abbreviations_type_1.keys()))})(?!\w)( \w)?')
    abbreviations_pattern_type_2 = re.compile(fr'\b({"|".join(abbreviations_type_2.keys())})\.? ?(?=[А-Я])( \w)?')
    abbreviations_pattern_type_3 = re.compile(fr'(?i)\b({"|".join(abbreviations_type_3.keys())})\.? ?(?=\d)( \w)?')

    def get_replace(dictionary, suffix=''):
        def replace(match):
            abbreviation, next_letter = match.groups()
            abbreviation = abbreviation.lower().replace(' ', '')
            abbreviation = dictionary[abbreviation]
            if suffix:
                abbreviation += suffix
            if next_letter is not None:
                if next_letter.isupper() and not abbreviation.endswith('.'):
                    abbreviation += '.'
                abbreviation += next_letter
            return abbreviation
        return replace

    for _ in range(2):
        text = abbreviations_pattern_type_0.sub(get_replace(abbreviations_type_0), text)
        text = abbreviations_pattern_type_1.sub(get_replace(abbreviations_type_1), text)
        text = abbreviations_pattern_type_2.sub(get_replace(abbreviations_type_2, suffix=' '), text)
        text = abbreviations_pattern_type_3.sub(get_replace(abbreviations_type_3, suffix=' '), text)
    return text

# Функция для замены сокращений на полные формы
def normalize_physical_units(text):
    # Словарь с приставками и их полными формами
    values = {
        '%': ['процент', 'процента', 'процентов'],
        'кв метр': ['квадратный метр', 'квадратных метра', 'квадратных метров'],
        'кв метра': ['квадратный метр', 'квадратных метра', 'квадратных метров'],
        'кв метров': ['квадратный метр', 'квадратных метра', 'квадратных метров'],
        'м2': ['квадратный метр', 'квадратных метра', 'квадратных метров'],
        'м 2': ['квадратный метр', 'квадратных метра', 'квадратных метров'],
        'м3': ['кубический метр', 'кубических метра', 'кубических метров'],
        'м 3': ['кубический метр', 'кубических метра', 'кубических метров'],
        'м/с': ['метр в секунду', 'метра в секунду', 'метров в секунду'],
        'м с': ['метр в секунду', 'метра в секунду', 'метров в секунду'],
        'км/ч': ['километр в час', 'километра в час', 'километров в час'],
        'км ч': ['километр в час', 'километра в час', 'километров в час'],
        'м': ['метр', 'метра', 'метров'],
        'см': ['сантиметр', 'сантиметра', 'сантиметров'],
        'мм': ['миллиметр', 'миллиметра', 'миллиметров'],
        'км': ['километр', 'километра', 'километров'],
        'ч': ['час', 'часа', 'часов'],
        'г': ['грамм', 'грамма', 'грамм'],
        'мг': ['миллиграмм', 'миллиграмма', 'миллиграмм'],
        'кг': ['килограмм', 'килограмма', 'килограмм'],
        'т': ['тонна', 'тонны', 'тонн'],
        'кб': ['килобайт', 'килобайта', 'килобайт'],
        'мб': ['мегабайт', 'мегабайта', 'мегабайт'],
        'гб': ['гигабайт', 'гигабайта', 'гигабайт'],
        'тб': ['терабайт', 'терабайта', 'терабайт'],
        'гц': ['герц', 'герца', 'герцов'],
        'ггц': ['гигагерц', 'гигагерца', 'гигагерц'],
        'мгц': ['мегагерц', 'мегагерца', 'мегагерц'],
        'кгц': ['килогерц', 'килогерца', 'килогерц'],
        'вт': ['ватт', 'ватта', 'ватт'],
        'мвт': ['милливатт', 'милливатта', 'милливатт'],
        'квт': ['киловатт', 'киловатта', 'киловатт'],
        'гвт': ['гигаватт', 'гигаватта', 'гигаватт'],
        'ом': ['ом', 'ома', 'омов'],
        'ком': ['килоом', 'килоома', 'килоомов'],
        'гом': ['гигаом', 'гигаома', 'гигаомов'],
        'сек': ['секунда', 'секунды', 'секунд'],
        'с': ['секунда', 'секунды', 'секунд'],
        'мс': ['милисекунда', 'милисекунды', 'милисекунд'],
        'нс': ['наносекунда', 'наносекунды', 'наносекунд'],
        'пс': ['пикосекунда', 'пикосекунды', 'пикосекунд'],
        'мин': ['минута', 'минуты', 'минут'],
        'ч': ['час', 'часа', 'часов'],
        'мин': ['минута', 'минуты', 'минут'],
        'дж': ['джоуль', 'джоуля', 'джоулей'],
        'мдж': ['миллиджоуль', 'миллиджоуля', 'миллиджоулей'],
        'кдж': ['килоджоуль', 'килоджоуля', 'килоджоулей'],
        'гдж': ['гигаджоуль', 'гигаджоуля', 'гигаджоулей'],

        'ма': ['миллиампер', 'миллиампера', 'миллиампер'],
        'ф': ['фарад', 'фарада', 'фарад'],
        'мф': ['микрофарад', 'микрофарада', 'микрофарад'],
        'нф': ['нанофарад', 'нанофарада', 'нанофарад'],
        'па': ['паскаль', 'паскаля', 'паскалей'],
        'кпа': ['килопаскаль', 'килопаскаля', 'килопаскалей'],
        'мпа': ['мегапаскаль', 'мегапаскаля', 'мегапаскалей'],
        'гпа': ['гигапаскаль', 'гигапаскаля', 'гигапаскалей'],
        'бар': ['бар', 'бара', 'бар'],
        'мбар': ['миллибар', 'миллибара', 'миллибар'],
        'нбар': ['нанобар', 'нанобара', 'нанобар'],
        'тыс': ['тысяча', 'тысячи', 'тысяч'],
        'млн': ['миллион', 'миллиона', 'миллионов'],
        'млрд': ['миллиард', 'миллиарда', 'миллиардов'],
    }
    femine_units = {'т', 'мин', 'сек', 'с', 'мс', 'нс', 'пс', 'тыс'}

    def russian_plural(number):
        if number % 10 == 1 and number % 100 != 11:
            return 0
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return 1
        else:
            return 2

    # Регулярное выражение для поиска сокращений
    conntected_numbers_pattern = re.compile(fr'(?i)(\d+)( )?({"|".join(values.keys())})(\.)?(?!\w)( \w)?')

    # Функция для замены сокращений на полные формы
    def replace(match):
        num, is_space, unit, dot, next_letter = match.groups()
        is_femine = unit in femine_units
        num = int(num)
        key_unit = unit.lower()
        if key_unit in values:
            unit = values[key_unit][russian_plural(num)]
        num = number_to_words(num)
        if is_femine:
            num = regular_number_to_femine(num)
        text = f'{num} {unit}'
        if next_letter is not None:
            if dot is not None and next_letter.isupper():
                text += '.'
            text += next_letter
        return text

    for _ in range(2):
        text = conntected_numbers_pattern.sub(replace, text)
    return text


def cyrrilize(text):
    """Convert a given text from Latin script to an approximate Cyrillic script in lowercase,
    taking into account common digraphs."""
    cyrrilized_text = ""
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in cyrrilization_mapping_extended:
            # If a digraph is found, add its cyrrilization and increment by 2
            cyrrilized_text += cyrrilization_mapping_extended[text[i:i+2]]
            i += 2
        else:
            # Add the cyrrilization of a single character
            cyrrilized_text += cyrrilization_mapping_extended.get(text[i], text[i])
            i += 1
    return cyrrilized_text

def roman_to_int(s):
    """
    Конвертирует римское число в целое.
    :param s: строка, содержащая римское число.
    :return: целое число.
    """
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'Х': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    integer = 0
    for i in range(len(s)):
        if i > 0 and roman_numerals[s[i]] > roman_numerals[s[i - 1]]:
            integer += roman_numerals[s[i]] - 2 * roman_numerals[s[i - 1]]
        else:
            integer += roman_numerals[s[i]]
    return integer


def regular_number_to_femine(text: str):
    mapping = {
        'один': 'одна',
        'два': 'две',
    }
    words = text.split()
    if words[-1] not in mapping:
        return text
    words[-1] = mapping[words[-1]]
    return ' '.join(words)



def number_to_words(n):
    """
    Convert a number into its word components in Russian
    """
    if n == 0:
        return 'ноль'

    units = ['','один','два','три','четыре','пять','шесть','семь','восемь','девять']
    teens = ['десять','одиннадцать','двенадцать','тринадцать','четырнадцать','пятнадцать','шестнадцать','семнадцать','восемнадцать','девятнадцать']
    tens = ['','десять','двадцать','тридцать','сорок','пятьдесят','шестьдесят','семьдесят','восемьдесят','девяносто']
    hundreds = ['','сто','двести','триста','четыреста','пятьсот','шестьсот','семьсот','восемьсот','девятьсот']
    
    thousand_units = ['тысяча', 'тысячи', 'тысяч']
    million_units = ['миллион', 'миллиона', 'миллионов']
    billion_units = ['миллиард', 'миллиарда', 'миллиардов']

    words = []

    # Helper function to resolve the correct form of thousands, millions, and billions
    def russian_plural(number, units):
        if number % 10 == 1 and number % 100 != 11:
            return units[0]
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return units[1]
        else:
            return units[2]

    # Helper function to handle numbers below 1000
    def under_thousand(number, allow_one=True):
        if number == 0:
            return []
        elif number < 10:
            return [units[number]]
        elif number < 20:
            return [teens[number - 10]]
        elif number < 100:
            return [tens[number // 10], units[number % 10]]
        else:
            return [hundreds[number // 100]] + under_thousand(number % 100)

    # Break the number into the billions, millions, thousands, and the rest
    billions = n // 1_000_000_000
    millions = (n % 1_000_000_000) // 1_000_000
    thousands = (n % 1_000_000) // 1_000
    remainder = n % 1_000

    if billions:
        if billions != 1:
            words.extend(under_thousand(billions))
        words.append(russian_plural(billions, billion_units))
    if millions:
        if millions != 1:
            words.extend(under_thousand(millions))
        words.append(russian_plural(millions, million_units))
    if thousands:
        # Special case for 'one' and 'two' in thousands
        if thousands > 1:
            words.append(regular_number_to_femine(' '.join(under_thousand(thousands))))
        words.append(russian_plural(thousands, thousand_units))
    words += under_thousand(remainder)

    return ' '.join(word for word in words if word)

def number_to_ordinal(text, case='nominative'):
    """
    Convert the last word of a number expressed in words to its ordinal form in Russian.
    """
    # Словарь для преобразования основных числительных в порядковые
    ordinal_map = {
        'nominative': {
            'ноль': 'нулевой', 'один': 'первый', 'два': 'второй', 'три': 'третий', 'четыре': 'четвертый',
            'пять': 'пятый', 'шесть': 'шестой', 'семь': 'седьмой', 'восемь': 'восьмой', 'девять': 'девятый',
            'десять': 'десятый', 'одиннадцать': 'одиннадцатый', 'двенадцать': 'двенадцатый',
            'тринадцать': 'тринадцатый', 'четырнадцать': 'четырнадцатый', 'пятнадцать': 'пятнадцатый',
            'шестнадцать': 'шестнадцатый', 'семнадцать': 'семнадцатый', 'восемнадцать': 'восемнадцатый',
            'девятнадцать': 'девятнадцатый', 'двадцать': 'двадцатый', 'тридцать': 'тридцатый',
            'сорок': 'сороковой', 'пятьдесят': 'пятидесятый', 'шестьдесят': 'шестидесятый',
            'семьдесят': 'семидесятый', 'восемьдесят': 'восьмидесятый', 'девяносто': 'девяностый',
            'сто': 'сотый', 'двести': 'двухсотый', 'триста': 'трехсотый', 'четыреста': 'четырехсотый',
            'пятьсот': 'пятисотый', 'шестьсот': 'шестисотый', 'семьсот': 'семисотый',
            'восемьсот': 'восьмисотый', 'девятьсот': 'девятисотый', 'тысяча': 'тысячный',
            'миллион': 'миллионный', 'миллиард': 'миллиардный'
        },
        'nominative_neuter': {
            'ноль': 'нулевое', 'один': 'первое', 'два': 'второе', 'три': 'третье', 'четыре': 'четвертое',
            'пять': 'пятое', 'шесть': 'шестое', 'семь': 'седьмое', 'восемь': 'восьмое', 'девять': 'девятое',
            'десять': 'десятое', 'одиннадцать': 'одиннадцатое', 'двенадцать': 'двенадцатое',
            'тринадцать': 'тринадцатое', 'четырнадцать': 'четырнадцатое', 'пятнадцать': 'пятнадцатое',
            'шестнадцать': 'шестнадцатое', 'семнадцать': 'семнадцатое', 'восемнадцать': 'восемнадцатое',
            'девятнадцать': 'девятнадцатое', 'двадцать': 'двадцатое', 'тридцать': 'тридцатое',
            'сорок': 'сороковое', 'пятьдесят': 'пятидесятое', 'шестьдесят': 'шестидесятое',
            'семьдесят': 'семидесятое', 'восемьдесят': 'восьмидесятое', 'девяносто': 'девяностое',
            'сто': 'сотое', 'двести': 'двухсотое', 'триста': 'трехсотое', 'четыреста': 'четырехсотое',
            'пятьсот': 'пятисотое', 'шестьсот': 'шестисотое', 'семьсот': 'семисотое',
            'восемьсот': 'восьмисотое', 'девятьсот': 'девятисотое', 'тысяча': 'тысячное',
            'миллион': 'миллионное', 'миллиард': 'миллиардное'
        },
        'nominative_feminine': {
            'ноль': 'нулевая', 'один': 'первая', 'два': 'вторая', 'три': 'третья', 'четыре': 'четвертая',
            'пять': 'пятая', 'шесть': 'шестая', 'семь': 'седьмая', 'восемь': 'восьмая', 'девять': 'девятая',
            'десять': 'десятая', 'одиннадцать': 'одиннадцатая', 'двенадцать': 'двенадцатая',
            'тринадцать': 'тринадцатая', 'четырнадцать': 'четырнадцатая', 'пятнадцать': 'пятнадцатая',
            'шестнадцать': 'шестнадцатая', 'семнадцать': 'семнадцатая', 'восемнадцать': 'восемнадцатая',
            'девятнадцать': 'девятнадцатая', 'двадцать': 'двадцатая', 'тридцать': 'тридцатая',
            'сорок': 'сороковая', 'пятьдесят': 'пятидесятая', 'шестьдесят': 'шестидесятая',
            'семьдесят': 'семидесятая', 'восемьдесят': 'восьмидесятая', 'девяносто': 'девяностая',
            'сто': 'сотая', 'двести': 'двухсотая', 'триста': 'трехсотая', 'четыреста': 'четырехсотая',
            'пятьсот': 'пятисотая', 'шестьсот': 'шестисотая', 'семьсот': 'семисотая',
            'восемьсот': 'восьмисотая', 'девятьсот': 'девятисотая', 'тысяча': 'тысячная',
            'миллион': 'миллионная', 'миллиард': 'миллиардная'
        },
        'nominative_plural': {
            'ноль': 'нулевые', 'один': 'первые', 'два': 'вторые', 'три': 'третьи', 'четыре': 'четвертые',
            'пять': 'пятые', 'шесть': 'шестые', 'семь': 'седьмые', 'восемь': 'восьмые', 'девять': 'девятые',
            'десять': 'десятые', 'одиннадцать': 'одиннадцатые', 'двенадцать': 'двенадцатые',
            'тринадцать': 'тринадцатые', 'четырнадцать': 'четырнадцатые', 'пятнадцать': 'пятнадцатые',
            'шестнадцать': 'шестнадцатые', 'семнадцать': 'семнадцатые', 'восемнадцать': 'восемнадцатые',
            'девятнадцать': 'девятнадцатые', 'двадцать': 'двадцатые', 'тридцать': 'тридцатые',
            'сорок': 'сороковые', 'пятьдесят': 'пятидесятые', 'шестьдесят': 'шестидесятые',
            'семьдесят': 'семидесятые', 'восемьдесят': 'восьмидесятые', 'девяносто': 'девяностые',
            'сто': 'сотые', 'двести': 'двухсотые', 'триста': 'трехсотые', 'четыреста': 'четырехсотые',
            'пятьсот': 'пятисотые', 'шестьсот': 'шестисотые', 'семьсот': 'семисотые',
            'восемьсот': 'восьмисотые', 'девятьсот': 'девятисотые', 'тысяча': 'тысячные',
            'миллион': 'миллионные', 'миллиард': 'миллиардные'
        },
        'genitive': {
            'ноль': 'нулевого', 'один': 'первого', 'два': 'второго', 'три': 'третьего', 'четыре': 'четвертого',
            'пять': 'пятого', 'шесть': 'шестого', 'семь': 'седьмого', 'восемь': 'восьмого', 'девять': 'девятого',
            'десять': 'десятого', 'одиннадцать': 'одиннадцатого', 'двенадцать': 'двенадцатого',
            'тринадцать': 'тринадцатого', 'четырнадцать': 'четырнадцатого', 'пятнадцать': 'пятнадцатого',
            'шестнадцать': 'шестнадцатого', 'семнадцать': 'семнадцатого', 'восемнадцать': 'восемнадцатого',
            'девятнадцать': 'девятнадцатого', 'двадцать': 'двадцатого', 'тридцать': 'тридцатого',
            'сорок': 'сорокового', 'пятьдесят': 'пятидесятого', 'шестьдесят': 'шестидесятого',
            'семьдесят': 'семидесятого', 'восемьдесят': 'восьмидесятого', 'девяносто': 'девяностого',
            'сто': 'сотого', 'двести': 'двухсотого', 'триста': 'трехсотого', 'четыреста': 'четырехсотого',
            'пятьсот': 'пятисотого', 'шестьсот': 'шестисотого', 'семьсот': 'семисотого',
            'восемьсот': 'восьмисотого', 'девятьсот': 'девятисотого', 'тысяча': 'тысячного',
            'миллион': 'миллионного', 'миллиард': 'миллиардного'
        },
        'genitive_plural': {
            'ноль': 'нулевых', 'один': 'первых', 'два': 'вторых', 'три': 'третьих', 'четыре': 'четвертых',
            'пять': 'пятых', 'шесть': 'шестых', 'семь': 'седьмых', 'восемь': 'восьмых', 'девять': 'девятых',
            'десять': 'десятых', 'одиннадцать': 'одиннадцатых', 'двенадцать': 'двенадцатых',
            'тринадцать': 'тринадцатых', 'четырнадцать': 'четырнадцатых', 'пятнадцать': 'пятнадцатых',
            'шестнадцать': 'шестнадцатых', 'семнадцать': 'семнадцатых', 'восемнадцать': 'восемнадцатых',
            'девятнадцать': 'девятнадцатых', 'двадцать': 'двадцатых', 'тридцать': 'тридцатых',
            'сорок': 'сороковых', 'пятьдесят': 'пятидесятых', 'шестьдесят': 'шестидесятых',
            'семьдесят': 'семидесятых', 'восемьдесят': 'восьмидесятых', 'девяносто': 'девяностых',
            'сто': 'сотых', 'двести': 'двухсотых', 'триста': 'трехсотых', 'четыреста': 'четырехсотых',
            'пятьсот': 'пятисотых', 'шестьсот': 'шестисотых', 'семьсот': 'семисотых',
            'восемьсот': 'восьмисотых', 'девятьсот': 'девятисотых', 'тысяча': 'тысячных',
            'миллион': 'миллионных', 'миллиард': 'миллиардных'
        },
        'dative': {
            'ноль': 'нулевому', 'один': 'первому', 'два': 'второму', 'три': 'третьему', 'четыре': 'четвертому',
            'пять': 'пятому', 'шесть': 'шестому', 'семь': 'седьмому', 'восемь': 'восьмому', 'девять': 'девятому',
            'десять': 'десятому', 'одиннадцать': 'одиннадцатому', 'двенадцать': 'двенадцатому',
            'тринадцать': 'тринадцатому', 'четырнадцать': 'четырнадцатому', 'пятнадцать': 'пятнадцатому',
            'шестнадцать': 'шестнадцатому', 'семнадцать': 'семнадцатому', 'восемнадцать': 'восемнадцатому',
            'девятнадцать': 'девятнадцатому', 'двадцать': 'двадцатому', 'тридцать': 'тридцатому',
            'сорок': 'сороковому', 'пятьдесят': 'пятидесятому', 'шестьдесят': 'шестидесятому',
            'семьдесят': 'семидесятому', 'восемьдесят': 'восьмидесятому', 'девяносто': 'девяностому',
            'сто': 'сотому', 'двести': 'двухсотому', 'триста': 'трехсотому', 'четыреста': 'четырехсотому',
            'пятьсот': 'пятисотому', 'шестьсот': 'шестисотому', 'семьсот': 'семисотому',
            'восемьсот': 'восьмисотому', 'девятьсот': 'девятисотому', 'тысяча': 'тысячному',
            'миллион': 'миллионному', 'миллиард': 'миллиардному'
        },
        'dative_plural': {
            'ноль': 'нулевым', 'один': 'первым', 'два': 'вторым', 'три': 'третьим', 'четыре': 'четвертым',
            'пять': 'пятым', 'шесть': 'шестым', 'семь': 'седьмым', 'восемь': 'восьмым', 'девять': 'девятым',
            'десять': 'десятым', 'одиннадцать': 'одиннадцатым', 'двенадцать': 'двенадцатым',
            'тринадцать': 'тринадцатым', 'четырнадцать': 'четырнадцатым', 'пятнадцать': 'пятнадцатым',
            'шестнадцать': 'шестнадцатым', 'семнадцать': 'семнадцатым', 'восемнадцать': 'восемнадцатым',
            'девятнадцать': 'девятнадцатым', 'двадцать': 'двадцатым', 'тридцать': 'тридцатым',
            'сорок': 'сороковым', 'пятьдесят': 'пятидесятым', 'шестьдесят': 'шестидесятым',
            'семьдесят': 'семидесятым', 'восемьдесят': 'восьмидесятым', 'девяносто': 'девяностым',
            'сто': 'сотым', 'двести': 'двухсотым', 'триста': 'трехсотым', 'четыреста': 'четырехсотым',
            'пятьсот': 'пятисотым', 'шестьсот': 'шестисотым', 'семьсот': 'семисотым',
            'восемьсот': 'восьмисотым', 'девятьсот': 'девятисотым', 'тысяча': 'тысячным',
            'миллион': 'миллионным', 'миллиард': 'миллиардным'
        },
        'prepositional': {
            'ноль': 'нулевом', 'один': 'первом', 'два': 'втором', 'три': 'третьем', 'четыре': 'четвертом',
            'пять': 'пятом', 'шесть': 'шестом', 'семь': 'седьмом', 'восемь': 'восьмом', 'девять': 'девятом',
            'десять': 'десятом', 'одиннадцать': 'одиннадцатом', 'двенадцать': 'двенадцатом',
            'тринадцать': 'тринадцатом', 'четырнадцать': 'четырнадцатом', 'пятнадцать': 'пятнадцатом',
            'шестнадцать': 'шестнадцатом', 'семнадцать': 'семнадцатом', 'восемнадцать': 'восемнадцатом',
            'девятнадцать': 'девятнадцатом', 'двадцать': 'двадцатом', 'тридцать': 'тридцатом',
            'сорок': 'сороковом', 'пятьдесят': 'пятидесятом', 'шестьдесят': 'шестидесятом',
            'семьдесят': 'семидесятом', 'восемьдесят': 'восьмидесятом', 'девяносто': 'девяностом',
            'сто': 'сотом', 'двести': 'двухсотом', 'триста': 'трехсотом', 'четыреста': 'четырехсотом',
            'пятьсот': 'пятисотом', 'шестьсот': 'шестисотом', 'семьсот': 'семисотом',
            'восемьсот': 'восьмисотом', 'девятьсот': 'девятисотом', 'тысяча': 'тысячном',
            'миллион': 'миллионном', 'миллиард': 'миллиардном'
        },
        'instrumental': {
            'ноль': 'нулевым', 'один': 'первым', 'два': 'вторым', 'три': 'третьим', 'четыре': 'четвертым',
            'пять': 'пятым', 'шесть': 'шестым', 'семь': 'седьмым', 'восемь': 'восьмым', 'девять': 'девятым',
            'десять': 'десятым', 'одиннадцать': 'одиннадцатым', 'двенадцать': 'двенадцатым',
            'тринадцать': 'тринадцатым', 'четырнадцать': 'четырнадцатым', 'пятнадцать': 'пятнадцатым',
            'шестнадцать': 'шестнадцатым', 'семнадцать': 'семнадцатым', 'восемнадцать': 'восемнадцатым',
            'девятнадцать': 'девятнадцатым', 'двадцать': 'двадцатым', 'тридцать': 'тридцатым',
            'сорок': 'сороковым', 'пятьдесят': 'пятидесятым', 'шестьдесят': 'шестидесятым',
            'семьдесят': 'семидесятым', 'восемьдесят': 'восьмидесятым', 'девяносто': 'девяностым',
            'сто': 'сотым', 'двести': 'двухсотым', 'триста': 'трехсотым', 'четыреста': 'четырехсотым',
            'пятьсот': 'пятисотым', 'шестьсот': 'шестисотым', 'семьсот': 'семисотым',
            'восемьсот': 'восьмисотым', 'девятьсот': 'девятисотым', 'тысяча': 'тысячным',
            'миллион': 'миллионным', 'миллиард': 'миллиардным'
        },
    }

    assert case in ordinal_map, f'Your case "{case}" isn\'t supported'

    # Разбиваем текст на слова
    words = text.split()

    # Если последнее слово в списке есть в словаре, заменяем его
    if words[-1] in ordinal_map[case]:
        words[-1] = ordinal_map[case][words[-1]]
    else:
        if words[-1] in ('тысяча', 'тысячи', 'тысяч'):
            # Словарь с порядковыми числительными для разных падежей
            ordinal_endings = {
                'nominative': 'ый',
                'nominative_neuter': 'ое',
                'nominative_feminine': 'ая',
                'nominative_plural': 'ые',
                'genitive': 'ого',
                'genitive_plural': 'ых',
                'dative': 'ому',
                'dative_plural': 'ым',
                'prepositional': 'ом',
                'instrumental': 'ым',
            }

            base_word = words[-2]
            # Словарь для преобразования числительных в основу порядкового числительного
            base_to_ordinal = {
                'одна': 'одно',
                'две': 'двух',
                'три': 'трех',
                'четыре': 'четырех',
                'пять': 'пяти',
                'шесть': 'шести',
                'семь': 'семи',
                'восемь': 'восьми',
                'девять': 'девяти',
                # Добавить остальные числительные по необходимости
            }
            # Получаем основу порядкового числительного
            ordinal_base = base_to_ordinal.get(base_word)
            if not ordinal_base:
                raise ValueError(f"Числительное '{base_word}' не поддерживается.")
            
            # Добавляем окончание в зависимости от падежа
            ordinal = ordinal_base + 'тысячн' + ordinal_endings[case]
            return ordinal
            
        raise RuntimeError(f"Check an ordinal form of {words[-1]} with {case} case. Original text: {text}")

    # Возвращаем текст с порядковым числительным
    return ' '.join(words)


def number_to_words_ordinal(num: int, case='nominative'):
    return number_to_ordinal(number_to_words(num), case)


def number_to_words_digit_by_digit(text_num: str):
    units = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    return ' '.join(units[int(digit)] for digit in text_num)


def normalize_number_form(text):
    non_digit_pattern = re.compile(r'\D+')
    number_3digit_pattern = re.compile(r'\b[1-9]\d{,2}((\.|,|\s)\s*\d{3})*\b')
    def replace_number_form(match):
        return non_digit_pattern.sub('', match.group(0))
    return number_3digit_pattern.sub(replace_number_form, text)


def normalize_text_with_numbers(text, large_number_by_digit_probs=0.5):
    number_pattern = re.compile(r'\b\d+\b')

    def replace_number(match):
        original_text = match.group(0)
        number = int(original_text)
        by_digit = number >= 1_000_000_000_000 or original_text.startswith('0') or \
            (number >= 10_000_000 and random.random() < large_number_by_digit_probs)
        if by_digit:
            return number_to_words_digit_by_digit(original_text)
        else:
            return number_to_words(number)
        
    return number_pattern.sub(replace_number, text)


def normalize_text_with_numbers_force(text, large_number_by_digit_probs=0.5):
    if not any(char.isdigit() for char in text):
        return text

    conntected_numbers_pattern = re.compile(r'(?<=\D)(?=\d)|(?<=\d)(?=\D)')
    separated_text = conntected_numbers_pattern.sub(' ', text)
    normalized_text = normalize_text_with_numbers(separated_text)

    cleaned_text = re.sub(r'\s{2,}', ' ', normalized_text)
    cleaned_text = re.sub(r'\s+([,.!?])', r'\1', cleaned_text)
    return cleaned_text


def normalize_ru_phone_number(match):
    phone_number = match.group(0)
    digits = re.sub(r'[^\d\+]+', '', phone_number)
    parts = [digits[:-10], digits[-10:-7], digits[-7:-4], digits[-4:-2], digits[-2:]]
    return normalize_text_with_phone_numbers(' '.join(parts))


def normalize_time(text, half_past_hour_prob=0.5, quarter_to_hour_prob=0.5, add_time_units_prob=0.2):
    time_pattern = re.compile(r'\b\d{2}:\d{2}\b')
    def replace_time(match):
        hours, minutes = map(int, match.group(0).split(':'))
        if not hours:
            if not minutes:
                return 'полночь'
            return normalize_physical_units(f'{minutes} мин.')
        if minutes == 30 and random.random() < half_past_hour_prob:
            return f'пол {number_to_words_ordinal((hours + 1) % 12, case='genitive')}'
        if minutes == 45 and random.random() < quarter_to_hour_prob:
            return f'без пятнадцати {number_to_words((hours + 1) % 12)}'
        if random.random() < add_time_units_prob:
            result = normalize_physical_units(f'{hours} ч.')
            if minutes:
                result = ' '.join([result, normalize_physical_units(f'{minutes} мин.')])
            return result
        if minutes < 10:
            minutes = f'ноль {number_to_words(minutes)}'
        else:
            minutes = number_to_words(minutes)
        return ' '.join([number_to_words(hours), regular_number_to_femine(minutes)])
    return time_pattern.sub(replace_time, text)


def normalize_text_with_phone_numbers(text):
    non_digit_pattern = re.compile(r'\D+')
    spoken_phone_pattern = re.compile(r'(\+)?(\(?\d{1,3}([\( \-\)]+\d{1,4}){2,}\)?)')
    def replace_spoken_phone(match):
        original_text = match.group(0)
        if len(original_text) < 10:
            return original_text

        plus, number, _ = match.groups()
        numbers = non_digit_pattern.sub(' ', number).split()

        words = list()
        if plus is not None:
            words.append('плюс')
        words.extend(map(number_to_words, map(int, numbers)))
        return ' '.join(words)
    text = spoken_phone_pattern.sub(replace_spoken_phone, text)

    # Detect all phone numbers in the text
    ru_phone_pattern = re.compile(r"(?:\+?7|8)\s*\(?\d{3}\)?\s*\d{3}[-\s]?\d{2}[-\s]?\d{2}|8\d{10}")
    text = ru_phone_pattern.sub(normalize_ru_phone_number, text)
    return text

# Full function that detects and converts currency in a text to its full Russian word representation
def currency_normalization(text):
    """
    Detects currency amounts in the text and converts them to their word representations in Russian.
    """
    # Helper function to resolve the correct form of the currency units
    def russian_plural(number, units):
        if number % 10 == 1 and number % 100 != 11:
            return units[0]
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return units[1]
        else:
            return units[2]

    # Function to convert a currency amount into its word components in Russian
    def currency_to_words(amount, currency='rub'):
        # Define the currency units and subunits
        currencies = {
            'rub': (['рубль', 'рубля', 'рублей'], ['копейка', 'копейки', 'копеек']),
            'usd': (['доллар', 'доллара', 'долларов'], ['цент', 'цента', 'центов']),
            'eur': (['евро', 'евро', 'евро'], ['евроцент', 'евроцента', 'евроцентов']),  # Euro has invariable form
            'gbp': (['фунт', 'фунта', 'фунтов'], ['пенс', 'пенса', 'пенсов']),
            'uah': (['гривна', 'гривны', 'гривен'], ['копейка', 'копейки', 'копеек']),
        }

        # Get the correct currency units
        main_units, sub_units = currencies.get(currency, currencies['rub'])

        # Separate the amount into main and subunits
        main_amount = int(amount)
        sub_amount = int(round((amount - main_amount) * 100))

        # Convert numbers to words
        main_words = number_to_words(main_amount) + ' ' + russian_plural(main_amount, main_units)
        sub_words = ''

        # Add subunits if present
        if sub_amount > 0:
            sub_words = number_to_words(sub_amount) + ' ' + russian_plural(sub_amount, sub_units)

        # Combine main and subunit words
        full_currency_words = main_words.strip()
        if sub_words:
            full_currency_words += ' ' + sub_words.strip()

        return full_currency_words

    # Define currency patterns for detection
    currency_patterns = {
        'rub': [r'(\d+(?:\.\d\d)?)\s*(руб(л(ей|я|ь))?|₽)', r'(\d+(?:\.\d\d)?)\s*RUB'],
        'usd': [r'(\d+(?:\.\d\d)?)\s*(доллар(ов|а|ы)?|\$)', r'(\d+(?:\.\d\d)?)\s*USD', r'\$(\d+(?:\.\d\d)?)'],
        'eur': [r'(\d+(?:\.\d\d)?)\s*(евро|€)', r'(\d+(?:\.\d\d)?)\s*EUR', r'(\d+)\s*€'],
        'gbp': [r'(\d+(?:\.\d\d)?)\s*(фунт(ов|а|ы)?|£)', r'(\d+(?:\.\d\d)?)\s*GBP', r'£(\d+)'],
        'uah': [r'(\d+(?:\.\d\d)?)\s*(грив(ен|ны|на)|₴)', r'(\d+(?:\.\d\d)?)\s*UAH', r'(\d+)\s*₴'],
    }

    # Detect and convert currencies in the text
    def detect_currency(text):
        # Check each currency conntected_numbers_pattern to find matches
        for currency_code, patterns in currency_patterns.items():
            for conntected_numbers_pattern in patterns:
                matches = re.finditer(conntected_numbers_pattern, text)
                for match in matches:
                    # Extract the amount and convert it to words
                    amount = float(match.group(1))
                    currency_words = currency_to_words(amount, currency_code)
                    # Replace the original amount with its word representation in the text
                    text = re.sub(conntected_numbers_pattern, currency_words, text, count=1)

        return text

    # Run the detection and conversion on the input text
    text = detect_currency(text)
    another_currency_dict = {
        r'грн': 'uah',
        r'гр': 'uah',
        r'руб': 'rub',
        r'р': 'rub',
        r'тыс\.? ?грн': (1000, 'uah'),
        r'т\.? ?гр': (1000, 'uah'),
        r'тыс\.? ?р': (1000, 'rub'),
        r'т\.? ?р': (1000, 'rub')
    }
    non_w_pattern = re.compile(r'\W+')

    conntected_numbers_pattern = re.compile(fr'(?<!\w)([\d ]*\d[\d ]*)({"|".join(another_currency_dict.keys())})\b(\.)?( \w)?')

    for key, value in tuple(another_currency_dict.items()):
        another_currency_dict[non_w_pattern.sub('', key)] = value

    def normalize_2(match):
        amount, currency, dot, next_letter = match.groups()
        amount = int(amount.replace(' ', ''))
        currency = another_currency_dict[non_w_pattern.sub('', currency)]
        if isinstance(currency, tuple):
            multiplier, currency = currency
            amount *= multiplier

        text = currency_to_words(amount, currency)
        if next_letter is not None:
            if dot is not None and next_letter.isupper():
                text += '.'
            text += next_letter
        return text

    text = conntected_numbers_pattern.sub(normalize_2, text)

    return text

# Updated function to normalize dates in a given text with month names and ordinal days
def normalize_dates(text, year_word_prob=0.5, genitive_ordinal_day_prob=0.5):
    # Month names in Russian in the genitive case
    month_names = {
        '01': 'января', '02': 'февраля', '03': 'марта',
        '04': 'апреля', '05': 'мая', '06': 'июня',
        '07': 'июля', '08': 'августа', '09': 'сентября',
        '10': 'октября', '11': 'ноября', '12': 'декабря'
    }

    # Regular expression for matching dates in DD.MM.YYYY format
    date_pattern_1 = re.compile(r'\b(\d{2})[. /\\-]{1,2}(\d{2})[. /\\-]{1,2}(\d{4})(\s*г\.|\s*года)?(?!\w)( \w)?')
    date_pattern_2 = re.compile(r'\b(\d{4})[. /\\-]{1,2}(\d{2})[. /\\-]{1,2}(\d{2})\b')
    date_pattern_3 = re.compile(fr'(?i)\b((\d{{1,2}})[. /\\-]{{0,2}})?({"|".join(month_names.values())})([. /\\-]{{0,2}}(\d{{4}}))?(\s*г\.|\s*года)?(?!\w)( \w)?')

    # Function to normalize a single date
    def normalize_date(day, month, year, year_word_prob):
        # Convert day to ordinal word and year to words
        if day is not None:
            case = 'genitive' if random.random() < genitive_ordinal_day_prob else 'nominative_neuter'
            day_word = number_to_words_ordinal(int(day), case)
        if year is not None:
            year_word = number_to_words_ordinal(int(year), case='genitive')
        # Use the month name from the mapping
        month_name = month_names.get(month, month)
        # Construct the normalized date string in the format "7 января 2021 года"
        if day is None:
            text = f'{month_name} {year_word}'
        elif year is None:
            text = f'{day_word} {month_name}'
        else:
            text = f'{day_word} {month_name} {year_word}'
        if year_word_prob != 1:
            assert 0 <= year_word_prob <= 1
            if random.random() <= year_word_prob:
                text += ' года'
        else:
            text += ' года'
        return text

    # Function to normalize a single date DD.MM.YYYY
    def normalize_date_1(match):
        day, month, year, year_word, next_letter = match.groups()
        custom_year_word_prob = year_word_prob if year_word is None else 1
        text = normalize_date(day, month, year, custom_year_word_prob)
        if next_letter is not None:
            if year_word is not None and year_word.endswith('.') and next_letter.isupper():
                text += '.'
            text += next_letter
        return text

    # Function to normalize a single date YYYY.MM.DD
    def normalize_date_2(match):
        year, month, day = match.groups()
        return normalize_date(day, month, year, year_word_prob)

    # Function to normalize a single date DD? month YYYY? year?
    def normalize_date_3(match):
        day, _, month, _, year, year_word, next_letter = match.groups()
        custom_year_word_prob = year_word_prob
        if year_word is not None:
            custom_year_word_prob = 1
        elif year is None:
            custom_year_word_prob = 0
        if day is None and year is None:
            return match.group(0)
        text = normalize_date(day, month, year, custom_year_word_prob)
        if next_letter is not None:
            if year_word is not None and year_word.endswith('.') and next_letter.isupper():
                text += '.'
            text += next_letter
        return text

    # Replace all found dates in the text with their normalized forms
    for _ in range(2):
        normalized_text = date_pattern_1.sub(normalize_date_1, text)
        normalized_text = date_pattern_2.sub(normalize_date_2, normalized_text)
        normalized_text = date_pattern_3.sub(normalize_date_3, normalized_text)

    # Function to normalize a single date YYYY.MM.DD
    def normalize_utc(match):
        utc, sign, num = match.groups()
        return f'ютиси {"минус" if sign == "-" else "плюс"} {number_to_words(int(num))}'

    utc_pattern = re.compile(r'(?i)(utc) ?(-|\+) ?(\d{1,2})')
    normalized_text = utc_pattern.sub(normalize_utc, normalized_text)

    return normalized_text

def normalize_years(text):
    def normalize_single_year(match):
        year, ending, next_letter = match.groups()
        case = 'nominative'
        if ending == 'г.':
            ending = 'год'
        elif ending == 'года':
            case = 'genitive'
        elif ending == 'году':
            case = 'prepositional'
        elif ending == 'годе':
            case = 'prepositional'
        elif ending == 'годом':
            case = 'instrumental'

        text = f'{number_to_words_ordinal(int(year), case)} {ending}'
        if next_letter is not None:
            if next_letter.isupper():
                text += '.'
            text += next_letter
        return text

    def normalize_multi_year(match):
        original_text = match.group(0)
        prefix, year1, union, year2, _, ending, next_letter = match.groups()
        case = 'nominative'
        if ending in ['гг', 'гг.']:
            ending = 'годы'
        elif ending == 'годов':
            case = 'genitive'
        elif ending == 'годам':
            case = 'dative'
        elif ending == 'годах':
            case = 'prepositional'
        elif ending == 'годами':
            case = 'instrumental'

        if ending is None and (len(year1) < 4 or len(year2) < 4):
            return original_text

        if prefix is not None:
            year1 = number_to_words_ordinal(int(year1), 'genitive')
            year2 = number_to_words_ordinal(int(year2), 'nominative')
        else:
            year1 = number_to_words_ordinal(int(year1), case)
            year2 = number_to_words_ordinal(int(year2), case)

        text = f'{year1} {union} {year2}'
        if prefix is not None:
            text = f'{prefix}{text}'
        if ending is not None:
            text = f'{text} {ending}'
        if next_letter is not None:
            if next_letter.isupper():
                text += '.'
            text += next_letter
        if original_text.endswith(' '):
            text += ' '
        return text

    multi_year_pattern = re.compile(r'(?i)\b(С )?(\d+) ?(-|по) ?(\d+)( ?(гг\.?|годы|годов|годам|годах|годами))?(?!\w)( \w)?')
    single_year_pattern = re.compile(r'(?i)\b(\d+) ?(г\.|год|года|году|годе|годом)(?!\w)( \w)?')

    for _ in range(2):
        text = multi_year_pattern.sub(normalize_multi_year, text)
        text = single_year_pattern.sub(normalize_single_year, text)

    return text

def normalize_ordinals_years(text):
    def _normalize_ordinals_years(match):
        original_text = match.group(0)
        num, ending = match.groups()
        cases = [
            'nominative', 'genitive', 'dative', 'prepositional', 'instrumental',
            'nominative_plural', 'nominative_feminine', 'nominative_neuter',
            'genitive_plural', 'dative_plural']
        num = number_to_words(int(num))
        for case in cases:
            maybe_text = number_to_ordinal(num, case)
            if maybe_text.endswith(ending):
                return maybe_text
        return original_text

    ordinals_years_pattern = re.compile(r'(?i)\b(\d+)-?([а-я]{1,3})\b')
    text = ordinals_years_pattern.sub(_normalize_ordinals_years, text)
    return text

def normalize_roman(text):
    def normalize_signle_roman(match):
        original_text = match.group(0)
        str_number, _, ending, next_letter = match.groups()
        number = roman_to_int(str_number.upper())
        if ending is None and len(str_number) < 4 and (number > 21 or original_text in 'xхi'):
            return original_text

        case = 'nominative'
        if ending == 'в.':
            ending = 'век'
        if ending == 'ст.':
            ending = 'столетие'
            case = 'nominative_neuter'
        if ending in ['века', 'столетия']:
            case = 'genitive'
        elif ending in ['веку', 'столетию']:
            case = 'dative'
        elif ending in ['веке', 'столетии']:
            case = 'prepositional'
        text = number_to_words_ordinal(number, case)
        if ending is not None:
            text = f'{text} {ending}'
        if next_letter is not None:
            if next_letter.isupper():
                text += '.'
            text += next_letter
        if original_text.endswith(' '):
            text += ' '
        return text

    def normalize_multi_roman(match):
        number1, number2, _, ending, next_letter = match.groups()
        case = 'nominative'
        if ending in ['вв', 'вв.']:
            ending = 'века'
        if ending == 'ст.':
            ending = 'столетия'
            case = 'nominative_neuter'
        elif ending in ['веков', 'столетий']:
            case = 'genitive'
        elif ending in ['векам', 'столетиям']:
            case = 'dative'
        elif ending in ['веках', 'столетиях']:
            case = 'prepositional'
        number1 = number_to_words_ordinal(roman_to_int(number1.upper()), case)
        number2 = number_to_words_ordinal(roman_to_int(number2.upper()), case)
        text = f'{number1} - {number2}'
        if ending is not None:
            text = f'{text} {ending}'
        if next_letter is not None:
            if next_letter.isupper():
                text += '.'
            text += next_letter
        if match.group(0).endswith(' '):
            text += ' '
        return text

    multi_year_pattern = re.compile(r'(?i)\b([IVXХLCDM]+) ?- ?([IVXХLCDM]+)( ?(вв\.?|ст\.|века|столетия|веков|столетий|веках|столетиях|векам|столетиям))?(?!\w)( \w)?')
    single_roman_pattern = re.compile(r'(?i)\b([IVXХLCDM]+)( ?(в\.|век|века|веке|веку|ст\.|столетие|столетия|столетии|столетию))?(?!\w)( \w)?')

    for _ in range(2):
        text = multi_year_pattern.sub(normalize_multi_roman, text)
        text = single_roman_pattern.sub(normalize_signle_roman, text)

    return text

def normalize_capitals(text):
    capital_letter_pattern = re.compile(r'([.?!]\s*)(\w)')
    def normalize_capital_letter(match):
        sign, letter = match.groups()
        return f'{sign}{letter.upper()}'
    
    text = capital_letter_pattern.sub(normalize_capital_letter, text)
    return text

def normalize_russian(
    text,
    abbreviations_exanding=False,
    year_word_prob=0.5,
    large_number_by_digit_probs=0.5,
    genitive_ordinal_day_prob=0.75,
    half_past_hour_prob=0.5,
    quarter_to_hour_prob=0.5,
    add_time_units_prob=0.2,
    capitalize=True,
):
    text = normalize_time(text, half_past_hour_prob, quarter_to_hour_prob, add_time_units_prob)
    text = normalize_dates(text, year_word_prob, genitive_ordinal_day_prob)
    text = normalize_years(text)
    text = normalize_ordinals_years(text)
    text = normalize_roman(text)
    text = normalize_abbreviations(text)
    if abbreviations_exanding:
        text = expand_abbreviations(text)
    text = normalize_text_with_phone_numbers(text)
    text = normalize_number_form(text)
    text = currency_normalization(text)
    text = normalize_physical_units(text)
    text = normalize_text_with_numbers(text, large_number_by_digit_probs)
    text = cyrrilize(text)
    text = normalize_text_with_numbers_force(text, large_number_by_digit_probs)
    if capitalize:
        text = normalize_capitals(text)
    return text
