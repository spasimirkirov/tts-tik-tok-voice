from enum import Enum

# Enum to define available voices for text-to-speech conversion
class Voice(Enum):
    # DISNEY VOICES
    GHOSTFACE = 'en_us_ghostface'
    CHEWBACCA = 'en_us_chewbacca'
    C3PO = 'en_us_c3po'
    STITCH = 'en_us_stitch'
    STORMTROOPER = 'en_us_stormtrooper'
    ROCKET = 'en_us_rocket'
    MADAME_LEOTA = 'en_female_madam_leota'
    GHOST_HOST = 'en_male_ghosthost'
    PIRATE = 'en_male_pirate'

    # ENGLISH VOICES
    AU_FEMALE_1 = 'en_au_001'
    AU_MALE_1 = 'en_au_002'
    UK_MALE_1 = 'en_uk_001'
    UK_MALE_2 = 'en_uk_003'
    US_FEMALE_1 = 'en_us_001'
    US_FEMALE_2 = 'en_us_002'
    US_MALE_1 = 'en_us_006'
    US_MALE_2 = 'en_us_007'
    US_MALE_3 = 'en_us_009'
    US_MALE_4 = 'en_us_010'
    MALE_JOMBOY = 'en_male_jomboy'
    MALE_CODY = 'en_male_cody'
    FEMALE_SAMC = 'en_female_samc'
    FEMALE_MAKEUP = 'en_female_makeup'
    FEMALE_RICHGIRL = 'en_female_richgirl'
    MALE_GRINCH = 'en_male_grinch'
    MALE_DEADPOOL = 'en_male_deadpool'
    MALE_JARVIS = 'en_male_jarvis'
    MALE_ASHMAGIC = 'en_male_ashmagic'
    MALE_OLANTERKKERS = 'en_male_olantekkers'
    MALE_UKNEIGHBOR = 'en_male_ukneighbor'
    MALE_UKBUTLER = 'en_male_ukbutler'
    FEMALE_SHENNA = 'en_female_shenna'
    FEMALE_PANSINO = 'en_female_pansino'
    MALE_TREVOR = 'en_male_trevor'
    FEMALE_BETTY = 'en_female_betty'
    MALE_CUPID = 'en_male_cupid'
    FEMALE_GRANDMA = 'en_female_grandma'
    MALE_XMXS_CHRISTMAS = 'en_male_m2_xhxs_m03_christmas'
    MALE_SANTA_NARRATION = 'en_male_santa_narration'
    MALE_SING_DEEP_JINGLE = 'en_male_sing_deep_jingle'
    MALE_SANTA_EFFECT = 'en_male_santa_effect'
    FEMALE_HT_NEYEAR = 'en_female_ht_f08_newyear'
    MALE_WIZARD = 'en_male_wizard'
    FEMALE_HT_HALLOWEEN = 'en_female_ht_f08_halloween'

    # EUROPE VOICES
    FR_MALE_1 = 'fr_001'
    FR_MALE_2 = 'fr_002'
    DE_FEMALE = 'de_001'
    DE_MALE = 'de_002'
    ES_MALE = 'es_002'
    
    # AMERICA VOICES
    ES_MX_MALE = 'es_mx_002'
    BR_FEMALE_1 = 'br_001'
    BR_FEMALE_2 = 'br_003'
    BR_FEMALE_3 = 'br_004'
    BR_MALE = 'br_005'
    BP_FEMALE_IVETE = 'bp_female_ivete'
    BP_FEMALE_LUDMILLA = 'bp_female_ludmilla'
    PT_FEMALE_LHAYS = 'pt_female_lhays'
    PT_FEMALE_LAIZZA = 'pt_female_laizza'
    PT_MALE_BUENO = 'pt_male_bueno'

    # ASIA VOICES
    ID_FEMALE = 'id_001'
    JP_FEMALE_1 = 'jp_001'
    JP_FEMALE_2 = 'jp_003'
    JP_FEMALE_3 = 'jp_005'
    JP_MALE = 'jp_006'
    KR_MALE_1 = 'kr_002'
    KR_FEMALE = 'kr_003'
    KR_MALE_2 = 'kr_004'
    JP_FEMALE_FUJICOCHAN = 'jp_female_fujicochan'
    JP_FEMALE_HASEGAWARIONA = 'jp_female_hasegawariona'
    JP_MALE_KEIICHINAKANO = 'jp_male_keiichinakano'
    JP_FEMALE_OOMAEAIIKA = 'jp_female_oomaeaika'
    JP_MALE_YUJINCHIGUSA = 'jp_male_yujinchigusa'
    JP_FEMALE_SHIROU = 'jp_female_shirou'
    JP_MALE_TAMAWAKAZUKI = 'jp_male_tamawakazuki'
    JP_FEMALE_KAORISHOJI = 'jp_female_kaorishoji'
    JP_FEMALE_YAGISHAKI = 'jp_female_yagishaki'
    JP_MALE_HIKAKIN = 'jp_male_hikakin'
    JP_FEMALE_REI = 'jp_female_rei'
    JP_MALE_SHUICHIRO = 'jp_male_shuichiro'
    JP_MALE_MATSUDAKE = 'jp_male_matsudake'
    JP_FEMALE_MACHIKORIIITA = 'jp_female_machikoriiita'
    JP_MALE_MATSUO = 'jp_male_matsuo'
    JP_MALE_OSADA = 'jp_male_osada'

    # SINGING VOICES
    SING_FEMALE_ALTO = 'en_female_f08_salut_damour'
    SING_MALE_TENOR = 'en_male_m03_lobby'
    SING_FEMALE_WARMY_BREEZE = 'en_female_f08_warmy_breeze'
    SING_MALE_SUNSHINE_SOON = 'en_male_m03_sunshine_soon'
    SING_FEMALE_GLORIOUS = 'en_female_ht_f08_glorious'
    SING_MALE_IT_GOES_UP = 'en_male_sing_funny_it_goes_up'
    SING_MALE_CHIPMUNK = 'en_male_m2_xhxs_m03_silly'
    SING_FEMALE_WONDERFUL_WORLD = 'en_female_ht_f08_wonderful_world'
    SING_MALE_FUNNY_THANKSGIVING = 'en_male_sing_funny_thanksgiving'

    # OTHER
    MALE_NARRATION = 'en_male_narration'
    MALE_FUNNY = 'en_male_funny'
    FEMALE_EMOTIONAL = 'en_female_emotional'

    # Function to check if a string matches any enum member name
    @staticmethod
    def from_string(input_string: str):
        # Iterate over all enum members
        for voice in Voice:
            if voice.name == input_string:
                return voice
        return None


