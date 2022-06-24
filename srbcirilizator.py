#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Done according to: https://github.com/turanjanin/cirilizator
class SrbCirilizator():

    # Digraphs must be placed first
    initial_map = {
        "DJ": "Ђ",
        "DЈ": "Ђ", # D + cyrillic J
        "Dj": "Ђ",
        "Dј": "Ђ", # D + cyrillic j
        "LJ": "Љ",
        "LЈ": "Љ", # L + cyrillic J
        "Ǉ":  "Љ",
        "Lj": "Љ",
        "Lј": "Љ", # L + cyrillic j
        "ǈ":  "Љ",
        "NJ": "Њ",
        "NЈ": "Њ", # N + cyrillic J
        "Ǌ":  "Њ",
        "Nj": "Њ",
        "Nј": "Њ", # N + cyrillic j
        "ǋ":  "Њ",
        "DŽ": "Џ",
        "Ǆ":  "Џ",
        "DŽ": "Џ", # D + Z with caron
        "Dž": "Џ",
        "ǅ":  "Џ",
        "Dž": "Џ", # D + z with caron
        "dj": "ђ",
        "dј": "ђ", # d + cyrillic j
        "lj": "љ",
        "lј": "љ", # l + cyrillic j
        "ǉ":  "љ",
        "nj": "њ",
        "nј": "њ", # n + cyrillic j
        "ǌ":  "њ",
        "dž": "џ",
        "ǆ":  "џ",
        "dž": "џ", # d + z with caron
        "A":  "А",
        "B":  "Б",
        "V":  "В",
        "G":  "Г",
        "D":  "Д",
        "Đ":  "Ђ",
        "Ð":  "Ђ",
        "ᴆ":  "Ђ",
        "E":  "Е",
        "Ž":  "Ж",
        "Ž":  "Ж", # Z with caron
        "Z":  "З",
        "I":  "И",
        "J":  "Ј",
        "K":  "К",
        "L":  "Л",
        "M":  "М",
        "N":  "Н",
        "O":  "О",
        "P":  "П",
        "R":  "Р",
        "S":  "С",
        "T":  "Т",
        "Ć":  "Ћ",
        "Ć":  "Ћ", # C with acute accent
        "U":  "У",
        "F":  "Ф",
        "H":  "Х",
        "C":  "Ц",
        "Č":  "Ч",
        "Č":  "Ч", # C with caron
        "Š":  "Ш",
        "Š":  "Ш", # S with caron
        "a":  "а",
        "æ":  "ае",
        "b":  "б",
        "v":  "в",
        "g":  "г",
        "d":  "д",
        "đ":  "ђ",
        "e":  "е",
        "ž":  "ж",
        "ž":  "ж", # z with caron
        "z":  "з",
        "i":  "и",
        "ĳ":  "иј",
        "j":  "ј",
        "k":  "к",
        "l":  "л",
        "m":  "м",
        "n":  "н",
        "o":  "о",
        "œ":  "ое",
        "p":  "п",
        "r":  "р",
        "s":  "с",
        "ﬆ":  "ст",
        "t":  "т",
        "ć":  "ћ",
        "ć":  "ћ", # c with acute accent
        "u":  "у",
        "f":  "ф",
        "ﬁ":  "фи",
        "ﬂ":  "фл",
        "h":  "х",
        "c":  "ц",
        "č":  "ч",
        "č":  "ч", # c with caron
        "š":  "ш",
        "š":  "ш", # s with caron
    }

    serbian_words_with_foreign_character_combinations = [
        "ammar",
        "amss",
        "aparthejd",
        "ddor",
        "dss",
        "dvadesettrog",
        "epp",
        "fss",
        "gss",
        "interreakc",
        "interresor",
        "izzzdiovns",
        "kss",
        "llsls",
        "mmf",
        "naddu",
        "natha",
        "natho",
        "ommetar",
        "penthaus",
        "palack",
        "poddirektor",
        "poddisciplin",
        "poddomen",
        "poddres",
        "posthumn",
        "posttrans",
        "posttraum",
        "pothodni",
        "pothranj",
        "preddijabetes",
        "prethod",
        "ptt",
        "sbb",
        "sdss",
        "ssp",
        "ssrnj",
        "sssr",
        "superračun",
        "šopingholi",
        "tass",
        "transseks",
        "transsibir",
        "tridesettrog",
        "uppr",
        "vannastav"
    ]

    common_foreign_words = [
        "administration",
        "adobe",
        "advanced",
        "advertising",
        "autocad",
        "bitcoin",
        "book",
        "boot",
        "cancel",
        "canon",
        "carlsberg",
        "cisco",
        "clio",
        "cloud",
        "coca-col",
        "cookie",
        "cooking",
        "cool",
        "covid",
        "dacia",
        "default",
        "develop",
        "e-mail",
        "edge",
        "email",
        "emoji",
        "english",
        "facebook",
        "fashion",
        "food",
        "foundation",
        "gaming",
        "gmail",
        "gmt",
        "good",
        "google",
        "hdmi",
        "image",
        "iphon",
        "ipod",
        "javascript",
        "jazeera",
        "joomla",
        "league",
        "like",
        "linkedin",
        "look",
        "macbook",
        "mail",
        "manager",
        "maps",
        "mastercard",
        "mercator",
        "microsoft",
        "mitsubishi",
        "notebook",
        "nvidia",
        "online",
        "outlook",
        "panasonic",
        "pdf",
        "peugeot",
        "podcast",
        "postpaid",
        "printscreen",
        "procredit",
        "project",
        "punk",
        "renault",
        "rock",
        "screenshot",
        "seen",
        "selfie",
        "share",
        "shift",
        "shop",
        "smartphone",
        "space",
        "steam",
        "stream",
        "subscrib",
        "tool",
        "topic",
        "trailer",
        "ufc",
        "unicredit",
        "username",
        "viber"
    ]

    whole_foreign_words = [
        "air",
        "alpha",
        "and",
        "back",
        "bitcoin",
        "celebrities",
        "conditions",
        "co2",
        "cpu",
        "creative",
        "disclaimer",
        "dj",
        "electronics",
        "fresh",
        "fun",
        "geographic",
        "gmbh",
        "h2o",
        "hair",
        "have",
        "home",
        "ii",
        "iii",
        "idj",
        "idjtv",
        "life",
        "live",
        "login",
        "national",
        "made",
        "makeup",
        "must",
        "previous",
        "public",
        "reserved",
        "terms",
        "url",
        "vii",
        "viii",
        "visa"
    ]

    foreign_character_combinations = [
        'q',
        'w',
        'x',
        'y',
        'é',
        'á',
        'ó',
        'ü',
        'ö',
        'ä',
        'ê',
        'è',
        'ú',
        'í',
        'ő',
        'ű',
        'ñ',
        'ş',
        'ç',
        'ğ',
        'ı',
        'ł',
        'ø',
        'ß',
        '&',
        '@',
        '#',
        'bb',
        'cc',
        'ck',
        'cs',
        'dd',
        'ee',
        'ff',
        'gg',
        'gy',
        'hh',
        'kk',
        'll',
        'ly',
        'mm',
        'nn',
        'ny',
        'ph',
        'pp',
        'rr',
        'sh',
        'ss',
        'sz',
        'tt',
        'zs',
        'zz',
        'ch',
        'gh',
        'th',
        '\'s',
        '\'t',
        '.com',
        '.edu',
        '.net',
        '.info',
        '.rs',
        '.org',
        '©',
        '®',
        '™'
    ]

    digraph_exceptions = {
        "dj": [
            "adjektiv",
            "adjunkt",
            "bazdje",
            "bdje",
            "bezdje",
            "blijedje",
            "bludje",
            "bridjе",
            "vidjel",
            "vidjet",
            "vindjakn",
            "višenedje",
            "vrijedje",
            "gdje",
            "gudje",
            "gdjir",
            "daždje",
            "dvonedje",
            "devetonedje",
            "desetonedje",
            "djb",
            "djeva",
            "djevi",
            "djevo",
            "djed",
            "djejstv",
            "djel",
            "djenem",
            "djeneš",
            # "djene" rare (+ Дјене (town)), but it would colide with ђене-ђене, ђеневљанка, ђенерал итд.
            "djenu",
            "djet",
            "djec",
            "dječ",
            "djuar",
            "djubison",
            "djubouz",
            "djuer",
            "djui",
            # "djuk", djuk (engl. Duke) косило би се нпр. са Djukanović
            "djuks",
            "djulej",
            "djumars",
            "djupont",
            "djurant",
            "djusenberi",
            "djuharst",
            "djuherst",
            "dovdje",
            "dogrdje",
            "dodjel",
            "drvodje",
            "drugdje",
            "elektrosnabdje",
            "žudje",
            "zabludje",
            "zavidje",
            "zavrijedje",
            "zagudje",
            "zadjev",
            "zadjen",
            "zalebdje",
            "zaludje",
            "zaodje",
            "zapodje",
            "zarudje",
            "zasjedje",
            "zasmrdje",
            "zastidje",
            "zaštedje",
            "zdje",
            "zlodje",
            "igdje",
            "izbledje",
            "izblijedje",
            "izvidje",
            "izdjejst",
            "izdjelj",
            "izludje",
            "isprdje",
            "jednonedje",
            "kojegdje",
            "kudjelj",
            "lebdje",
            "ludjel",
            "ludjet",
            "makfadjen",
            "marmadjuk",
            "međudjel",
            "nadjaha",
            "nadjača",
            "nadjeb",
            "nadjev",
            "nadjenul",
            "nadjenuo",
            "nadjenut",
            "negdje",
            "nedjel",
            "nadjunač",
            "nenadjača",
            "nenadjebi",
            "nenavidje",
            "neodje",
            "nepodjarm",
            "nerazdje",
            "nigdje",
            "obdjel",
            "obnevidje",
            "ovdje",
            "odjav",
            "odjah",
            "odjaš",
            "odjeb",
            "odjev",
            "odjed",
            "odjezd",
            "odjek",
            "odjel",
            "odjen",
            "odjeć",
            "odjec",
            "odjur",
            "odsjedje",
            "ondje",
            "opredje",
            "osijedje",
            "osmonedje",
            "pardju",
            "perdju",
            "petonedje",
            "poblijedje",
            "povidje",
            "pogdjegdje",
            "pogdje",
            "podjakn",
            "podjamč",
            "podjastu",
            "podjemč",
            "podjar",
            "podjeb",
            "podjed",
            "podjezič",
            "podjel",
            "podjen",
            "podjet",
            "pododjel",
            "pozavidje",
            "poludje",
            "poljodjel",
            "ponegdje",
            "ponedjelj",
            "porazdje",
            "posijedje",
            "posjedje",
            "postidje",
            "potpodjel",
            "poštedje",
            "pradjed",
            "prdje",
            "preblijedje",
            "previdje",
            "predvidje",
            "predjel",
            "preodjen",
            "preraspodje",
            "presjedje",
            "pridjev",
            "pridjen",
            "prismrdje",
            "prištedje",
            "probdje",
            "problijedje",
            "prodjen",
            "prolebdje",
            "prosijedje",
            "prosjedje",
            "protivdjel",
            "prošlonedje",
            "radjard",
            "razvidje",
            "razdjev",
            "razdjel",
            "razodje",
            "raspodje",
            "rasprdje",
            "remekdjel",
            "rudjen",
            "rudjet",
            "sadje",
            "svagdje",
            "svidje",
            "svugdje",
            "sedmonedjelj",
            "sijedje",
            "sjedje",
            "smrdje",
            "snabdje",
            "snovidje",
            "starosjedje",
            "stidje",
            "studje",
            "sudjel",
            "tronedje",
            "ublijedje",
            "uvidje",
            "udjel",
            "udjen",
            "uprdje",
            "usidjel",
            "usjedje",
            "usmrdje",
            "uštedje",
            "cjelonedje",
            "četvoronedje",
            "čukundjed",
            "šestonedjelj",
            "štedje",
            "štogdje",
            "šukundjed",
        ],
        "dž": [
            "feldžandarm",
            "nadžanj",
            "nadždrel",
            "nadžel",
            "nadžeo",
            "nadžet",
            "nadživ",
            "nadžinj",
            "nadžnj",
            "nadžrec",
            "nadžup",
            "odžali",
            "odžari",
            "odžel",
            "odžive",
            "odživljava",
            "odžubor",
            "odžvaka",
            "odžval",
            "odžvać",
            "podžanr",
            "podžel",
            "podže",
            "podžig",
            "podžiz",
            "podžil",
            "podžnje",
            "podžupan",
            "predželu",
            "predživot",
        ],
        "nj": [
            "anjon",
            "injaric",
            "injekc",
            "injekt",
            "injicira",
            "injurij",
            "kenjon",
            "konjug",
            "konjunk",
            "nekonjug",
            "nekonjunk",
            "ssrnj",
            "tanjug",
            "vanjezičk",
        ],
    }

    # See: https://en.wikipedia.org/wiki/Zero-width_non-joiner
    digraph_replacements = {
        "dj": {
            "dj": "d\u200Cj",
            "Dj": "D\u200Cj",
            "DJ": "D\u200CJ",
        },
        "dž": {
            "dž": "d\u200Cž",
            "Dž": "D\u200Cž",
            "DŽ": "D\u200CŽ",
        },
        "nj": {
            "nj": "n\u200Cj",
            "Nj": "N\u200Cj",
            "NJ": "N\u200CJ",
        }
    }

    def text_to_cyrillic(self, text):
        if len(text.strip()) == 0:
            return text
        words = re.split('\s+', text)
        for i in range(len(words)):
            index = self.transliteration_index_of_word_starts_with(words[i], self.whole_foreign_words, "-")
            if index >= 0:
                words[i] = words[i][:index] + self.word_to_cyrillic(words[i][index:])
            else:
                if not self.looks_like_foreign_word(words[i]):
                    words[i] = self.word_to_cyrillic(words[i])
        return ' '.join(words)


    def looks_like_foreign_word(self, word):
        trimmed_word = self.trim_excessive_characters(word)
        word = trimmed_word.lower()

        if word == "":
            return False

        if self.word_starts_with(word, self.serbian_words_with_foreign_character_combinations):
            return False

        if self.word_contains_string(word, self.foreign_character_combinations):
            return True

        if self.word_starts_with(word, self.common_foreign_words):
            return True

        if self.word_is_equal_to(word, self.whole_foreign_words):
            return True

        if self.word_contains_measurement_unit(trimmed_word):
            return True

        return False


    def word_to_cyrillic(self, word):
        word = self.split_latin_digraphs(word)
        for key, value in self.initial_map.items():
            word = word.replace(key, value)
        return word


    def split_latin_digraphs(self, str1):
        lowercaseStr = str1.strip().lower()

        for digraph in self.digraph_exceptions:
            #print(f'digraph={digraph}')
            if not digraph in lowercaseStr:
                continue

            for word in self.digraph_exceptions[digraph]:
                #print(f'word={word}')
                if not lowercaseStr.startswith(word):
                    continue

                # Split all possible occurrences, regardless of case
                for key in self.digraph_replacements[digraph]:
                    str1 = str1.replace(key, self.digraph_replacements[digraph][key])

                break
        #print(f"Splitted word: {str1}")
        return str1


    def word_contains_string(self, word, array):
        for array_word in array:
            if array_word in word:
                return True
        return False

    def word_is_equal_to(self, word, array):
        for array_word in array:
            if word == array_word:
                return True
        return False

    def word_starts_with(self, word, array):
        for array_word in array:
            if word.startswith(array_word):
                return True
        return False

    def word_contains_measurement_unit(self, word):
        unit_adjacent_to_sth = "([zafpnμmcdhKMGTPEY]?([BVWJFSHCΩATNhlmg]|m[²³]?|s[²]?|cd|Pa|Wb|Hz))"
        unit_optionaly_adjacent_to_sth = "(°[FC]|[kMGTPZY](B|Hz)|[pnμmcdhk]m[²³]?|m[²³]|[mcdh][lg]|kg|km)"
        number = "(\d+([\.,]\d)*)"
        regExp = "^(" + number + unit_adjacent_to_sth + ")|(" \
            + number + "?(" + unit_optionaly_adjacent_to_sth + "|" \
            + unit_adjacent_to_sth + "/" + unit_adjacent_to_sth + "))$"

        #print(f"Regexp: {regExp}, {re.match(regExp, word)}")
        return re.match(regExp, word) is not None


    """
    Retrieves index of the first character of the word that should be transliterated.
    Function examines only words that have a root that is a foreign word, followed by
    some separator character and remainder of the word which is in Serbian.
    Example: dj-evi should be transliterated as dj-еви so the function retrieves 3.
    """
    def transliteration_index_of_word_starts_with(self, word, array, char_separator):
        word = self.trim_excessive_characters(word).lower()
        if word == "":
            return -1

        appended_foreign_words = list(map(lambda el: el + char_separator, array))

        for array_word in appended_foreign_words:
            if word.startswith(array_word):
                return len(array_word)

        return -1


    # Trims white spaces and punctuation marks from the start and the end of the word.
    def trim_excessive_characters(self, word):
        excessive_chars = "[\\s!?,:;\.\*\\-—~`'\"„”“”‘’(){}\\[\\]<>«»\\/\\\\]"
        regexp = "^(" + excessive_chars + ")+|(" + excessive_chars + ")+$"

        return re.sub(regexp, '', word)


