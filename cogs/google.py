from google.cloud import texttospeech # ssml must be well-formed according to: https://www.w3.org/TR/speech-synthesis/
import platform
# Error handling for GOOGLE_APPLICATION_CREDENTIALS
try:
    with open(f"{pathing('LoginInfo')}/serviceTokenPath.json", "r") as f:
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (json.load(f))[platform.system()]
        except:
            raise FileNotFoundError
except FileNotFoundError:
    with open(f"{pathing('LoginInfo')}/serviceTokenPath.json", "w") as f:
        path = input(f"set path for {platform.system()} to GOOGLE_APPLICATION_CREDENTIALS: ")
        json.dump({f"{platform.system()}": path}, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
except IndexError:
    with open(f"{pathing('LoginInfo')}/serviceTokenPath.json", "a+") as f:
        _path = json.load(f)
        path = input(f"set path for {platform.system()} to GOOGLE_APPLICATION_CREDENTIALS: ")
        _path.append({f"{platform.system()}": path})
        json.dump(_path, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

def googleTTS(string):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=string)
    voice = texttospeech.types.VoiceSelectionParams(language_code='en-AU-Standard-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open(f"{pathing()}/Voicelines/output.mp3", 'wb') as out:
        out.write(response.audio_content)
    return f"{pathing()}/Voicelines/output.mp3"

    @comms.command()
    async def google(self, ctx, option):
        if await ctx.bot.is_owner(ctx.author):
            options = ['say', 'search']
            if option in options:
                if option == 'say':
                    vc = ctx.guild.voice_client
                    if not vc:
                        vc = await ctx.author.voice.channel.connect()
                    option0 = (list(ctx.message.content))[12:]
                    option0 = ''.join(str(y) for y in option0)
                    googleTTS(option0)
                    vc.play(discord.FFmpegPCMAudio(f"{pathing()}/Voicelines/output.mp3"))
                    print(f"{ctx.message.author} has said '{option0}' with googleTTS")
                elif option == 'search':
                    pass
            else:
                await ctx.send(f"Option isn't in {', '.join(str(y) for y in options)}")
        else:
            ctx.send(f"{ctx.author.mention}, I do not approve")

    @comms.command()
    async def volume(self, ctx, amount):
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = int(amount)
        print(f"{ctx.message.author} has changed the volume to {int(amount)}")
