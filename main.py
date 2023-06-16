import json
import os
import re
import time


def load_file(filepath):
    filelist = []
    for root, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(tuple([".json", ".mcfunction"])):
                filelist.append(os.path.join(root, filename))
    return filelist


def load_lang(lang_file):
    with open(lang_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return json.loads(content)


def modify(filelist, lang):
    for file in filelist:
        with open(file, 'r+', encoding='utf-8') as f:
            con = search_str(f.read(), lang)

            f.seek(0)
            f.truncate()
            f.write(con)
            f.close()


def search_str(con, lang):
    translate_keys = re.findall('("translate":"(.*?)")', con)
    translate_keys_order = re.findall(r'(\\"translate\\":\\"(.*?)\\")', con)
    text_keys = re.findall('("text":"(.*?)")', con)

    con = replace_str(translate_keys, con, lang)
    con = replace_str(translate_keys_order, con, lang)
    con = replace_str(text_keys, con, lang)

    return con


def replace_str(keys, con, lang):
    if keys:
        for dirt_value in keys:
            dirt_ = dirt_value[0]
            value_ = dirt_value[1]
            try:
                new_dirt = dirt_.replace(value_, lang[value_], 1)
                con = con.replace(dirt_, new_dirt, 1)
            except KeyError:
                pass
    return con


if __name__ == '__main__':
    start_time = time.time()

    files = load_file('BlazeandCavesAdvancementsPack\data')
    langC = load_lang('zh_cn.json')
    modify(files, langC)

    end_time = time.time()
    print(f"替换完成 总用时 {end_time - start_time}s")
