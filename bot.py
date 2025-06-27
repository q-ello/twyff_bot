from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import json

BOT_TOKEN = "7102704601:AAGIikQy2RStt_x31IC-ulkt5AXY4gO8lmM"

songs_by_duration = {
    100: "I Just Want to Have Something to Do - Ramones",
    101: "All's Quiet on the Eastern Front - The Exploited",
    102: "She's a Sensation - The Buzzcocks",
    103: "Go Mental - Dead Kennedys",
    104: "Bad Brain - Bad Brains",
    105: "It's a Long Way Back - AC/DC",
    106: "Can't Get You Outta My Mind - Devo",
    107: "Rock 'n' Roll High School - The Runaways",
    108: "Wart Hog - The Stooges",
    109: "Mama's Boy - Suicidal Tendencies",
    110: "Stronger Than Death - Black Label Society",
    111: "Mental Hell - The Misfits",
    112: "Planet Earth 1988 - X-Ray Spex",
    113: "Human Kind - The Damned",
    114: "Ignorance Is Bliss - Agent Orange",
    115: "Come Back Baby - The Dictators",
    116: "Love Kills - The Circle Jerks",
    117: "Born to Die in Berlin - The Adverts",
    118: "Poison Heart - The Cramps",
    119: "Main Man - T. Rex",
    120: "Tomorrow She Goes Away - The Saints",
    121: "I Won't Let It Happen - The Jam",
    122: "Journey to the Center of the Mind - The Amboy Dukes",
    123: "Substitute - The Who",
    124: "Happy Jack - Small Faces",
    125: "Pictures of Lily - The Kinks",
    126: "The Seeker - Love",
    127: "Anyway, Anyhow, Anywhere - The Creation",
    128: "Circles - Captain Beefheart",
    129: "Armenian Genocide - System of a Down",
    130: "36 - Danzig",
    131: "Bounce - Iggy Pop",
    132: "Boom! - The Sonics",
    133: "Mind - Talking Heads",
    134: "Therapy - Infectious Grooves",
    135: "My Generation - Patti Smith",
    136: "I Can't Explain - The Zombies",
    137: "Pinball Wizard - The New York Dolls",
    138: "See Me, Feel Me - Blue Cheer",
    139: "I Can See for Miles - The Nazz",
    140: "Magic Bus - Sly & The Family Stone",
    141: "Call Me Lightning - The Pretty Things",
    142: "Legal Matter - The Action",
    143: "The Kids Are Alright - Generation X",
    144: "A Quick One While He's Away - The Easybeats",
    145: "Dogs - Nina Hagen",
    146: "Barracuda - Heart",
    147: "In the City - The Clash",
    148: "Bucket T - Jan and Dean",
    149: "Disguises - The Monks",
    150: "Blitzkrieg Bop - Ramones",
    151: "Song 2 - Blur",
    152: "Seven Nation Army - The White Stripes",
    153: "Come As You Are - Nirvana",
    154: "Pumped Up Kicks - Foster the People",
    155: "Wonderwall - Oasis",
    156: "Billie Jean - Michael Jackson",
    157: "Sweet Child O' Mine - Guns N' Roses",
    158: "Smells Like Teen Spirit - Nirvana",
    159: "Maps - Yeah Yeah Yeahs",
    160: "Let It Be - The Beatles",
    161: "Such Great Heights - The Postal Service",
    162: "Imagine - John Lennon",
    163: "Kids - MGMT",
    164: "1979 - The Smashing Pumpkins",
    165: "Thriller - Michael Jackson",
    166: "Time to Dance - The Sounds",
    167: "Ceremony - New Order",
    168: "Hey Jude - The Beatles",
    169: "Black No. 1 - Type O Negative",
    170: "Lose Yourself - Eminem",
    171: "Obstacle 1 - Interpol",
    172: "Mr. Brightside - The Killers",
    173: "Everlong - Foo Fighters",
    174: "Somebody That I Used to Know - Gotye",
    175: "The Funeral - Band of Horses",
    176: "Uptown Funk - Mark Ronson ft. Bruno Mars",
    177: "Holland, 1945 - Neutral Milk Hotel",
    178: "Shape of You - Ed Sheeran",
    179: "Sleepyhead - Passion Pit",
    180: "Africa - Toto",
    181: "Rebellion (Lies) - Arcade Fire",
    182: "Don't Stop Believin' - Journey",
    183: "In the Aeroplane Over the Sea - Neutral Milk Hotel",
    184: "The Suburbs - Arcade Fire",
    185: "Bohemian Rhapsody - Queen",
    186: "Lazy Eye - Silversun Pickups",
    187: "Banquet - Bloc Party",
    188: "Hotel California - Eagles",
    189: "Fell in Love with a Girl - The White Stripes",
    190: "Stairway to Heaven - Led Zeppelin",
    191: "The Modern Age - The Strokes",
    192: "Float On - Modest Mouse",
    193: "This Charming Man - The Smiths",
    194: "Neighborhood #1 (Tunnels) - Arcade Fire",
    195: "November Rain - Guns N' Roses",
    196: "Svefn-g-englar - Sigur Rós",
    197: "Pyramid Song - Radiohead",
    198: "Paradise City - Guns N' Roses",
    199: "Disorder - Joy Division",
    200: "Breathe Me - Sia",
    201: "One - Metallica",
    202: "Mad World - Gary Jules",
    203: "Skinny Love - Bon Iver",
    204: "The Scientist - Coldplay",
    205: "Nothing Else Matters - Metallica",
    206: "Hurt - Nine Inch Nails",
    207: "Teardrop - Massive Attack",
    208: "No One Knows - Queens of the Stone Age",
    209: "Karma Police - Radiohead",
    210: "Layla - Derek and the Dominos",
    211: "Exit Music (For a Film) - Radiohead",
    212: "The Sound of Silence - Simon & Garfunkel",
    213: "Fake Plastic Trees - Radiohead",
    214: "Black - Pearl Jam",
    215: "Free Bird - Lynyrd Skynyrd",
    216: "Paranoid Android - Radiohead",
    217: "Heroes - David Bowie",
    218: "Under the Bridge - Red Hot Chili Peppers",
    219: "Everlong - Foo Fighters",
    220: "Light My Fire - The Doors",
    221: "Wish You Were Here - Pink Floyd",
    222: "More Than a Feeling - Boston",
    223: "Hallelujah - Jeff Buckley",
    224: "In the Air Tonight - Phil Collins",
    225: "All Along the Watchtower - Jimi Hendrix",
    226: "Space Oddity - David Bowie",
    227: "Time - Pink Floyd",
    228: "While My Guitar Gently Weeps - The Beatles",
    229: "A Day in the Life - The Beatles",
    230: "Purple Rain - Prince",
    231: "Epitaph - King Crimson",
    232: "Us and Them - Pink Floyd",
    233: "Since I've Been Loving You - Led Zeppelin",
    234: "Riders on the Storm - The Doors",
    235: "Brain Damage/Eclipse - Pink Floyd",
    236: "Gimme Shelter - The Rolling Stones",
    237: "The Rain Song - Led Zeppelin",
    238: "Dogs - Pink Floyd",
    239: "Paranoid Android - Radiohead",
    240: "Bohemian Rhapsody - Queen",
    241: "Telegraph Road - Dire Straits",
    242: "2112 Overture - Rush",
    243: "Xanadu - Rush",
    244: "Starless - King Crimson",
    245: "Child in Time - Deep Purple",
    246: "The Trees - Rush",
    247: "Money - Pink Floyd",
    248: "Have a Cigar - Pink Floyd",
    249: "In My Time of Dying - Led Zeppelin",
    250: "Echoes - Pink Floyd",
    251: "Heart of the Sunrise - Yes",
    252: "The Court of the Crimson King - King Crimson",
    253: "Roundabout - Yes",
    254: "Locomotive Breath - Jethro Tull",
    255: "Kashmir - Led Zeppelin",
    256: "Achilles Last Stand - Led Zeppelin",
    257: "The Musical Box - Genesis",
    258: "Welcome to the Machine - Pink Floyd",
    259: "Atom Heart Mother - Pink Floyd",
    260: "The Revealing Science of God - Yes",
    261: "Baker Street - Gerry Rafferty",
    262: "Cortez the Killer - Neil Young",
    263: "The Weight - The Band",
    264: "Whipping Post - The Allman Brothers Band",
    265: "Green Grass and High Tides - The Outlaws",
    266: "Jessica - The Allman Brothers Band",
    267: "Europa - Santana",
    268: "Watermelon in Easter Hay - Frank Zappa",
    269: "Maggot Brain - Funkadelic",
    270: "A Cruel Angel's Thesis - Yoko Takahashi",
    271: "Shine On You Crazy Diamond Part I - Pink Floyd",
    272: "Dream On - Aerosmith",
    273: "Tuesday's Gone - Lynyrd Skynyrd",
    274: "Blue Sky - The Allman Brothers Band",
    275: "La Grange - ZZ Top",
    276: "Midnight Rider - The Allman Brothers Band",
    277: "Mississippi Queen - Mountain",
    278: "Born to Be Wild - Steppenwolf",
    279: "Smoke on the Water - Deep Purple",
    280: "Jesus of Suburbia - Green Day",
    281: "2112 Part II - Rush",
    282: "Cygnus X-1 - Rush",
    283: "Funeral for a Friend - Elton John",
    284: "Karn Evil 9 1st Impression - Emerson Lake & Palmer",
    285: "The End - The Doors",
    286: "When the Levee Breaks - Led Zeppelin",
    287: "Ten Years Gone - Led Zeppelin",
    288: "No Quarter - Led Zeppelin",
    289: "Dazed and Confused - Led Zeppelin",
    290: "In Memory of Elizabeth Reed - The Allman Brothers Band",
    291: "Roundabout - Yes",
    292: "Close to the Edge Part I - Yes",
    293: "And You and I - Yes",
    294: "Siberian Khatru - Yes",
    295: "Starship Trooper - Yes",
    296: "Long Distance Runaround - Yes",
    297: "The Gates of Delirium Part I - Yes",
    298: "Sound Chaser - Yes",
    299: "To Be Over - Yes",
    300: "Shine On You Crazy Diamond (Parts I-V) - Pink Floyd",
    301: "Welcome to the Machine - Pink Floyd",
    302: "Have a Cigar - Pink Floyd",
    303: "Wish You Were Here - Pink Floyd",
    304: "Shine On You Crazy Diamond Part VI - Pink Floyd",
    305: "Pigs (Three Different Ones) - Pink Floyd",
    306: "Dogs Part I - Pink Floyd",
    307: "Sheep - Pink Floyd",
    308: "Pigs on the Wing Part 2 - Pink Floyd",
    309: "In the Flesh? - Pink Floyd",
    310: "The Thin Ice - Pink Floyd",
    311: "Another Brick in the Wall Part 1 - Pink Floyd",
    312: "The Happiest Days of Our Lives - Pink Floyd",
    313: "Another Brick in the Wall Part 2 - Pink Floyd",
    314: "Mother - Pink Floyd",
    315: "Goodbye Blue Sky - Pink Floyd",
    316: "Empty Spaces - Pink Floyd",
    317: "Young Lust - Pink Floyd",
    318: "One of My Turns - Pink Floyd",
    319: "Don't Leave Me Now - Pink Floyd",
    320: "Another Brick in the Wall Part 3 - Pink Floyd",
    321: "Goodbye Cruel World - Pink Floyd",
    322: "Hey You - Pink Floyd",
    323: "Is There Anybody Out There? - Pink Floyd",
    324: "Nobody Home - Pink Floyd",
    325: "Vera - Pink Floyd",
    326: "Bring the Boys Back Home - Pink Floyd",
    327: "Comfortably Numb - Pink Floyd",
    328: "The Show Must Go On - Pink Floyd",
    329: "In the Flesh - Pink Floyd",
    330: "Run Like Hell - Pink Floyd",
    331: "Waiting for the Worms - Pink Floyd",
    332: "Stop - Pink Floyd",
    333: "The Trial - Pink Floyd",
    334: "Outside the Wall - Pink Floyd",
    335: "Thick as a Brick Part I - Jethro Tull",
    340: "Aqualung - Jethro Tull",
    345: "Locomotive Breath - Jethro Tull",
    350: "Cross-Eyed Mary - Jethro Tull",
    355: "Bohemian Rhapsody - Queen",
    360: "The Prophet's Song - Queen",
    365: "March of the Black Queen - Queen",
    370: "Innuendo - Queen",
    375: "Brighton Rock - Queen",
    380: "It's a Hard Life - Queen",
    385: "The Millionaire Waltz - Queen",
    390: "White Queen (As It Began) - Queen",
    391: "Hotel California - Eagles",
    395: "The Last Resort - Eagles",
    400: "Achilles Last Stand - Led Zeppelin",
    405: "Caravan - Led Zeppelin",
    410: "How Many More Times - Led Zeppelin",
    415: "Whole Lotta Love - Led Zeppelin",
    420: "In-A-Gadda-Da-Vida - Iron Butterfly",
    425: "Time Has Come Today - The Chambers Brothers",
    430: "Ball and Chain - Big Brother and the Holding Company",
    435: "East-West - The Paul Butterfield Blues Band",
    440: "Dark Star - Grateful Dead",
    445: "The Eleven - Grateful Dead",
    450: "St. Stephen - Grateful Dead",
    455: "China Cat Sunflower/I Know You Rider - Grateful Dead",
    460: "Playing in the Band - Grateful Dead",
    465: "Terrapin Station - Grateful Dead",
    470: "Help on the Way/Slipknot!/Franklin's Tower - Grateful Dead",
    475: "Fire on the Mountain - Grateful Dead",
    480: "Stairway to Heaven - Led Zeppelin",
    485: "Supper's Ready Part I - Genesis",
    490: "The Musical Box - Genesis",
    495: "The Return of the Giant Hogweed - Genesis",
    500: "The Fountain of Salmacis - Genesis",
    505: "The Knife - Genesis",
    510: "Trespass - Genesis",
    515: "Dancing with the Moonlit Knight - Genesis",
    520: "Firth of Fifth - Genesis",
    525: "The Battle of Epping Forest - Genesis",
    530: "The Cinema Show - Genesis",
    535: "In the Cage - Genesis",
    537: "November Rain - Guns N' Roses",
    540: "Estranged - Guns N' Roses",
    545: "Free Bird - Lynyrd Skynyrd",
    550: "Green Grass and High Tides - The Outlaws",
    555: "Jessica - The Allman Brothers Band",
    560: "Mountain Jam - The Allman Brothers Band",
    565: "Whipping Post - The Allman Brothers Band",
    570: "Elizabeth Reed - The Allman Brothers Band",
    575: "Dreams - The Allman Brothers Band",
    580: "Blue Sky - The Allman Brothers Band",
    585: "Les Brers in A Minor - The Allman Brothers Band",
    590: "Hot 'Lanta - The Allman Brothers Band",
    595: "You Don't Love Me - The Allman Brothers Band",
    600: "Soulshine - The Allman Brothers Band"
}

