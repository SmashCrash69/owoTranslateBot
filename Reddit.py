from os import name
import praw, random, json, time
subreddits = {
    "dick" : ["MassiveCock", "penis", "monsterdicks", "ThickDick", "ratemycock", "cock", "averagepenis", "dicks"], 
    "ass": ["FantasticAss", "asstastic", "bigasses", "thick", "pawg", "ass", "assinthong"], 
    "tits": ["BustyPetite", "Boobies", "bustybabes", "voluptuous", "tits", "Stacked", "Nipples"],
    "pussy": ["pussy", "GodPussy", "LabiaGW", "nsfw", "knockmeup"], 
    "hentai": ["rule34", "hentai", "animebooty"], 
    "bdsm": ["bdsm", "bdsmgw", "bondage", "bondageblowjobs", "spanking", "forcedorgasms", "collared", "intenseBDSM", "skinnyBDSM", "dominated", "teenbdsm", "femsub"], 
    "porn": ["nsfw", "nsfw_gif", "porn", "porn_gifs", "gonewild", "happygirls", "nsfwgaming", "naughtywives", "nsfw_gifs", "nude_selfie", "LipsThatGrip"], 
    "gay_porn": ["gaynsfw", "gaygifs", "gayporn", "gaybrosgonewild", "twinks", "lovegaymale", "gaycumsluts", "rule34gay"],
    "futanari": ["futanari", "cutefutanari", "shesbiggerthanyou", "futanaripegging", "Futasarebigger"],
    "femboy":  ["traphentai", "FemboyHentai", "SubbyStonerBoi", "ThiccTrapsH", "VentiHentai"],
    "thighs": ["thighdeology", "animethighss", "AnimeThicc"],
    "food": ["foodporn", "food", "burgers"],
    "cars": ["carporn", "F1Porn", "JDM", "Autos", "Shitty_Car_Mods"]
}
ListOfsubreddits = [
    "dick", 
    "ass", 
    "tits",
    "pussy", 
    "hentai", 
    "bdsm", 
    "porn", 
    "gay_porn",
    "futanari",
    "femboy",
    "thighs",
    "food",
    "cars"]
urls = {"dick": set(), "ass": set(), "tits": set(), "pussy": set(), "hentai": set(), "bdsm": set(), "porn": set(), "gay_porn": set(), "futanari": set(), "femboy": set(), "thighs": set(), "food": set(), "cars": set()}
image_types = ("jpg", "jpeg", "png", "gif")
counter = 0
total = 100
conn = praw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET", user_agent="owoTranslatorBot by mlgmj_0")

def write(urls):
    newUrls = {}
    with open("urlsv2.json", "w") as file:
        for i in list(urls):
            newUrls[i] = list(urls[i])
        file.write(json.dumps(newUrls))

def read(urls : dict = {"dick": set(), "ass": set(), "tits": set(), "pussy": set(), "hentai": set(), "bdsm": set(), "porn": set(), "gay_porn": set(), "futanari": set(), "femboy": set(), "thighs": set(), "food": set(), "cars": set()}):
    with open("urlsv2.json", "r") as file:
        oldUrls = json.loads(file.read())
        for i in list(oldUrls):
            if oldUrls[i] != list(urls[i]):
                if len(oldUrls[i]) > len(list(urls[i])):
                    urls[i] = set(oldUrls[i])
    return urls


def main(urls, counter, total):
    try:
        write(urls)
        time.sleep(0.5)
        urls = read(urls)
        if counter >= len(ListOfsubreddits):
            counter = 0
        if len(urls[ListOfsubreddits[counter]]) <= total:
            genre = ListOfsubreddits[counter]
            subreddit = conn.subreddit(random.choice(subreddits[genre]))
            for submission in subreddit.hot(limit=50):
                if submission.url.split(".")[-1] in image_types:
                    if submission.score > 10 and submission.upvote_ratio > 0.75:
                        oldLen = len(urls[genre])
                        urls[genre].add(submission.url)
                        newLen = len(urls[genre])
                        if newLen > oldLen:
                            counter += 1
                            return urls, counter, total
        else:
            for i in list(subreddits):
                if len(subreddits[i]) < total:
                    return urls, counter, total
        total += 100
        print("prestige: " + str(total//100))
    except Exception as e:
        raise e
    return urls, counter, total

while True:
    urls, counter, total = main(urls, counter, total)