if __name__ == "__main__":
    cir = SrbCirilizator()

    # Test 'trim_excessive_characters'
    assert cir.trim_excessive_characters("  !?:;.*-—~`'„”“”‘’(){}[]<>«»a!?:;.*-—~`'„”“”‘’()/\\") == "a"

    # Test 'transliteration_index_of_word_starts_with'
    assert cir.transliteration_index_of_word_starts_with('dj-evi', cir.whole_foreign_words, '-') == 3
    assert cir.transliteration_index_of_word_starts_with('makeup-om', cir.whole_foreign_words, '-') == 7

    # Test 'word_contains_measurement_unit'
    assert cir.word_contains_measurement_unit('32°C') == True

    # Test proper transliteration case of latin digraphs
    assert cir.text_to_cyrillic('Ljubičasta LJOVISNA je ljankase') == 'Љубичаста ЉОВИСНА је љанкасе'
    assert cir.text_to_cyrillic('Njiše se njopajuće NJANJAVO') == 'Њише се њопајуће ЊАЊАВО'
    assert cir.text_to_cyrillic('Džangrizavi DŽUDISTA džemper odžakom Džodi daje.') == 'Џангризави ЏУДИСТА џемпер оџаком Џоди даје.'

    # Test proper transliteration of Latin to Cyrillic
    assert cir.text_to_cyrillic('brza vižljasta lija hoće da đipi preko lenjog flegmatičnog džukca.') == 'брза вижљаста лија хоће да ђипи преко лењог флегматичног џукца.'
    assert cir.text_to_cyrillic('LJUDI, JAZAVAC DŽEF TRČI PO ŠUMI GLOĐUĆI NEKO SUHO ŽBUNJE!') == 'ЉУДИ, ЈАЗАВАЦ ЏЕФ ТРЧИ ПО ШУМИ ГЛОЂУЋИ НЕКО СУХО ЖБУЊЕ!'
    assert cir.text_to_cyrillic('Ðavo je u detaǉima, nĳe da ti Čika Džoš nije rekao?') == 'Ђаво је у детаљима, није да ти Чика Џош није рекао?'

    # Test correct transliteration of Latin digraphs
    assert cir.text_to_cyrillic('Odjednom Tanjug reče da će nadživeti injekciju. Dodjavola, džangrizava njuška je bila u pravu.') == 'Од‌једном Тан‌југ рече да ће над‌живети ин‌јекцију. Дођавола, џангризава њушка је била у праву.'

    # Test that words with foreign characters will not be transliterated
    assert cir.text_to_cyrillic('Biografiju pošaljite kao Word dokument u docx formatu za Über Yahu.') == 'Биографију пошаљите као Word документ у docx формату за Über Yahu.'

    # Test it_wont_transliterate_to_cyrillic_some_of_the_most_common_foreign_words
    assert cir.text_to_cyrillic('Moj DJ username Adobe Dacia po defaultu sve PDF dokumente šalje mailom Google developerima.') == 'Мој DJ username Adobe Dacia по defaultu све PDF документе шаље mailom Google developerima.'

    # Test it_wont_transliterate_to_cyrillic_words_with_foreign_character_combination
    assert cir.text_to_cyrillic('Naša pevačica, Jellena sa dva l, učestvovala u prethodnoj VII sezoni Big Brother muzzičkog festivalа na sajtu domen.com') == 'Наша певачица, Jellena са два л, учествовала у претходној VII сезони Биг Brother muzzičkog фестивала на сајту domen.com'