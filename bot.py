from importlib import reload

import discord

import config
import processor


client = discord.Client()


@client.event
async def on_ready():
    print('Engine Hearth logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # No self-reply
    if message.author == client.user:
        return

    if message.content == 'reload':
        reload(config)
        reload(processor)
        await message.add_reaction('\u2705')  # white_check_mark
        return

    await processor.on_message(message)


def main():
    secret = open(config.EnvConfig['secret_file']).read()
    client.run(secret)


if __name__ == "__main__":
    main()
