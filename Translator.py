import random

prefixes = [
    "<3 ",
    "0w0 ",
    "H-hewwo?? ",
    "HIIII! ",
    "Haiiii! ",
    "Huohhhh. ",
    "OWO ",
    "OwO ",
    "UwU ",
]

suffixes = [
    " ( ͡° ᴥ ͡°)",
    " (´・ω・｀)",
    " (ʘᗩʘ')",
    " (இωஇ )",
    " (๑•́ ₃ •̀๑)",
    " (• o •)",
    " (⁎˃ᆺ˂)",
    " (●´ω｀●)",
    " (◠‿◠✿)",
    " (✿ ♡‿♡)",
    " (❁´◡`❁)",
    " (　'◟ ')",
    " (人◕ω◕)",
    " (；ω；)",
    " (｀へ´)",
    " ._.",
    " :3",
    " :D",
    " :P",
    " ;-;",
    " ;3",
    " ;_;",
    " <{^v^}>",
    " >_<",
    " >_>",
    " UwU",
    " XDDD",
    " ^-^",
    " ^_^",
    " x3",
    " x3",
    " xD",
    " ÙωÙ",
    " ʕʘ‿ʘʔ",
    " ㅇㅅㅇ",
    ", fwendo",
    "（＾ｖ＾）",
]

substitutions = {
    "r": "w",
    "l": "w",
    "R": "W",
    "L": "W",
    #'ow': 'OwO',
    "no": "nu",
    "has": "haz",
    "have": "haz",
    " says": " sez",
    "you": "uu",
    "the ": "da ",
    "The ": "Da ",
    "THE ": "THE ",
}


def addAffixes(string, reverse=False):
    if reverse:
        string = string.split(" ")
        string[0] = f"{string[0]} "
        string[-1] = f" {string[-1]}"
        if string[0] in prefixes:
            string.pop(0)
        if string[-1] in suffixes:
            string.pop(-1)
        string = " ".join(string)
    else:
        string = random.choice(prefixes) + string + random.choice(suffixes)
    return string


def substitute(string, reverse=False):
    replacements = []
    if reverse:
        toBeReplaced = list(substitutions)
        for k in toBeReplaced:
            replacements.append(substitutions[k])

        for word in replacements:
            string = string.replace(word, toBeReplaced[replacements.index(word)])

    else:
        replacements = list(substitutions)
        for word in replacements:
            string = string.replace(word, substitutions[word])
    return string


def owo(string, translate=False, reverse=False):
    if translate:
        return substitute(string)

    else:
        return (
            addAffixes(substitute(string, reverse=True), reverse=True)
            if reverse
            else addAffixes(substitute(string))
        )

