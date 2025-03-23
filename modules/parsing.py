"""
The blacklist warnings are formatted as follows:

For profanities:
Profane word detected: ike
Original: ike & tina turner
Censored: *** & tina turner

For UTF-8 stuff:
Non-ASCII characters found: キトレョギー
Original: トーキョーレギー
Unidecoded: to-kiyo-regi-

The logic here is to find out what is the original word and return it. We do that by selecting the lines that contain the original and target phrases, and then comparing them.
"""


def get_original_word(text):
    target_phrase = text.split("\n")[1].split(": ")[1]
    original_phrase = text.split("\n")[2].split(": ")[1]
    word = ""

    for char in target_phrase:
        # we check whether the current character matches the one in the original phrase. if not, add it.
        # I chose to check against the original phrase instead of "*" because the original phrase might contain it, which will mess up the result.
        if char != original_phrase[target_phrase.index(char)]:
            word += char

    return word


def is_offense_warning(text):
    return "Profane word detected" in text


def is_utf_warning(text):
    return "Non-ASCII characters found" in text
