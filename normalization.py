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


# Функция для замены сокращений на полные формы
def normalize_phys_units(text):
    # Словарь с приставками и их полными формами
    values = {
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
        'гц': ['герц', 'герца', 'герцов'],
        'ггц': ['гигагерц', 'гигагерца', 'гигагерц'],
        'мгц': ['мегагерц', 'мегагерца', 'мегагерц'],
        'кгц': ['килогерц', 'килогерца', 'килогерц'],
        'вт': ['ватт', 'ватта', 'ватт'],
        'мвт': ['милливатт', 'милливатта', 'милливатт'],
        'квт': ['киловатт', 'киловатта', 'киловатт'],
        'гвт': ['гигаватт', 'гигаватта', 'гигаватт'],
        'в': ['вольт', 'вольта', 'вольт'],
        'мв': ['милливольт', 'милливольта', 'милливольт'],
        'кв': ['киловольт', 'киловольта', 'киловольт'],
        'гв': ['гигавольт', 'гигавольта', 'гигавольт'],
        'ом': ['ом', 'ома', 'омов'],
        'ком': ['килоом', 'килоома', 'килоомов'],
        'гом': ['гигаом', 'гигаома', 'гигаомов'],
        'с': ['секунда', 'секунды', 'секунд'],
        'мс': ['милисекунда', 'милисекунды', 'милисекунд'],
        'нс': ['наносекунда', 'наносекунды', 'наносекунд'],
        'пс': ['пикосекунда', 'пикосекунды', 'пикосекунд'],
        'к': ['кельвин', 'кельвина', 'кельвинов'],
        'дж': ['джоуль', 'джоуля', 'джоулей'],
        'мдж': ['миллиджоуль', 'миллиджоуля', 'миллиджоулей'],
        'кдж': ['килоджоуль', 'килоджоуля', 'килоджоулей'],
        'гдж': ['гигаджоуль', 'гигаджоуля', 'гигаджоулей'],

        'а': ['ампер', 'ампера', 'амперов'],
        'ма': ['миллиампер', 'миллиампера', 'миллиамперов'],
        'ка': ['килоампер', 'килоампера', 'килоамперов'],
        'га': ['гигаампер', 'гигаампера', 'гигаамперов'],
        'ф': ['фарад', 'фарада', 'фарадов'],
        'мф': ['микрофарад', 'микрофарада', 'микрофарадов'],
        'нф': ['нанофарад', 'нанофарада', 'нанофарадов'],
        'па': ['паскаль', 'паскаля', 'паскалей'],
        'кпа': ['килопаскаль', 'килопаскаля', 'килопаскалей'],
        'мпа': ['мегапаскаль', 'мегапаскаля', 'мегапаскалей'],
        'гпа': ['гигапаскаль', 'гигапаскаля', 'гигапаскалей'],
        'бар': ['бар', 'бара', 'баров'],
        'мбар': ['миллибар', 'миллибара', 'миллибаров'],
        'нбар': ['нанобар', 'нанобара', 'нанобаров'],
        # Добавьте остальные величины по аналогии
    }

    def russian_plural(number):
        if number % 10 == 1 and number % 100 != 11:
            return 0
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return 1
        else:
            return 2

    # Регулярное выражение для поиска сокращений
    pattern = re.compile(fr'(?i)(\d+)( )?({"|".join(values.keys())})(?=\W)')
    
    # Функция для замены сокращений на полные формы
    def replace(match):
        num, is_space, unit = match.groups()
        if unit.lower() in values:
            unit = values[unit.lower()][russian_plural(int(num))]
        return f"{num} {unit}"

    # Замена сокращений на полные формы
    return pattern.sub(replace, text)


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
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    integer = 0
    for i in range(len(s)):
        if i > 0 and roman_numerals[s[i]] > roman_numerals[s[i - 1]]:
            integer += roman_numerals[s[i]] - 2 * roman_numerals[s[i - 1]]
        else:
            integer += roman_numerals[s[i]]
    return integer

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
    def under_thousand(number):
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
        words += under_thousand(billions) + [russian_plural(billions, billion_units)]
    if millions:
        words += under_thousand(millions) + [russian_plural(millions, million_units)]
    if thousands:
        # Special case for 'one' and 'two' in thousands
        if thousands % 10 == 1 and thousands % 100 != 11:
            pass
        elif thousands % 10 == 2 and thousands % 100 != 12:
            words.append('две')
        else:
            words += under_thousand(thousands)
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
            'один': 'первый', 'два': 'второй', 'три': 'третий', 'четыре': 'четвертый', 'пять': 'пятый',
            'шесть': 'шестой', 'семь': 'седьмой', 'восемь': 'восьмой', 'девять': 'девятый',
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
        'genitive': {
            'один': 'первого', 'два': 'второго', 'три': 'третьего', 'четыре': 'четвертого', 'пять': 'пятого',
            'шесть': 'шестого', 'семь': 'седьмого', 'восемь': 'восьмого', 'девять': 'девятого',
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
        'dative': {
            'один': 'первому', 'два': 'второму', 'три': 'третьему', 'четыре': 'четвертому', 'пять': 'пятому',
            'шесть': 'шестому', 'семь': 'седьмому', 'восемь': 'восьмому', 'девять': 'девятому',
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
        'prepositional': {
            'один': 'первом', 'два': 'втором', 'три': 'третьем', 'четыре': 'четвертом', 'пять': 'пятом',
            'шесть': 'шестом', 'семь': 'седьмом', 'восемь': 'восьмом', 'девять': 'девятом',
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
            'один': 'первым', 'два': 'вторым', 'три': 'третьим', 'четыре': 'четвертым', 'пять': 'пятым',
            'шесть': 'шестым', 'семь': 'седьмым', 'восемь': 'восьмым', 'девять': 'девятым',
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
        'nominative_plural': {
            'один': 'первые', 'два': 'вторые', 'три': 'третьи', 'четыре': 'четвертые', 'пять': 'пятые',
            'шесть': 'шестые', 'семь': 'седьмые', 'восемь': 'восьмые', 'девять': 'девятые',
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
        'genitive_plural': {
            'один': 'первых', 'два': 'вторых', 'три': 'третьих', 'четыре': 'четвертых', 'пять': 'пятых',
            'шесть': 'шестых', 'семь': 'седьмых', 'восемь': 'восьмых', 'девять': 'девятых',
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
        'dative_plural': {
            'один': 'первым', 'два': 'вторым', 'три': 'третьим', 'четыре': 'четвертым', 'пять': 'пятым',
            'шесть': 'шестым', 'семь': 'седьмым', 'восемь': 'восьмым', 'девять': 'девятым',
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
        }
    }

    assert case in ordinal_map, f'Your case "{case}" isn\'t supported'

    # Разбиваем текст на слова
    words = text.split()

    # Если последнее слово в списке есть в словаре, заменяем его
    if words[-1] in ordinal_map[case]:
        words[-1] = ordinal_map[case][words[-1]]
    else:
        raise RunTimeError(f"Check an ordinal form of {words[-1]}")

    # Возвращаем текст с порядковым числительным
    return ' '.join(words)


def detect_numbers(text):
    # Regular expression pattern for matching standalone numbers
    number_pattern = re.compile(r'\b\d+\b')
    # Find all matches and return them along with their start and end indices
    matches = list(number_pattern.finditer(text))
    number_matches = [{'number': match.group(), 'start': match.start(), 'end': match.end()} for match in matches]
    
    return number_matches

def number_to_words_digit_by_digit(n):
    """
    Convert a number into its word components in Russian, digit by digit.
    """
    units = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    return ' '.join(units[int(digit)] for digit in str(n))

# Update the normalize_text_with_numbers to handle large numbers by reading them digit by digit
def normalize_text_with_numbers(text, large_number_by_digit_probs=0.5):
    # Detect all standalone numbers in the text
    detected_numbers = detect_numbers(text)
    # Sort detected numbers by their starting index in descending order
    detected_numbers.sort(key=lambda x: x['start'], reverse=True)
    
    # Replace each number with its normalized form
    for num in detected_numbers:
        number_value = int(num['number'])
        # For large numbers that are out of the range of the 'number_to_words' function, use 'number_to_words_digit_by_digit'
        if number_value >= 1_000_000_000_000:
            normalized_number = number_to_words_digit_by_digit(number_value)
        elif number_value >= 10_000_000:
            if random.random() < large_number_by_digit_probs:
                normalized_number = number_to_words_digit_by_digit(number_value)
            else:
                normalized_number = number_to_words(number_value)
        else:
            normalized_number = number_to_words(number_value)
        # Replace the original number in the text with its normalized form
        text = text[:num['start']] + normalized_number + text[num['end']:]
    
    return text


def normalize_text_with_numbers_force(text, large_number_by_digit_probs=0.5):
    if not any(char.isdigit() for char in text):
        return text

    # Регулярное выражение для поиска чисел
    pattern = r'(?<=\D)(?=\d)|(?<=\d)(?=\D)'
    
    # Замена найденных позиций на пробелы
    separated_text = re.sub(pattern, ' ', text)
    
    normalized_text = normalize_text_with_numbers(separated_text)

    # Удаление двойных пробелов
    cleaned_text = re.sub(r'\s{2,}', ' ', normalized_text)

    # Удаление лишних пробелов перед знаками препинания
    cleaned_text = re.sub(r'\s+([,.!?])', r'\1', cleaned_text)

    return cleaned_text


def normalize_phone_number(phone_number):
    # Strip the phone number of all non-numeric characters
    digits = re.sub(r'\D', '', phone_number)

    # Define the segments for the Russian phone number
    segments = {
        'country_code': digits[:1],  # +7 or 8
        'area_code': digits[1:4],    # 495
        'block_1': digits[4:7],      # 123
        'block_2': digits[7:9],      # 45
        'block_3': digits[9:11],     # 67
    }

    # Normalizing the country code
    if segments['country_code'] == '8':
        segments['country_code'] = 'восемь'
    elif segments['country_code'] == '7':
        segments['country_code'] = 'плюс семь'

    # Normalize each segment using the number_to_words function
    normalized_segments = {
        key: number_to_words(int(value)) if key != 'country_code' else value
        for key, value in segments.items()
    }

    # Combine the segments into the final spoken form
    spoken_form = ' '.join(normalized_segments.values())

    return spoken_form

# Correcting the phone number normalization function to handle various formats correctly

def normalize_text_with_phone_numbers(text):
    # Detect all phone numbers in the text
    phone_pattern = re.compile(
        r"(?:\+7|8)\s*\(?\d{3}\)?\s*\d{3}[-\s]?\d{2}[-\s]?\d{2}|8\d{10}"
    )
    # We use finditer here instead of findall to get the match objects, which will include the start and end indices.
    matches = list(phone_pattern.finditer(text))
    detected_phone_numbers = [{'phone': match.group().strip(), 'start': match.start(), 'end': match.end()} for match in matches]

    # Sort detected phone numbers by their starting index in descending order
    # This ensures that when we replace them, we don't mess up the indices of the remaining phone numbers
    detected_phone_numbers.sort(key=lambda x: x['start'], reverse=True)
    
    # Replace each phone number with its normalized form
    for pn in detected_phone_numbers:
        normalized_phone = normalize_phone_number(pn['phone'])
        # Replace the original phone number in the text with its normalized form
        text = text[:pn['start']] + normalized_phone + text[pn['end']:]
    
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
        # Check each currency pattern to find matches
        for currency_code, patterns in currency_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    # Extract the amount and convert it to words
                    amount = float(match.group(1))
                    currency_words = currency_to_words(amount, currency_code)
                    # Replace the original amount with its word representation in the text
                    text = re.sub(pattern, currency_words, text, count=1)

        return text

    # Run the detection and conversion on the input text
    return detect_currency(text)

# Updated function to normalize dates in a given text with month names and ordinal days
def normalize_dates(text, year_word_probability=0.5):
    # Month names in Russian in the genitive case
    month_names = {
        '01': 'января', '02': 'февраля', '03': 'марта',
        '04': 'апреля', '05': 'мая', '06': 'июня',
        '07': 'июля', '08': 'августа', '09': 'сентября',
        '10': 'октября', '11': 'ноября', '12': 'декабря'
    }

    # Regular expression for matching dates in DD.MM.YYYY format
    date_pattern_1 = re.compile(r'\b(\d{2})[. /\\-](\d{2})[. /\\-](\d{4})\b')
    date_pattern_2 = re.compile(r'\b(\d{4})[. /\\-](\d{2})[. /\\-](\d{2})\b')
    date_pattern_3 = re.compile(fr'(?i)\b(\d{{1,2}})?([. /\\-])?({"|".join(month_names.values())})([. /\\-])?(\d{{4}})?( года)?\b')

    # Function to normalize a single date
    def normalize_date(day, month, year, year_word_probability):
        # Convert day to ordinal word and year to words
        if day is not None:
            day_word = number_to_words_ordinal(int(day))
        if year is not None:
            year_word = number_to_ordinal(number_to_words(int(year)), case='genitive')
        # Use the month name from the mapping
        month_name = month_names.get(month, month)
        # Construct the normalized date string in the format "7 января 2021 года"
        if day is None:
            text = f'{month_name} {year_word}'
        elif year is None:
            text = f'{day_word} {month_name}'
        else:
            text = f'{day_word} {month_name} {year_word}'
        if year_word_probability != 1:
            assert 0 <= year_word_probability <= 1
            if random.random() <= year_word_probability:
                text += ' года'
        else:
            text += ' года'
        return text

    # Function to normalize a single date DD.MM.YYYY
    def normalize_date_1(match):
        day, month, year = match.groups()
        return normalize_date(day, month, year, year_word_probability)

    # Function to normalize a single date YYYY.MM.DD
    def normalize_date_2(match):
        year, month, day = match.groups()
        return normalize_date(day, month, year, year_word_probability)

    # Function to normalize a single date DD? month YYYY? year?
    def normalize_date_3(match):
        day, _, month, _, year, year_word = match.groups()
        custom_year_word_probability = year_word_probability
        if year_word is not None:
            custom_year_word_probability = 1
        elif year is None:
            custom_year_word_probability = 0
        if day is None and year is None:
            return match.group(0)
        return normalize_date(day, month, year, custom_year_word_probability)
    
    def number_to_words_ordinal(n):
        """
        Convert a number into its ordinal word components in Russian. This function is specific to days of the month,
        where ordinal numbers are required.
        """
        # Russian ordinal numbers for days (1st to 31st) in the genitive case, which is used for dates
        ordinal_days = {
            1: 'первое', 2: 'второе', 3: 'третье', 4: 'четвёртое', 5: 'пятое',
            6: 'шестое', 7: 'седьмое', 8: 'восьмое', 9: 'девятое', 10: 'десятое',
            11: 'одиннадцатое', 12: 'двенадцатое', 13: 'тринадцатое', 14: 'четырнадцатое', 15: 'пятнадцатое',
            16: 'шестнадцатое', 17: 'семнадцатое', 18: 'восемнадцатое', 19: 'девятнадцатое', 20: 'двадцатое',
            21: 'двадцать первое', 22: 'двадцать второе', 23: 'двадцать третье', 24: 'двадцать четвёртое',
            25: 'двадцать пятое', 26: 'двадцать шестое', 27: 'двадцать седьмое', 28: 'двадцать восьмое',
            29: 'двадцать девятое', 30: 'тридцатое', 31: 'тридцать первое'
        }
        return ordinal_days.get(n, '')

    # Replace all found dates in the text with their normalized forms
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
        year, ending = match.groups()
        if ending == 'г.':
            ending = 'год'
        elif ending == 'года':
            case = 'genitive'
        elif ending == 'году':
            case = 'dative'
        elif ending == 'годе':
            case = 'prepositional'
        elif ending == 'годом':
            case = 'instrumental'
        return f'{number_to_ordinal(number_to_words(int(year)))} {ending}'

    def normalize_multi_year(match):
        original_text = match.group(0)
        year1, year2, ending = match.groups()
        case = 'nominative'
        if ending == 'гг.':
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

        year1 = number_to_ordinal(number_to_words(int(year1)), case)
        year2 = number_to_ordinal(number_to_words(int(year2)), case)

        text = f'{year1} - {year2}'
        if ending is not None:
            text = f'{text} {ending}'
        if original_text.endswith(' '):
            text += ' '
        return text

    multi_year_pattern = re.compile(r'(?i)\b(\d+) ?- ?(\d+) ?(гг\.|годы|годов|годам|годах|годами)?(?!\w)')
    text = multi_year_pattern.sub(normalize_multi_year, text)

    single_year_pattern = re.compile(r'(?i)\b(\d+) ?(г\.|год|года|году|годе|годом)(?!\w)')
    text = single_year_pattern.sub(normalize_single_year, text)

    return text

def normalize_ordinals_years(text):
    def _normalize_ordinals_years(match):
        original_text = match.group(0)
        num, ending = match.groups()
        cases = [
            'nominative', 'genitive', 'dative', 'prepositional', 'instrumental',
            'nominative_plural', 'genitive_plural', 'dative_plural']
        num = number_to_words(int(num))
        for case in cases:
            maybe_text = number_to_ordinal(num, case)
            if maybe_text.endswith(ending):
                return maybe_text
        return original_text

    ordinals_years_pattern = re.compile(r'(?i)\b(\d+)-([а-я]{1,3})\b')
    text = ordinals_years_pattern.sub(_normalize_ordinals_years, text)
    return text

def normalize_roman(text):
    def normalize_signle_roman(match):
        original_text = match.group(0)
        number, ending = match.groups()
        number = roman_to_int(number.upper())
        if ending is None and (number > 21 or original_text == 'x'):
            return original_text

        case = 'nominative'
        if ending == 'в.':
            ending = 'век'
        elif ending in ['века', 'столетия']:
            case = 'genitive'
        text = number_to_ordinal(number_to_words(number), case)
        if ending is not None:
            text = f'{text} {ending}'
        if original_text.endswith(' '):
            text += ' '
        return text

    def normalize_multi_roman(match):
        number1, number2, ending = match.groups()
        case = 'nominative'
        if ending == 'вв.':
            ending = 'века'
        elif ending == 'веков':
            case = 'genitive'
        number1 = number_to_ordinal(number_to_words(roman_to_int(number1.upper())), case)
        number2 = number_to_ordinal(number_to_words(roman_to_int(number2.upper())), case)
        text = f"{number1} - {number2}"
        if ending is not None:
            text = f'{text} {ending}'
        if match.group(0).endswith(' '):
            text += ' '
        return text

    multi_year_pattern = re.compile(r'(?i)\b([IVXLCDM]+) ?- ?([IVXLCDM]+) ?(вв\.|века|веков)?(?!\w)')
    text = multi_year_pattern.sub(normalize_multi_roman, text)

    single_roman_pattern = re.compile(r'(?i)\b([IVXLCDM]+) ?(в.|век|века|столетие|столетия)?\b')
    text = single_roman_pattern.sub(normalize_signle_roman, text)
    return text

def normalize_russian(text, abbreviations_exanding=False, year_word_probability=0.5, large_number_by_digit_probs=0.5):
    if abbreviations_exanding:
        text = expand_abbreviations(text)
    text = normalize_dates(text, year_word_probability)
    text = normalize_years(text)
    text = normalize_ordinals_years(text)
    text = normalize_roman(text)
    text = currency_normalization(text)
    text = normalize_phys_units(text)
    text = normalize_text_with_phone_numbers(text)
    text = normalize_text_with_numbers(text, large_number_by_digit_probs)
    text = cyrrilize(text)
    text = normalize_text_with_numbers_force(text, large_number_by_digit_probs)
    return text