filename = 'userdata.json'

def update_user_data(userid, duration):
    try:
        userdata = {}

        #reading data
        try:
            with open(filename, 'r') as f:
                d = json.load(f)
                for key in d:
                    userdata[key] = d[key]
        except:
            pass

        #calculating data
        if userid not in userdata.keys():
            userdata[userid] = []
        
        if duration not in userdata[userid]:
            userdata[userid].append(duration)
        #writing data
        with open(filename, 'w') as f:
            json.dump(userdata, f)
        
        return len(userdata[userid])
    except:
        return -1

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message is None:
            return
        
        voice = update.message.voice
        if voice is None:
            return
        
        if update.effective_user is None:
            return
        
        sender = update.effective_user.first_name
        if update.message.forward_origin:
            await update.message.reply_text(f'{sender}, как не стыдно не просто пользоваться голосовыми, но ещё и пересылать их...')
            return

        duration = voice.duration
        print(f"Voice message duration: {duration}")

        file_size = voice.file_size
        
        sender_id = str(update.effective_user.id)

        format = 1 if duration % 10 == 1 and duration % 100 != 11 else 2 if duration % 10 < 5 and duration % 100 not in range(10, 15) else 5 

        if duration < 10:
            match format:
                case 1:
                    ending = 'a'
                case 2:
                    ending = 'ы'
                case 5:
                    ending = ''
            roast = f"Всего лишь {duration} секунд{ending}? Да, {sender}, ну это можно было и ручками написать"
        elif duration in songs_by_duration.keys():
            songs_count = -1
            if sender_id:
                songs_count = update_user_data(sender_id, duration)
            roast = f"Мы получили голосовое сообщение от {sender}.\nЗа время этого сообщения мы бы могли послушать целую песню {songs_by_duration[duration]} \
({songs_count}/{len(songs_by_duration)}).\n\nВремя задуматься."
        else:
            ending = ['ых', '']
            match format:
                case 1:
                    ending = ['ую', 'у']
                case 1:
                    ending = ['ые', 'ы']
                case 1:
                    ending = ['ых', '']

            roast = f"Мы получили цел{ending[0]} {duration} секунд{ending[1]} аудио от {sender}.\nЭто примерно {((file_size if file_size else 0)/1024):.1f} Кб абсолютно ненужных нам данных.\n👏👏👏"
        await update.message.reply_text(roast)
    except Exception as e:
        print(repr(e))

def get_unlocked_songs(userid):
    try:
        userdata = []
        print(userid)
        with open(filename, 'r') as f:
                d = json.load(f)
                if userid in d.keys():
                    userdata = d[userid]
        return userdata
    except Exception as e:
        print(repr(e))
        return []

async def see_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user is None:
            return
        if update.message is None:
            return
        
        sender_id = str(update.effective_user.id)
        unlocked_songs = get_unlocked_songs(sender_id)
        answer = ""
        if len(unlocked_songs) == 0:
            answer = "Тобой пока не было ничего разблокировано."
            await update.message.reply_text(answer)
        else:
            answer = f"Песен разблокировано: {len(unlocked_songs)}/{len(songs_by_duration)}\n\n"
            for i in range(len(unlocked_songs)):
                new_chunk = f'{i+1}. {songs_by_duration[unlocked_songs[i]]} - {unlocked_songs[i]}с\n'
                if len(answer + new_chunk) >= 4096:
                    await update.message.reply_text(answer)
                    answer = ''
                answer += new_chunk
            if answer != '':
                await update.message.reply_text(answer)
        
    except Exception as e:
        print(repr(e))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(CommandHandler("stats", see_stats))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
