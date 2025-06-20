import re


class RegexPatterns:
    # pattern to identify repeating words/tokens
    repeat_pat = re.compile(r"\b(\w+)\s+\1\s+\1(?:\s+\1)*\b")
    foo = "bar"
    # pattern to identify initial bullet characters
    initial_bullet_pattern = re.compile("^[\u002D\u058A\u05BE\u1400\u1806\u2010\u2011\u2012\u2013\u2014\u2015\u2022\u2023\u2043\u204C\u204D\u2219\u25CB\u25CF\u25D8\u25E6\u261A\u261B\u261C\u261E\u2E17\u2E1A\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D*•>·/+]", re.UNICODE) #fmt: skip
    # pattern to identify bullet characters anywhere in a string
    bullet_pattern = re.compile("[\u002D\u058A\u05BE\u1400\u1806\u2010\u2011\u2012\u2013\u2014\u2015\u2022\u2023\u2043\u204C\u204D\u2219\u25CB\u25CF\u25D8\u25E6\u261A\u261B\u261C\u261E\u2E17\u2E1A\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D*•>·/+]", re.UNICODE) # fmt: skip
