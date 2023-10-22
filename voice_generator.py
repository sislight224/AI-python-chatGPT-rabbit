import fakeyou
import os
from uuid import uuid4
import time
simpsons_dict = {
    'Abraham Simpson': 'TM:byzk08rq9g0y',
    'Abe Simpson': 'TM:byzk08rq9g0y',

    'Agnes Skinner': 'TM:zar729c189ev',
    'Agnes': 'TM:zar729c189ev',

    'Apu Nahasapeemapetilon': 'TM:dz97wz0jjbfv',
    'Apu': 'TM:dz97wz0jjbfv',

    'Barney Gumble': 'TM:xnqgv6jgh9ew',
    'Barney': 'TM:xnqgv6jgh9ew',

    'Bart Simpson': 'TM:jm8h9gc59qxe',
    'Bart': 'TM:jm8h9gc59qxe',

    'Blue Haired Lawyer': 'TM:h1bg48cckwgz',
    'Blue Lawyer': 'TM:h1bg48cckwgz',

    'Carl Carlson': 'TM:q9x66em0grj7',
    'Carl': 'TM:q9x66em0grj7',

    'Chief Wiggum': 'TM:3y454grm2yxh',
    'Wiggum': 'TM:3y454grm2yxh',

    'Cletus Spuckler': 'TM:m3218ajs841r',
    'Cletus': 'TM:m3218ajs841r',

    'Comic Book Guy': 'TM:1tesjbz0b2ng',

    'Dolph Starbeam': 'TM:rqdp1me0j7mp',
    'Dolph': 'TM:rqdp1me0j7mp',

    'Dr. Julius Hibbert': 'TM:akskqggffy3w',
    'Dr. Hibbert': 'TM:akskqggffy3w',

    'Frank Grimes': 'TM:naswfpxcfz1m',
    'Grimes': 'TM:naswfpxcfz1m',

    'Gil Gunderson': 'TM:1ceapwagaxgc',
    'Gil': 'TM:1ceapwagaxgc',

    'Groundskeeper Willie': 'TM:5x7fg761v5ym',
    'Willie': 'TM:5x7fg761v5ym',

    'Homer Simpson': 'TM:dy1tchfdhcwf',
    'Homer': 'TM:dy1tchfdhcwf',

    'Horatio McAllister': 'TM:b7zca7vtcgvz',
    'Sea Captain': 'TM:b7zca7vtcgvz',
    'McAllister': 'TM:b7zca7vtcgvz',

    'Itchy': 'TM:ceygxdqz1yta',

    'Jasper Beardsley': 'TM:6vc84yjdpez7',
    'Jasper': 'TM:6vc84yjdpez7',

    'Jimbo Jones': 'TM:g0wv1rzs8fx8',
    'Jimbo': 'TM:g0wv1rzs8fx8',

    'Joe Quimby': 'TM:tqp9cmxa5vm1',
    'Quimby': 'TM:tqp9cmxa5vm1',

    'Kang': 'TM:nbt0f3k5ye3b',

    'Kent Brockman': 'TM:9d3n3x1bgkfp',
    'Brockman': 'TM:9d3n3x1bgkfp',

    'Kirk Van Houten': 'TM:dfqe7xyx6w6m',
    'Kirk': 'TM:dfqe7xyx6w6m',

    'Kodos': 'TM:3e9c806avgqb',

    'Krusty the Clown': 'TM:37ajh00wpmrv',
    'Krusty': 'TM:37ajh00wpmrv',

    'Lenny Leonard': 'TM:rc2cxbrkhvrs',
    'Lenny': 'TM:rc2cxbrkhvrs',

    'McBain': 'TM:0zdq7sjfjjva',
    'Rainier Wolfcastle': 'TM:0zdq7sjfjjva',
    'Wolfcastle': 'TM:0zdq7sjfjjva',

    'Moe Szyslak': 'TM:9fsxfcmpg448',
    'Moe': 'TM:9fsxfcmpg448',

    'Mr. Burns': 'TM:zj2x6094n6bd',
    'Burns': 'TM:zj2x6094n6bd',

    'Ned Flanders': 'TM:dn7m102edhqt',
    'Ned': 'TM:dn7m102edhqt',

    'Nelson Muntz': 'TM:jz440z5wgr79',
    'Nelson': 'TM:jz440z5wgr79',

    'Old Jewish Man': 'TM:e5w29s16avag',

    'Otto Mann': 'TM:kjyqqa3dq0cv',
    'Otto': 'TM:kjyqqa3dq0cv',

    'Patty Bouvier': 'TM:34a7gj7hv7rn',
    'Selma Bouvier': 'TM:34a7gj7hv7rn',
    'Patty and Selma': 'TM:34a7gj7hv7rn',

    'Professor Frink': 'TM:pzj5zs043e0t',
    'Frink': 'TM:pzj5zs043e0t',

    'Ralph Wiggum': 'TM:3c2kasdavn4s',
    'Ralph': 'TM:3c2kasdavn4s',

    'Reverend Lovejoy': 'TM:ffcq44jvrkch',
    'Lovejoy': 'TM:ffcq44jvrkch',

    'Rich Texan': 'TM:mhf0qh3zf896',

    'Scratchy': 'TM:8sxdn5msfygw',

    'Principal Seymour Skinner': 'TM:9csk7t7gbwr7',
    'Seymour Skinner': 'TM:9csk7t7gbwr7',
    'Skinner': 'TM:9csk7t7gbwr7',

    'Sherry and Terri': 'TM:z77n1e41y988',
    'Sherry': 'TM:z77n1e41y988',
    'Terri': 'TM:z77n1e41y988',

    'Squeaky Voice Teen': 'TM:jg2rtjgt945j',
    'Squeaky Teen': 'TM:jg2rtjgt945j',

    'Superintendent Chalmers': 'TM:0js70zb5p6z4',
    'Chalmers': 'TM:0js70zb5p6z4',

    'Todd Flanders': 'TM:m5e9w7h6vbs6',
    'Rod Flanders': 'TM:m5e9w7h6vbs6',
    'Todd and Rod': 'TM:m5e9w7h6vbs6',

    'Troy McClure': 'TM:g4n5d6z4wxdy',
    'McClure': 'TM:g4n5d6z4wxdy',

    'Waylon Smithers': 'TM:0d4h1s8y8g0z',
    'Smithers': 'TM:0d4h1s8y8g0z',

    'Marge Simpson': 'TM:jg2rtjgt945j',
    'Marge': 'TM:jg2rtjgt945j',

    'Lisa Simpson': 'TM:jg2rtjgt945j',
    'Lisa': 'TM:jg2rtjgt945j',

    'Milhouse Van Houten': 'TM:jg2rtjgt945j',
    'Milhouse': 'TM:jg2rtjgt945j'
}






