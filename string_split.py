import re

new_file_name = "(コミティア102) [臨終サーカス (はぐはぐ)] このは恋心 ～先生に恋する少女～ [中国翻訳](COMITIA102) [Rinjuu Circus (Haguhagu)] Konoha Koigokoro ~Sensei ni Koi suru Shoujo~ [Chinese] [脸肿汉化组]"
if "[中国翻訳]" in new_file_name and "[Chinese]" in new_file_name:
    spilter1 = "[中国翻訳]"
    spilter2 = "[Chinese]"
    p1 = new_file_name.split(spilter1)
    p2 = new_file_name.split(spilter2)
    print(p1[0] + p2[1])