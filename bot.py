import functools
import random
import re

import discord

from config import EnvConfig as cfg
from roll import Check


MAX_POOL_SIZE = 100
MAX_POOL_RESULT_LEN = 1000

client = discord.Client()


@client.event
async def on_ready():
    print('Engine Hearth logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # No self-reply
    if message.author == client.user:
        return

    # Limit to one channel
    if message.channel.name != cfg['channel']:
        return

    # If the message starts with a number, roll a check with that pool size
    pool_match = re.search(r'^\s*(\d+)', message.content)
    if pool_match:
        pool_size = min(int(pool_match.group(1)), MAX_POOL_SIZE)
        await roll_check(message, pool_size)

    # No other actions supported at this time


async def roll_check(message, pool_size):
    '''
    Roll a check and return a rich embed describing the results
    '''
    # Check for a specified target number
    target_match = re.search(r'[Tt]\s*(\d+)', message.content)
    if target_match:
        # TN can't be below 2
        target_num = max(int(target_match.group(1)), 2)
    else:
        target_num = 8

    # Check for user karma - TODO
    karma = 0

    # Make the check
    result = Check(pool_size, target_num, karma=0)

    # Format the raw roll results
    result_str = ' + '.join(
        f"[{' '.join(map(str, sorted(roll, reverse=True)))}]"
        for roll in result.rolls)
    if len(result_str) > MAX_POOL_RESULT_LEN:
        result_str = result_str[:MAX_POOL_RESULT_LEN]

    # Format the rich embed reply
    embed = discord.Embed(color=message.author.color)
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.add_field(name=f'{pool_size}d10 TN {target_num}', value=result_str, inline=True)
    embed.add_field(name='Successes', value=f'**{result.successes}**', inline=True)
    embed.add_field(name='Ones', value=f'**{result.ones}**', inline=True)
    await message.channel.send(embed=embed)


def main():
    secret = open(cfg['secret_file']).read()
    client.run(secret)


if __name__ == "__main__":
    main()
