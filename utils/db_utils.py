from datetime import datetime

import discord
from pycoingecko import CoinGeckoAPI


def get_volume(currency):
    coin = CoinGeckoAPI()
    for coin in coin.get_coins():
        if coin['symbol'] == currency.lower():
            return coin['market_data']['total_volume']['usd']
    else:
        return None


def signals_helper(signal):
    embed = discord.Embed(
        title="Quality Signals Channel",
        description="",
        color=0xD5059D
    )
    embed.add_field(
        name=f"{convert_time_stamp(signal['timestamp'])}",
        value=chr(173),
        inline=False
    )
    embed.add_field(
        name=f"💎 Buy #{signal['coin']}/#{signal['currency']}",
        value=chr(173),
        inline=False
    )

    embed.add_field(name=chr(173), value=chr(173))

    embed.add_field(
        name=f"🛒 Entry Zone: {round(float(signal['buy_start']), 9)}-{round(float(signal['buy_end']), 9)}",
        value=chr(173),
        inline=False
    )
    embed.add_field(
        name=f"💵 Current ask: {round(float(signal['ask']), 9)}",
        value=chr(173),
        inline=False
    )
    embed.add_field(
        name=f"🎯 Target 1: {round(float(signal['target1']), 9)} ({round((float(signal['buy_end']) - float(signal['target1'])) / float(signal['buy_end']) * 100, 2) * -1}%)",
        value=chr(173),
        inline=False
    )
    if 'target2' in signal:
        embed.add_field(
            name=f"🎯 Target 2: {round(float(signal['target2']), 9)} ({round((float(signal['buy_end']) - float(signal['target2'])) / float(signal['buy_end']) * 100, 2) * -1}%)",
            value=chr(173),
            inline=False
        )
    if 'target3' in signal:
        embed.add_field(
            name=f"🎯 Target 3: {round(float(signal['target3']), 9)} ({round(((float(signal['buy_end']) - float(signal['target3'])) / float(signal['buy_end']) * 100), 2) * -1}%)",
            value=chr(173),
            inline=False
        )

    embed.add_field(name=chr(173), value=chr(173))

    if 'stop_loss' in signal:
        embed.add_field(
            name=f"🚫 Stop loss: {round(float(signal['stop_loss']), 9)} ({round(((float(signal['stop_loss']) - float(signal['buy_end'])) / float(signal['buy_end'])) * 100, 2)}%)",
            value=chr(173),
            inline=False
        )

    embed.add_field(
        name=f"💰 Volume #{signal['currency']}: {get_volume(signal['currency'])}$",
        value=chr(173),
        inline=False
    )

    embed.add_field(
        name=f"💰 Volume #{signal['coin']}: {get_volume(signal['coin'])}$",
        value=chr(173),
        inline=False
    )

    embed.add_field(name=chr(173), value=chr(173))

    embed.add_field(
        name=f"⏳ {signal['type']}",
        value=chr(173),
        inline=False
    )

    if "risk_level" in signal:
        if int(signal['risk_level']) <= 2:
            embed.add_field(
                name=f"⚠ Risk: {signal['risk_level']}/5 LOW",
                value=chr(173),
                inline=False
            )
        elif int(signal['risk_level']) == 3:
            embed.add_field(
                name=f"⚠ Risk: 3/5 MEDIUM",
                value=chr(173),
                inline=False
            )
        elif int(signal['risk_level']) == 4:
            embed.add_field(
                name=f"⚠ Risk: 4/5 MEDIUM HIGH",
                value=chr(173),
                inline=False
            )
        elif int(signal['risk_level']) == 5:
            embed.add_field(
                name=f"⚠ Risk: 5/5 HIGH",
                value=chr(173),
                inline=False
            )
    return embed


def create_telegram_msg(signal):
    text = f"🔥🔥🔥*Crypto Quality Signals*🔥🔥🔥\n\n" \
           f"*{convert_time_stamp(signal['timestamp'])}*\n\n" \
           f"💎 *Buy #{signal['coin']}/#{signal['currency']}*\n\n" \
           f"🛒 *Entry Zone: {round(float(signal['buy_start']), 9)}-{round(float(signal['buy_end']), 9)}*\n" \
           f"💵 *Current ask: {round(float(signal['ask']), 9)}*\n" \
           f"🎯 *Target 1: {round(float(signal['target1']), 9)} ({round((float(signal['buy_end']) - float(signal['target1'])) / float(signal['buy_end']) * 100, 2) * -1}%)*\n" \
           f"🎯 *Target 2: {round(float(signal['target2']), 9)} ({round((float(signal['buy_end']) - float(signal['target2'])) / float(signal['buy_end']) * 100, 2) * -1}%)*\n" \
           f"🎯 *Target 3: {round(float(signal['target3']), 9)} ({round(((float(signal['buy_end']) - float(signal['target3'])) / float(signal['buy_end']) * 100), 2) * -1}%)*\n\n" \
           f"🚫 *Stop loss: {round(float(signal['stop_loss']), 9)} ({round(((float(signal['stop_loss']) - float(signal['buy_end'])) / float(signal['buy_end'])) * 100, 2)}%)*\n\n" \
           f"💰 *Volume #{signal['currency']}: {get_volume(signal['currency'])}$*\n" \
           f"💰 *Volume #{signal['coin']}: {get_volume(signal['coin'])}$*\n\n" \
           f"⏳ *{signal['type']}*\n\n"
    if "risk_level" in signal:
        if int(signal['risk_level']) <= 2:
            text += f"⚠ *Risk: {signal['risk_level']}/5 LOW*"
        elif int(signal['risk_level']) == 3:
            text += f"⚠ *Risk: 3/5 MEDIUM*"
        elif int(signal['risk_level']) == 4:
            text += f"⚠ *Risk: 4/5 MEDIUM HIGH*"
        elif int(signal['risk_level']) == 5:
            text += f"⚠ *Risk: 5/5 HIGH*"


def convert_time_stamp(time):
    months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
              11: "Nov", 12: "Dec"}
    time = time.rstrip().split()
    date = time[0].split("-")
    time = datetime.strptime(time[1], "%H:%M:%S")
    month = months[int(date[1])]
    return f"{month} {date[2]}, {time.strftime('%I:%M %p')}"