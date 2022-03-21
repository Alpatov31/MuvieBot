import random
import vk_api
import time
import sqlite3
import os
import nltk
import requests

nltk.download('punkt')
from moviepy.editor import *

#poets_sub = open("subs/dead_poets_society.txt", "r")
#poets_list = poets_sub.readlines()

charade_sub = open("subs/charade.txt", "r")
charade_list = charade_sub.readlines()

friday_sub = open("subs/friday.txt", "r")
friday_list = friday_sub.readlines()

all_films = [charade_list, friday_list]

movies = ["films/charade.mp4", "films/friday.mp4"]

clp = []

level = ""
levels = ["Elementary Level", "Middle School Level", "High School Level", "College Level"]
definition = ""


def set_state(state, id):
    sql = f'''UPDATE Users SET state='{state}' WHERE id={id} '''
    cursor.execute(sql)
    conn.commit()


def set_property(name, value, id):
    sql = f'''UPDATE Users SET {name}='{value}' WHERE id={id} '''
    cursor.execute(sql)
    conn.commit()


def get_property(name, id):
    sql = f"SELECT {name} FROM Users WHERE id={from_id} "
    cursor.execute(sql)
    return cursor.fetchone()[0]


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

vk = vk_api.VkApi(token="c79337c4783864bd1731fb1bef7085122586ebc96ba54e03d40a696abf9426df633cd58c4c094ec7c965f")
api = vk_api.VkApi(token="00ab3a2baddb6a0e6cd8590926da522ce3d994fd335a484896bacc6ac758a540a36bdd0d552c1ca78e93c")
api._auth_token()
vk._auth_token()

value = {"count": 20, "offset": 0, "filter": "unanswered"}

kbrd = open("keyboards/empty.json", "r", encoding="UTF-8").read()

link = ""

