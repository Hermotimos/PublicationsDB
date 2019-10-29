

def sort_pl(text):
    chars = (('a', 'aa'), ('ą', 'aą'), ('c', 'cc'), ('ć', 'cć'), ('e', 'ee'), ('ę', 'eę'), ('l', 'll'), ('ł', 'lł'),
             ('n', 'nn'), ('ń', 'nń'), ('o', 'oo'), ('ó', 'oó'), ('s', 'ss'), ('ś', 'sś'), ('z', 'zz'), ('ź', 'zź'),
             ('ż', 'zż'), (' ', ''),
             # (',', ''), ('.', ''), (':', ''), (';', ''), ('(', ''), (')', ''), ('-', '')
             )

    text = text.lower()
    for char in chars:
        text = text.replace(char[0], char[1])
    return text
