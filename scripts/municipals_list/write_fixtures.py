import json

provinces = json.load(open('municipalities.json', 'r', encoding='utf-8'))

did = 0
mid = 0
district_fixtures = []
municipality_fixtures = []
for province in provinces:
    for district in province['districts']:
        did += 1
        district_data = {
            "model": "app.district",
            "pk": did,
            "fields": {
                "name": district['name_en'],
                "name_np": district['name_np']
            }
        }
        district_fixtures.append(district_data)

        for municipality in district['municipalities']:
            mid += 1
            municipality_data = {
                "model": "app.municipality",
                "pk": mid,
                "fields": {
                    "name": municipality['name_en'],
                    "name_np": municipality['name_np'],
                    "district": did,
                    "wards": municipality['wards']
                }
            }
            municipality_fixtures.append(municipality_data)

with open('district_fixtures.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(district_fixtures, ensure_ascii=False) + '\n')

with open('municipal_fixtures.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(municipality_fixtures, ensure_ascii=False) + '\n')
