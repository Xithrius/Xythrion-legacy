"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import __main__
import datetime
import os
import aiohttp
from google.cloud import texttospeech
import asyncio


def path(*objects):
    """ Returns path relative to caller file location with additional objects, if any """
    newPath = ((__main__.__file__).split(os.sep))[:-1]
    for i in objects:
        newPath.append(i)
    return (os.sep).join(str(y) for y in newPath)


credentials_path = path('handlers', 'configuration', 'google_service_credentials.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


def printc(string):
    """ Customized printing to the console with timestamps """
    now = datetime.datetime.now()
    print(f"~> [{now}] {string}")


def create_table(cogs_dict):
    """ """
    keys, cogs = [], []
    for k, v in cogs_dict.items():
        keys.append(k)
        cogs.append(', '.join(str(y)[:-3] for y in v))
    longest_cog_name = max(map(len, keys))
    longest_cog_line = max(map(len, cogs))
    print()
    for i in range(len(keys)):
        print(f'\t+{"-" * (longest_cog_name + 2)}+{"-" * (longest_cog_line + 2)}+')
        print(f'\t| {keys[i]}{" " * (longest_cog_name - len(keys[i]))} | {cogs[i]}{" " * (longest_cog_line - len(cogs[i]))} |')
    print(f'\t+{"-" * (longest_cog_name + 2)}+{"-" * (longest_cog_line + 2)}+')
    print()


def now():
    """ Returns the time depending on time zone from file """
    return datetime.datetime.now()


def progress_bar(iteration, total, prefix='PROGRESS:', suffix='COMPLETE', decimals=2, length=50, fill='█'):
    """ Progress bar for tracking progress """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

'''
async def tts(ctx):
    """ Text to speech through the bot's mic """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
    voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open(path('repository', 'tmp', 'output.mp3'), 'wb') as out:
        out.write(response.audio_content)
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=path('repository', 'tmp', 'output.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
'''
