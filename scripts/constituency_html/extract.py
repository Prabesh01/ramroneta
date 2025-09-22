out="""<div class="province">
    <button class="province-btn" onclick="toggleProvince(this)">Koshi Province<i class="fas fa-chevron-down"></i></button>

    <div class="province-content">
        <div class="districts-container">
"""

def make_html(district,constituencies,brk=False):
    global out
    if brk:
        out+="""
        </div>
    </div>
</div>
<div class="province">
    <button class="province-btn" onclick="toggleProvince(this)">Province<i class="fas fa-chevron-down"></i></button>

    <div class="province-content">
        <div class="districts-container">
        """        
    out += f"""
            <div class="district">
                <button class="district-btn" onclick="toggleDistrict(this)">{district.title()}<i class="fas fa-chevron-down"></i></button>
                <div class="district-content">
                    <div class="constituencies-container">
                        <ul class="constituency-list">"""
    for cons in constituencies:
        out += f'''
                            <li class="constituency-item"><a href="/hor/{{{{year}}}}/constituency/{cons}/list">{cons.title().replace('_','-')}</a></li>'''
    out += """
                        </ul>
                    </div>
                </div>
            </div>"""

lines=open('hor.txt').readlines()

district = "TAPLEJUNG"
constituencies=[]
for line in lines:
    brk=False
    txt = line.split('=')[0].strip()
    if txt.startswith(district.replace(' ','_')):
        constituencies.append(txt)
    else:
        if district in ['SAPTARI','DOLAKHA','GORKHA','GULMI','SALYAN','BAJURA']: brk=True
        make_html(district,constituencies,brk)
        district=' '.join(txt.split('_')[:-1]).strip()
        constituencies=[txt]

out+="""
        </div>
    </div>
</div>
"""

with open('hor.html','w') as f: f.write(out)