while True:
    isclip = 0
    isword = 0

    random_films = []
    random_words = []

    final_sub = ""

    word_list = []
    timing_start_list = []
    timing_end_list = []

    k = 0

    level = ""

    meaning = ""

    kol = ""

    messages = vk.method("messages.getConversations", value)

    if messages["count"] > 0:
        from_id = messages["items"][0]["last_message"]["from_id"]
        in_text = messages["items"][0]["last_message"]["text"]

        sql = f"SELECT * FROM Users WHERE id={from_id}"
        cursor.execute(sql)
        if len(cursor.fetchall()) == 0:
            sql = f'''
                    INSERT INTO Users (id, state)
                    VALUES ({from_id}, 'start')
                    '''
            cursor.execute(sql)
            conn.commit()

        if in_text == "Home":
            set_state("start", from_id)

        sql = f"SELECT state FROM Users WHERE id={from_id} "
        cursor.execute(sql)
        state = cursor.fetchone()[0]
        print(state)

        if state == "take":
            out_text = "Привет напиши слово на английском, либо на русском."
            set_state("word", from_id)
        elif state == "word":
            set_property("word", in_text, from_id)
            set_state("finish", from_id)

        word = in_text

        for i in all_films:
            for j in i:
                s = nltk.word_tokenize(j.lower())
                if word in s:
                    if "-->" in i[i.index(j) - 1]:
                        timing = i[i.index(j) - 1]
                        start = timing[:12]
                        end = timing[17:29]
                        time_1 = (int(start[:2]) * 360 + int(start[3:5]) * 60 + int(start[6:8]))
                        time_2 = (int(end[:2]) * 360 + int(end[3:5]) * 60 + int(end[6:8]))
                        time_len = time_2 - time_1
                        if time_len > 2:
                            random_films.append(i)
                    else:
                        timing = i[i.index(j) - 2]
                        start = timing[:12]
                        end = timing[17:29]
                        time_1 = (int(start[:2]) * 360 + int(start[3:5]) * 60 + int(start[6:8]))
                        time_2 = (int(end[:2]) * 360 + int(end[3:5]) * 60 + int(end[6:8]))
                        time_len = time_2 - time_1
                        if time_len > 2:
                            random_films.append(i)

        for i in random_films:
            for j in range(random_films.count(i) - 1):
                random_films.remove(i)
        if len(random_films) > 0:
            random_film = random.choice(random_films)

            for i in random_film:
                s = nltk.word_tokenize(i.lower())
                if word in s:
                    if "-->" in random_film[random_film.index(i) - 1]:
                        timing = random_film[random_film.index(i) - 1]
                        start = timing[:12]
                        end = timing[17:29]
                        time_1 = (int(start[:2]) * 360 + int(start[3:5]) * 60 + int(start[6:8]))
                        time_2 = (int(end[:2]) * 360 + int(end[3:5]) * 60 + int(end[6:8]))
                        time_len = time_2 - time_1
                        if time_len > 2:
                            timing_start_list.append(start)
                            timing_end_list.append(end)
                            word_list.append(i)
                    else:
                        timing = random_film[random_film.index(i) - 2]
                        start = timing[:12]
                        end = timing[17:29]
                        time_1 = (int(start[:2]) * 360 + int(start[3:5]) * 60 + int(start[6:8]))
                        time_2 = (int(end[:2]) * 360 + int(end[3:5]) * 60 + int(end[6:8]))
                        time_len = time_2 - time_1
                        if time_len > 2:
                            timing_start_list.append(start)
                            timing_end_list.append(end)
                            word_list.append(i)

            if len(word_list) > 0:
                random_index = random.randint(0, len(word_list) - 1)

                clip = VideoFileClip(movies[all_films.index(random_film)]).subclip(timing_start_list[random_index],
                                                                                   timing_end_list[random_index])
                final_lst = [random_film[random_film.index(word_list[random_index]) - 1], word_list[random_index],
                             random_film[random_film.index(word_list[random_index]) + 1]]
                for f in range(len(final_lst)):
                    final_lst[f] = final_lst[f].replace("<i>", "")
                    final_lst[f] = final_lst[f].replace("</i>", "")
                    final_lst[f] = final_lst[f].replace("\n", " ")
                    final_lst[f] = final_lst[f].replace("вЂ”", "")
                if ">" in final_lst[0]:
                    final_lst.remove(final_lst[0])
                final_sub = "".join(final_lst)
                clip_sub = TextClip(final_sub, font="Amiri-regular", color="white", fontsize=40).set_duration(
                    clip.duration)
                clip_sub = clip_sub.set_pos("bottom", "center")
                final_clip = CompositeVideoClip([clip, clip_sub])
                final_clip.write_videofile("clip.mp4")
                isclip = 1

        response = requests.get(f"https://www.dictionary.com/browse/{word}")  # get-запрос
        if ("definition, ") not in response.text:
            isword = 0
        else:
            isword = 1
            for i in levels:
                if i in response.text:
                    level = "⭐" * (levels.index(i) + 1)

            defin = response.text.index("definition, ")
            defin += 12
            numb = 0
            kol = response.text[defin + numb]
            while kol != ">":
                kol = response.text[defin + numb]
                meaning += kol
                numb += 1

            meaning = meaning[:-12]
        if isword == 1 and isclip == 0:
            vk.method("messages.send",
                      {"peer_id": from_id, "message": (
                          f"Слово: {word}\nЗначение: {meaning}\nСложность: {level}\n(К сожалению, мы не смогли найти отрывок с данным словом)"),
                       "random_id": random.randint(1, 1000), "keyboard": kbrd})
        elif isword == 0 and isclip == 0:
            vk.method("messages.send",
                      {"peer_id": from_id, "message": ("К сожалению, такого слова нет в словаре"),
                       "random_id": random.randint(1, 1000), "keyboard": kbrd})
        else:
            a = api.method("video.save", {"name": "clip"})
            b = requests.post(a["upload_url"],
                              files={"video_file": open("C:/Users/Asus/Desktop/final_muvie/clip.mp4", "rb")}).json()
            c = "video" + str(b['owner_id']) + "_" + str(b['video_id'])
            time.sleep(1)
            vk.method("messages.send",
                      {"peer_id": from_id, "message": (f"Слово: {word}\nЗначение: {meaning}\nСложность: {level}"),
                       "attachment": c,
                       "random_id": random.randint(1, 1000), "keyboard": kbrd})
    time.sleep(1)