import discord
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

client = discord.Client()
sr_no = 1


def generate_win_lose_bar(wins, losses):
    win = wins / (wins + losses)
    lose = 1 - win
    size = (317, 72)
    size_win = (int(size[0] - (size[0] * lose)), 72)
    size_lose = (int(size[0] - (size[0] * win)), 72)
    imgs = [Image.new('RGB', size_win, color='blue'), Image.new('RGB', size_lose, color='red')]
    img = Image.fromarray(np.hstack(list(np.asarray(i) for i in imgs)))
    return img.resize((100, 36))


async def get_discord_avatar(discord_id, bot):
    def resize_discord_avatar(avatar):
        im = avatar
        big_size = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        im = im.resize((64, 64))
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output.resize((64, 64))

    member = await bot.fetch_user(discord_id)
    response = requests.get(member.avatar_url_as(size=128), stream=True)  # .save()
    if response.status_code == 200:
        try:
            img = Image.open(response.raw)
            name = member.display_name.split()
            if len(name) > 1:
                name = name[1]
            else:
                name = name[0]
            return resize_discord_avatar(img), name
        except:
            print('An error occurred in lb_generator get_discord_avatar during fetching')


def paste_text(img, text, px, color='#000000', size=23):
    text = str(text)
    fnt = ImageFont.truetype('utils/fonts/Ginto-Nord-Regular.ttf', size)
    d = ImageDraw.Draw(img)
    d.text(px, text, font=fnt, fill=color)


def paste_img(img1, img2, px):
    return img1.paste(img2, px, img2.convert('RGBA'))


def update_pxs(pxs):
    for key in pxs:
        pxs[key] = pxs[key][0], pxs[key][1] + 100
    return pxs


async def generate_leaderboard(stats, table_name, bot):
    print('inside generate_leaderboard')
    global sr_no
    lbs = []
    pxs = {'sr': (34, 245), 'avatar': (77, 225), 'name': (168, 245), 'bar': (337, 236), 'wins': (344, 246),
           'losses': (408, 247), 'win_percent': (470, 244), 'kda': (650, 245), 'cs': (827, 245),
           'quadraKills': (967, 245), 'pentaKills': (1206, 245), 'averageDamageDealt': (1421, 245),
           'averageDamageTaken': (1699, 245), 'highestKillGame': (1976, 245), 'highestDeathGame': (2156, 245)}
    lb = Image.open(f'utils/img/{table_name}.jpg')
    index = 1
    for discord_id in stats:
        avatar, name = await get_discord_avatar(discord_id, bot)
        display_name = name  # '\n'.join(textwrap.wrap(name, width=10))
        bar = generate_win_lose_bar(wins=stats[discord_id]['wins'], losses=stats[discord_id]['losses'])
        paste_img(lb, avatar, pxs['avatar'])
        paste_img(lb, bar, pxs['bar'])
        paste_text(lb, display_name, pxs['name'])
        paste_text(lb, f'{sr_no}.', pxs['sr'])
        paste_text(lb, f"{stats[discord_id]['wins']}W", pxs['wins'], color='#ffffff', size=16)
        paste_text(lb, f"{stats[discord_id]['losses']}L", pxs['losses'], size=16)
        paste_text(lb, f"{round((stats[discord_id]['wins'] / stats[discord_id]['no_of_matches']) * 100, 1)}%",
                   pxs['win_percent'],
                   color='#00691f')
        paste_text(lb,
                   f"{round((stats[discord_id]['kills'] + stats[discord_id]['assists']) / stats[discord_id]['deaths'], 1)}",
                   pxs['kda'],
                   color='#910101')
        paste_text(lb, round(stats[discord_id]['creepScore'], 1), pxs['cs'], color='#040145')
        paste_text(lb, stats[discord_id]['quadraKills'], pxs['quadraKills'], color='#910101')
        paste_text(lb, stats[discord_id]['pentaKills'], pxs['pentaKills'], color='#910101')
        paste_text(lb, stats[discord_id]['averageDamageDealt'], pxs['averageDamageDealt'], color='#910101')
        paste_text(lb, stats[discord_id]['averageDamageTaken'], pxs['averageDamageTaken'], color='#910101')
        paste_text(lb, stats[discord_id]['highestKillGame'], pxs['highestKillGame'], color='#00691f')
        paste_text(lb, stats[discord_id]['highestDeathGame'], pxs['highestDeathGame'], color='#00691f')
        stats = update_pxs(pxs)
        sr_no += 1
        index += 1
        if index == 10:
            lb.save(f'utils/img/temp/temp{index}.jpg')
            lbs.append(f'utils/img/temp/temp{index}.jpg')
            lb = Image.open(f'utils/img/{table_name}.jpg')
            index = 1
        else:
            lb.save(f'utils/img/temp/temp{index}.jpg')
            lbs.append(f'utils/img/temp/temp{index}.jpg')
            lb = Image.open(f'utils/img/{table_name}.jpg')
            index = 1

    print('leaving generate_leaderboard')
    return lbs