VOICE_CATEGORIES = {
    'DISNEY': [
        Voice.GHOSTFACE,
        Voice.CHEWBACCA,
        Voice.C3PO,
        Voice.STITCH,
        Voice.STORMTROOPER,
        Voice.ROCKET,
        Voice.MADAME_LEOTA,
        Voice.GHOST_HOST,
        Voice.PIRATE,
    ],
    'ENGLISH': [
        Voice.AU_FEMALE_1,
        Voice.AU_MALE_1,
        Voice.UK_MALE_1,
        Voice.UK_MALE_2,
        Voice.US_FEMALE_1,
        Voice.US_FEMALE_2,
        Voice.US_MALE_1,
        Voice.US_MALE_2,
        Voice.US_MALE_3,
        Voice.US_MALE_4,
        Voice.MALE_JOMBOY,
        Voice.MALE_CODY,
        Voice.FEMALE_SAMC,
        Voice.FEMALE_MAKEUP,
        Voice.FEMALE_RICHGIRL,
        Voice.MALE_GRINCH,
        Voice.MALE_DEADPOOL,
        Voice.MALE_JARVIS,
        Voice.MALE_ASHMAGIC,
        Voice.MALE_OLANTERKKERS,
        Voice.MALE_UKNEIGHBOR,
        Voice.MALE_UKBUTLER,
        Voice.FEMALE_SHENNA,
        Voice.FEMALE_PANSINO,
        Voice.MALE_TREVOR,
        Voice.FEMALE_BETTY,
        Voice.MALE_CUPID,
        Voice.FEMALE_GRANDMA,
        Voice.MALE_XMXS_CHRISTMAS,
        Voice.MALE_SANTA_NARRATION,
        Voice.MALE_SING_DEEP_JINGLE,
        Voice.MALE_SANTA_EFFECT,
        Voice.FEMALE_HT_NEYEAR,
        Voice.MALE_WIZARD,
        Voice.FEMALE_HT_HALLOWEEN,
    ],
    'EUROPE': [
        Voice.FR_MALE_1,
        Voice.FR_MALE_2,
        Voice.DE_FEMALE,
        Voice.DE_MALE,
        Voice.ES_MALE,
    ],
    'AMERICA': [
        Voice.ES_MX_MALE,
        Voice.BR_FEMALE_1,
        Voice.BR_FEMALE_2,
        Voice.BR_FEMALE_3,
        Voice.BR_MALE,
        Voice.BP_FEMALE_IVETE,
        Voice.BP_FEMALE_LUDMILLA,
        Voice.PT_FEMALE_LHAYS,
        Voice.PT_FEMALE_LAIZZA,
        Voice.PT_MALE_BUENO,
    ],
    'ASIA': [
        Voice.ID_FEMALE,
        Voice.JP_FEMALE_1,
        Voice.JP_FEMALE_2,
        Voice.JP_FEMALE_3,
        Voice.JP_MALE,
        Voice.KR_MALE_1,
        Voice.KR_FEMALE,
        Voice.KR_MALE_2,
        Voice.JP_FEMALE_FUJICOCHAN,
        Voice.JP_FEMALE_HASEGAWARIONA,
        Voice.JP_MALE_KEIICHINAKANO,
        Voice.JP_FEMALE_OOMAEAIIKA,
        Voice.JP_MALE_YUJINCHIGUSA,
        Voice.JP_FEMALE_SHIROU,
        Voice.JP_MALE_TAMAWAKAZUKI,
        Voice.JP_FEMALE_KAORISHOJI,
        Voice.JP_FEMALE_YAGISHAKI,
        Voice.JP_MALE_HIKAKIN,
        Voice.JP_FEMALE_REI,
        Voice.JP_MALE_SHUICHIRO,
        Voice.JP_MALE_MATSUDAKE,
        Voice.JP_FEMALE_MACHIKORIIITA,
        Voice.JP_MALE_MATSUO,
        Voice.JP_MALE_OSADA,
    ],
    'SINGING': [
        Voice.SING_FEMALE_ALTO,
        Voice.SING_MALE_TENOR,
        Voice.SING_FEMALE_WARMY_BREEZE,
        Voice.SING_MALE_SUNSHINE_SOON,
        Voice.SING_FEMALE_GLORIOUS,
        Voice.SING_MALE_IT_GOES_UP,
        Voice.SING_MALE_CHIPMUNK,
        Voice.SING_FEMALE_WONDERFUL_WORLD,
        Voice.SING_MALE_FUNNY_THANKSGIVING,
    ],
    'OTHER': [
        Voice.MALE_NARRATION,
        Voice.MALE_FUNNY,
        Voice.FEMALE_EMOTIONAL,
    ],
}


def voices_payload() -> dict:
    categorized_voices = []
    for category, voices in VOICE_CATEGORIES.items():
        categorized_voices.append({
            'category': category,
            'voices': [
                {
                    'name': voice.name,
                    'id': voice.value,
                }
                for voice in voices
            ],
        })

    return {
        'totalVoices': len(list(Voice)),
        'categories': categorized_voices,
        'flat': [
            {
                'name': voice.name,
                'id': voice.value,
                'category': next(
                    (category for category, voices in VOICE_CATEGORIES.items() if voice in voices),
                    'UNCATEGORIZED',
                ),
            }
            for voice in Voice
        ],
    }
