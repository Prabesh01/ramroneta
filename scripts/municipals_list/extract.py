import json

en_provinces = json.load(open('en.json'))
np_provinces = json.load(open('np.json'))

data= [] # [{"province_en":"","province_np":"",districts:[{"district_en":"","district_np":"","municipalities":[{"municipal_en":"","municipal_np":"","wards":0}]}]}]

did = 0
mid = 0
for en_province in en_provinces:
    np_province = next((item for item in np_provinces if item["id"] == en_province["id"]), None)
    province = {
        "name_en": en_province["name"],
        "name_np": np_province["name"],
        "districts": []
    }
    
    if isinstance(en_province["districts"], dict):
        en_districts_list = [d for _, d in en_province["districts"].items()]
    else:
        en_districts_list = en_province["districts"]

    if np_province and isinstance(np_province["districts"], dict):
        np_districts_list = [d for _, d in np_province["districts"].items()]
    else:
        np_districts_list = np_province["districts"] if np_province else []

    for en_district in en_districts_list:
        did += 1
        np_district = next((item for item in np_districts_list if item["id"] == en_district["id"]), None) if np_province else None
        district = {
            "id": did,
            "name_en": en_district["name"],
            "name_np": np_district["name"] if np_district else "",
            "municipalities": []
        }
        
        if isinstance(en_district["municipalities"], dict):
            en_municipalities_list = [m for _, m in en_district["municipalities"].items()]
        else:
            en_municipalities_list = en_district["municipalities"]

        if np_district and isinstance(np_district["municipalities"], dict):
            np_municipalities_list = [m for _, m in np_district["municipalities"].items()]
        else:
            np_municipalities_list = np_district["municipalities"] if np_district else []

        for en_municipal in en_municipalities_list:
            mid += 1
            np_municipal = next((item for item in np_municipalities_list if item["id"] == en_municipal["id"]), None) if np_district else None
            municipal = {
                "id": mid,
                "name_en": en_municipal["name"],
                "name_np": np_municipal["name"] if np_municipal else "",
                "wards": len(en_municipal["wards"])
            }
            district["municipalities"].append(municipal)
        
        province["districts"].append(district)
    
    data.append(province)

with open('municipalities.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)