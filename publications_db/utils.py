
def replace_special_chars(text):
    chars = (
        # basic chars having variations in special chars below
        ('a', 'aa'), ('c', 'cc'), ('e', 'ee'), ('i', 'ii'), ('l', 'll'), ('n', 'nn'), ('o', 'oo'),  ('u', 'uu'),
        ('s', 'ss'), ('y', 'yy'), ('z', 'zz'),

        # PL
        ('ą', 'aą'), ('ć', 'cć'), ('ę', 'eę'),  ('ł', 'lł'), ('ń', 'nń'), ('ó', 'oó'), ('ś', 'sś'), ('ź', 'zź'),
        ('ż', 'zż'),

        # FR (https://en.wikipedia.org/wiki/French_orthography)
        # For determining alphabetical order, ligatures æ and œ are treated like the sequences oe and ae:
        ('æ', 'ae'), ('œ', 'oe'),
        # Accents are just diacritics; those have no effect on alphabetical order:
        ('â', 'aa'), ('à', 'aa'), ('ç', 'cc'), ('é', 'ee'), ('ê', 'ee'), ('è', 'ee'), ('ë', 'ee'),
        ('î', 'ii'), ('ï', 'ii'), ('ô', 'oo'),  ('û', 'uu'), ('ü', 'uu'),  ('ù', 'uu'), ('ÿ', 'yy'),

        # DE
        ('ä', 'aä'), ('ö', 'oö'), ('ü', 'uü'), ('ß', 'sss'),

        # another_language
        # ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''),

        # DIACRITICS
        (' ', ''),
        # (',', ''), ('.', ''), (':', ''), (';', ''), ('(', ''), (')', ''), ('-', ''),
    )

    text = text.lower()
    for char in chars:
        text = text.replace(char[0], char[1])
    return text


