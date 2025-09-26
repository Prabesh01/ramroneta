out="""<div class="province">
    <button class="province-btn" onclick="toggleProvince(this)">Koshi Province<i class="fas fa-chevron-down"></i></button>

    <div class="province-content">
        <div class="districts-container">
"""

map_replace = {
    "EASTERN RUKUM":"RUKUM_E",
    "WESTERN RUKUM":"RUKUM_W",
    "NAWALPARASI BARDAGHAT SUSTA EAST":"NAWALPARASI_E",
    "NAWALPARASI BARDAGHAT SUSTA WEST":"NAWALPARASI_W"
}

def make_html(province, district,constituencies,brk=False):
    global out
    map_name = district
    if district in map_replace:
        map_name = map_replace[district]
    if brk:
        out+=f"""
        </div>
    </div>
</div>
<div class="province">
    <button class="province-btn" onclick="toggleProvince(this)">{province} Province<i class="fas fa-chevron-down"></i></button>

    <div class="province-content">
        <div class="districts-container">
        """        
    out += f"""
            <div class="district">
                <button class="district-btn" onclick="toggleDistrict(this)">{district.title()}<i class="fas fa-chevron-down"></i></button>
                <div class="district-content">
                    <div class="constituencies-container">
                        <a href="/uploads/maps/{map_name}.pdf" target="_blank" class="map-link">🗺️ View Map</a>
                        <ul class="constituency-list">"""
    for cons in constituencies:
        out += f'''
                            <li class="constituency-item"><a href="/hor/{{{{year}}}}/constituency/{cons}/1">{cons.title().replace('_','-')}</a></li>'''
    out += """
                        </ul>
                    </div>
                </div>
            </div>"""

lines=open('hor.txt').readlines()

district = "TAPLEJUNG"
constituencies=[]
province_idx=0
provinces=['Koshi','Madhesh','Bagmati','Gandaki','Lumbini','Karnali','Sudurpaschim']
for line in lines:
    brk=False
    txt = line.split('=')[0].strip()
    if txt.startswith(district.replace(' ','_')):
        constituencies.append(txt)
    else:
        if district in ['SAPTARI','DOLAKHA','GORKHA','GULMI','SALYAN','BAJURA']: 
            province_idx+=1
            brk=True
        make_html(provinces[province_idx], district,constituencies,brk)
        district=' '.join(txt.split('_')[:-1]).strip()
        constituencies=[txt]

out+="""
        </div>
    </div>
</div>
"""

with open('hor.html','w') as f: f.write(out)
