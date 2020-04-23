# -*- coding: utf-8 -*-


import re
from django_user_agents.utils import get_user_agent
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from operator import itemgetter

class ParseRequest:

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]

    alphabet_en = [",", ".","the", "and", "or", "of", "from", "at", "it", "you", "we", "he", "she", "how", "am", "using", "use",
             "know", "with", "into", "value"
                , "to", "all", "is", "on", "off", "they", "because", "between", "does", "an", "about", "above", "after",
             "again", "against", "any", "are", "as not",
             "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "if", "else", "further",
             "had", "has", "have", "having", "her", "here", "hers", "herself", "him",
             "himself", "his", "in", "itself", "me", "more", "most", "my", "myself", "no", "nor", "not", "once", "only",
             "other", "ought", "our", "ours", "ourselves", "out", "over",
             "own", "same", "should", "so", "some", "such", "than", "that", "their", "theirs", "theme", "themselves",
             "then", "there", "these", "they", "this", "those", "through", "too",
             "under", "until", "since", "up", "very", "was", "which", "while", "who", "whom", "why", "would", "your",
             "yours", "yourself", "yourselves"
             ]

    alphabet_fr = [",", ".", "bonjour", "bonsoir", "aujourd'hui", "soir", "matin", "à", "ç", "de", "et", "dans", "quoi", "est", "la", "le", "un", "une", "des", "aux", "au", "ou", "oû",
             "par", "va", "ont", "êtes", "sur", "pas", "tous", "plusieurs", "vers", "aller",
             "ai", "aie", "aient", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "as", "alors", "aucun",
             "aura", "aurai", "auraient", "aurais", "aurait", "autre", "avaient", "avais", "avait", "avant", "avec",
             "avez", "aviez", "avions", "avoir", "avons", "ayant", "ayez", "ayons", "bon", "car", "ce", "ceci", "cela",
             "ces", "cet", "cette", "ceux", "chaque", "ci", "comme", "comment", "dedans", "dehors",
             "depuis", "deux", "devoir", "devrait", "devrez", "devriez", "devrions", "devrons", "devront", "dois",
             "doit", "dons", "dos", "droite", "du", "elle", "elles", "en", "encore", "es", "est", "eu", "eue",
             "eues", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "faire",
             "fais", "faisez", "fait", "faites", "fois", "font", "force", "furent", "fus", "fusse",
             "fussent", "fusses", "fussiez", "fussions", "fut", "haut", "hors", "ici",
             "il", "ils", "je", "juste", "les", "leur", "leurs", "lui", "ma", "maintenant", "mais", "me", "mes", "moi",
             "moins", "mon", "mot", "ne", "ni", "nom", "nos", "nomm", "notre",
             "nous", "nouveau", "nouveaux", "ont", "parce", "parole", "personne", "personnes", "peu", "peut", "plupart",
             "pour", "pourquoi", "qu", "quand",
             "que", "quel", "quelle", "quelles", "quels", "qui", "sa", "sans", "se", "sera", "serai", "seraient",
             "serais", "serait", "seras", "serez", "seriez", "serions",
             "serons", "seront", "ses", "seulement", "si", "sien", "soi",
             "soi", "soient", "sois", "soit", "sommes", "son", "sont", "sous", "soyez", "soyons", "suis", "sujet", "ta",
             "tandis", "te", "tellement", "tels", "tes", "toi", "ton", "tout", "trop",
             "tu", "valeur", "voient",
             "vois", "voit", "vont", "vos", "votre", "vous", "vu"
             ]

    alphabet_ar = ["ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ",
                   "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ء", "آ", "ٱ", "أ", "إ", "ة", "ؤ", "ئ", "ى"]


    def parse(self, request):
        browser = "Unknown"
        user_agent = request.META["HTTP_USER_AGENT"]

        if user_agent.find("Opera") > -1 or user_agent.find("OPR") > -1:
            browser = "Opera"

        if user_agent.find("Edge") > -1:
            browser = "ie Edge"

        if user_agent.find("MSIE") > -1 or user_agent.find("Trident/") > -1:
            browser = "ie"

        if user_agent.find("Chrome") > -1 and browser == "":
            browser = "Chrome"

        if user_agent.find("Safari") > -1 and browser == "":
            browser = "Safari"

        if user_agent.find("Firefox") > -1:
            browser = "Firefox"

        os = "Unknown"
        clientStrings = [
            {'s': 'Windows 10', 'r': re.findall("(Windows 10.0|Windows NT 10.0)", user_agent)},
            {'s': 'Windows 8.1', 'r': re.findall("(Windows 8.1|Windows NT 6.3)", user_agent)},
            {'s': 'Windows 8', 'r': re.findall("(Windows 8|Windows NT 6.2)", user_agent)},
            {'s': 'Windows 7', 'r': re.findall("(Windows 7|Windows NT 6.1)", user_agent)},
            {'s': 'Windows Vista', 'r': re.findall("Windows NT 6.0", user_agent)},
            {'s': 'Windows Server 2003', 'r': re.findall("Windows NT 5.2", user_agent)},
            {'s': 'Windows XP', 'r': re.findall("(Windows NT 5.1|Windows XP)", user_agent)},
            {'s': 'Windows 2000', 'r': re.findall("(Windows NT 5.0|Windows 2000)", user_agent)},
            {'s': 'Windows ME', 'r': re.findall("(Win 9x 4.90|Windows ME)", user_agent)},
            {'s': 'Windows 98', 'r': re.findall("(Windows 98|Win98)", user_agent)},
            {'s': 'Windows 95', 'r': re.findall("(Windows 95|Win95|Windows_95)", user_agent)},
            {'s': 'Windows NT 4.0', 'r': re.findall("(Windows NT 4.0|WinNT4.0|WinNT)", user_agent)},
            {'s': 'Windows CE', 'r': re.findall("Windows CE", user_agent)},
            {'s': 'Windows 3.11', 'r': re.findall("Win16", user_agent)},
            {'s': 'Android', 'r': re.findall("Android", user_agent)},
            {'s': 'Open BSD', 'r': re.findall("OpenBSD", user_agent)},
            {'s': 'Sun OS', 'r': re.findall("SunOS", user_agent)},
            {'s': 'Linux', 'r': re.findall("(Linux|X11)", user_agent)},
            {'s': 'iOS', 'r': re.findall("(iPhone|iPad|iPod)", user_agent)},
            {'s': 'Mac OS X', 'r': re.findall("Mac OS X", user_agent)},
            {'s': 'Mac OS', 'r': re.findall("(MacPPC|MacIntel|Mac_PowerPC|Macintosh)", user_agent)},
            {'s': 'QNX', 'r': re.findall("QNX", user_agent)},
            {'s': 'UNIX', 'r': re.findall("UNIX", user_agent)},
            {'s': 'BeOS', 'r': re.findall("BeOS", user_agent)},
            {'s': 'OS/2', 'r': re.findall("OS\/2", user_agent)},
            {'s': 'Search Bot',
             'r': re.findall("(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)",
                             user_agent)},
        ]

        for client in clientStrings:
            if len(client["r"]) > 0:
                os = client["s"]

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        real_ip = request.META.get('HTTP_X_REAL_IP')
        ip = "127.0.0.1"
        if not real_ip == None:
            ip = real_ip
        else:
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

        g = GeoIP2()
        # '41.141.74.230'

        user_agent = get_user_agent(request)
        mobile = False
        desktop = False
        if user_agent.is_mobile or user_agent.is_tablet:
            mobile = True
            desktop = False
        else:
            mobile = False
            desktop = True

        ip = str(ip)
        city = {"country_name": "Unknown", "city": "Unknown"}
        try:
            city = g.city(ip)
        except:
            city = {"country_name": "Unknown", "city": "Unknown"}

        if city["country_name"] == "null" or city["country_name"] is None:
            city["country_name"] = "Unknown"

        if city["city"] == "null" or city["city"] is None:
            city["city"] = "Unknown"


        return {  "ip" : ip, "browser" : browser, "os" : os, "country" : city["country_name"], "city" : city["city"], "mobile" : mobile, "desktop" : desktop }


    def parsekeywords(self, text, length=10):
        text = text
        current_language = self.detectLanguage(text)["current"]
        print(current_language)
        keywords = self.get_keywords(text, current_language, length)

        return { "keywords" : keywords, "lang" : current_language }




    def detectLanguage(self, text):
        object_detection = { "en" : 0, "fr" : 0, "ar" : 0 }
        l = len(text)
        score_en = 0
        score_fr = 0
        score_ar = 0

        for en in self.alphabet_en:
            index_of = text.find(en)
            if index_of > -1 :
                score_en += 1
                if len(en) > 1 :
                    split_en = text.split(en)
                    score_en += len(split_en)

        for fr in self.alphabet_fr:
            index_of_fr = text.find(fr)
            if index_of_fr > -1 :
                score_fr += 1
                if len(fr) > 1:
                    split_fr = text.split(fr)
                    score_fr += len(split_fr)

        for ar in self.alphabet_ar:
            index_of_ar = text.find(ar)
            if index_of_ar > -1 :
                score_ar += 1
                if len(ar) > 1:
                    split_ar = text.split(ar)
                    score_ar += len(split_ar)

        object_detection["en"] = (score_en * 100) / l
        object_detection["fr"] = (score_fr * 100) / l
        object_detection["ar"] = (score_ar * 100) / l

        current_language = "en"
        if object_detection["en"] > object_detection["fr"] and object_detection["en"] > object_detection["ar"] :
            current_language = "en"
        if object_detection["fr"] > object_detection["en"] and object_detection["fr"] > object_detection["ar"] :
            current_language = "fr"

        if object_detection["ar"] > object_detection["en"] and object_detection["ar"] > object_detection["fr"] :
            current_language = "ar"

        object_detection["current"] = current_language
        return object_detection



    def get_keywords(self, text, lang, length=None):

        stop_words = []
        if lang == "en" :
            stop_words = self.alphabet_en
        if lang == "fr":
            stop_words = self.alphabet_fr
        if lang == "fr":
            stop_words = self.alphabet_ar

        split_text = text.split(" ")
        result = []
        temp_result = ""
        sum_metric = 0
        len_text = len(text)
        for word in split_text:
            word = word.lower()
            word = word.replace(".", "").replace(",", "")
            word_passe_count = 0
            for stop in stop_words:
                if not word == stop and len(word) > 1 and temp_result.find(word) == -1:
                    word_passe_count += 1

            if word_passe_count == len(stop_words) :
                if not word == "" and not word == " " and not word == None:
                    temp_result += word + ","
                    split_word = text.split(word)
                    frequency = len(split_word)
                    len_word = len(word)

                    metric = ((len_word * frequency) * 100) / len_text
                    sum_metric +=metric
                    object_word = {"frequency": frequency, "metric": metric, "word": word, "length" : len_word}
                    result.append(object_word)




        result = sorted(result, key=itemgetter('metric'), reverse=True)
        mean_score = float(sum_metric) /  float(len(result))
        mean_score = round(mean_score)

        if length == None:
            new_result = []
            for item in result:
                if item["metric"] >= mean_score and item["metric"] > 0:
                    new_result.append(item)
            return new_result
        else:
            if length < len(result)-1 :
                result = result[0:length]



        return result