def generate_voice_files(lines_result, characters_to_use, prompt, save=False):
    # {'category_token': 'CAT:377189hqsbz', 'maybe_super_category_token': 'CAT:0aezw83sdnp',
    # 'model_type': 'tts', 'name': 'The Simpsons', 'name_for_dropdown': 'Simpsons', 'can_directly_have_models': True,
    # 'can_have_subcategories': False, 'can_only_mods_apply': False, 'is_mod_approved': True, 'is_synthetic': False,
    # 'should_be_sorted': True, 'created_at': '2022-01-06T08:50:20Z', 'updated_at': '2022-01-06T08:51:23Z',
    # 'deleted_at': None}
    fy = fakeyou.fakeyou.FakeYou()
    fy.login(username="Team@watchai.live", password="Watchai!")
    folder_loc = f"voices/{prompt}_{uuid4()}"
    if save:
        os.mkdir(folder_loc)
    # voices_list = fy.get_voices_by_category(categoryToken="CAT:377189hqsbz").json
    for i in lines_result:
        print(f"Generating voice file for: {list(i.items())[0][0]}: {list(i.items())[0][1]}")
        try:
            line = fy.say(text=list(i.items())[0][1], ttsModelToken=simpsons_dict[list(i.items())[0][0]])
            if save:
                line_path = f"{folder_loc}/{uuid4()}.wav"
                line.save(line_path)
                i["sound_path"] = line_path
            i["sound_bytearray"] = line.content
        except Exception as e1:
            try:
                print(f"Sound generation error: {e1}. \nWait three seconds and try again...")
                time.sleep(3)
                line = fy.say(text=list(i.items())[0][1], ttsModelToken=simpsons_dict[list(i.items())[0][0]])
                if save:
                    line_path = f"{folder_loc}/{uuid4()}.wav"
                    line.save(line_path)
                    i["sound_path"] = line_path
                i["sound_bytearray"] = line.content
            except Exception as e2:
                print(f"Sound generation error final: {e2}. \nWill assume no sound for this.")
                i["sound_bytearray"] = ""
                continue
                # todo: add logging
    return [i for i in lines_result if "sound_bytearray" in i]


    # get voices from lines
