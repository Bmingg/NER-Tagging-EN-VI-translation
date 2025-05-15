import json
import pandas as pd

# path to the json data file
json_path = "data/20250509_corpus_pubtator_output.json"
# path to the en-vn translation excel file
xlsx_path = "data/translate_all_output.xlsx"

def map_vi_text(json_path: str, xlsx_path: str) -> pd.DataFrame:

    f = open(json_path)
    data = json.load(f)

# Needs openpyxl library !pip install openpyxl
    try:
        vi_data = pd.read_excel(xlsx_path)
    except:
        raise Exception("Needs openpyxl library. If relevant, do pip install openpyxl")


    # Concat vietnamese title and abstract 
    def get_vi_text(data: pd.DataFrame):
        temp = data["vi_title"] + '. ' + data["vi_abstract"]
        return temp
        
    vi_texts = vi_data.apply(get_vi_text, axis=1)

    # Random check
    assert len(vi_texts) == len(data), "length mismatch"

    # Change current key names and map vietnamese data

    for (i, data_point) in enumerate(data):
        # Change key name from "text" to "en_text"
        data[i]["data"]["en_text"] =  data[i]["data"].pop("text")

        # Map vietnamese text to the data: "vi_text"
        data[i]["data"]["vi_text"] = vi_texts[i]

        # Change tagging target
        # 'from_name': 'label' --> 'en_label'
        # 'to_name': 'en_text'
        for (j, labeling) in enumerate(data_point["predictions"][0]['result']):
            data[i]["predictions"][0]['result'][j]['from_name'] = "en_label"
            data[i]["predictions"][0]['result'][j]['to_name'] = "en_text"

data = map_vi_text(json_path, xlsx_path)

# Change output path if relevant
out_path = "data/updated_corpus_pubtator_output.json"

with open(out_path, "w") as outfile:
    json.dump(data, outfile, indent=2)

print("Mapping vi texts is done!")