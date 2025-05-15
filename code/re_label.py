import json
import pandas as pd
from wtpsplit import SaT
 

json_path = "data/updated_corpus_pubtator_output.json"


def simple_re_label_sentence(json_path: str) -> pd.DataFrame:
    f = open(json_path)
    data = json.load(f)

    # Updating start_index and end_index
    for (i, data_point) in enumerate(data):
        dummy = data[i]["data"]["en_text"]

        for (j, labeling) in enumerate(data_point["predictions"][0]['result']):
            start_index = labeling['value']['start']
            end_index = labeling['value']['end']
            temp = dummy[:start_index]
            # c = temp.count(".\n")
            c = temp.count(". ")
            data[i]["predictions"][0]['result'][j]['value']['start'] += c
            data[i]["predictions"][0]['result'][j]['value']['end'] += c

    # Line break sentence by sentence
    for (i, data_point) in enumerate(data):
        # data[i]["data"]["en_text"] =  data[i]["data"]["en_text"].replace(".\n", ".\n\n")

        data[i]["data"]["en_text"] =  data[i]["data"]["en_text"].replace(". ", ".\n\n")

        data[i]["data"]["vi_text"] = data[i]["data"]["vi_text"].replace(". ", ".\n\n")


def sat_re_label_sentence(json_path: str) -> pd.DataFrame:
    f = open(json_path)
    data = json.load(f)
    sat_sm = SaT("sat-12l-sm")

    # Updating start_index and end_index
    for (i, data_point) in enumerate(data):
        print(i)
        dummy = data[i]["data"]["en_text"]
        en_sents = sat_sm.split(dummy,strip_whitespace=True)
        dummy = "\n".join(en_sents)
        data[i]["data"]["en_text"] = dummy
        vi_sents = sat_sm.split(data[i]["data"]["vi_text"],strip_whitespace=True)
        vi_text = "\n".join(vi_sents)
        data[i]["data"]["vi_text"] = vi_text
        if len(en_sents) != len(vi_sents):
            print("Length mismatch between number of en and vi sentences:", i)


        for (j, labeling) in enumerate(data_point["predictions"][0]['result']):
            start_index = labeling['value']['start']
            # end_index = labeling['value']['end']
            temp = dummy[:start_index]
            c = temp.count(".\n")
            data[i]["predictions"][0]['result'][j]['value']['start'] += c
            data[i]["predictions"][0]['result'][j]['value']['end'] += c

    # Line break sentence by sentence
    for (i, data_point) in enumerate(data):
        # data[i]["data"]["en_text"] =  data[i]["data"]["en_text"].replace(".\n", ".\n\n")

        data[i]["data"]["en_text"] =  data[i]["data"]["en_text"].replace(".\n", ".\n\n")

        data[i]["data"]["vi_text"] = data[i]["data"]["vi_text"].replace(".\n", ".\n\n")

data = simple_re_label_sentence(json_path)
# data = sat_re_label_sentence(json_path)
# Change output path if relevant
out_path = "data/final_corpus_pubtator_output.json"

with open(out_path, "w") as outfile:
    json.dump(data, outfile, indent=2)

print("Split into sentences done!")