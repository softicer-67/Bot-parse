# -*- coding: utf8 -*-
import json
import random
import requests
import time
from config import token_vk
import os


def start_search_posts():
    version = 5.131
    domain = 'globalcinema'
    count = 1
    offset = 1
    response = requests.get('https://api.vk.com/method/wall.get', params={
        'access_token': token_vk,
        'v': version,
        'domain': domain,
        'count': count,
        'offset': offset
    })
    all_posts = {}
    posts = response.json()['response']['items']

    for post in posts:
        post_id = str(post['id'])
        post_title = post['text']
        with open(f"posts.txt", encoding='utf-8') as i:
            txt = [i.rstrip('\n') for i in i]
        if post_id in txt:
            print('Нет новых постов')
            print('=' * 70)
            break
        else:
            print(f'Записываю пост ID {post_id} в txt')
            try:
                print(f'Новый пост ID: {post_id} | {post_title[:40]}...')
            except UnicodeEncodeError:
                continue
            with open(f"posts.txt", "w") as file:
                file.write(f'{post_id}\n')

            if 'attachments' in post:
                post = post['attachments']

                # Забираем фото
                pq = []
                if post[0]['type'] == 'photo':
                    photo_quality = post[0]['photo']['sizes']
                    for c in photo_quality:
                        pq.append([c['height'], c['url']])
                        photo_hi = max(pq)
                        post_img = photo_hi[1]
                # Забираем стоп-кадр видео
                vq = []
                if post[0]['type'] == 'video':
                    video_quality = post[0]['video']['image']
                    for d in video_quality:
                        vq.append((d['height'], d['url']))
                        video_hi = max(vq)
                        post_img = video_hi[1]

            all_posts[post_id] = {
                'post_title': post_title,
                'post_img': post_img
                }

            print(f'Записываю пост ID {post_id} в json')
            print('=' * 70)
            with open("all_posts.json", "w", encoding="utf-8") as file:
                json.dump(all_posts, file, indent=4, ensure_ascii=False)

            os.system('python bot.py')


def main():
    cnt = 1
    while True:
        try:
            print(f'[+] Ожидание новостей {cnt}')
            start_search_posts()
            t = random.uniform(180, 250)
            time.sleep(t)
            cnt += 1
        except Exception:
            continue


if __name__ == '__main__':
    main()
