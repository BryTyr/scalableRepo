
import os
import numpy
import random
import string
import requests
from wave import Wave_write
import argparse
from scipy.io import wavfile
from pydub import AudioSegment
import time

# not used for a finish
# def import_all_sounds(path_to_files,symbol_set):
#     sounds={}
#     for symbol in symbol_set:
#         path =file_path = os.path.join(path_to_files, symbol+".mp3")
#         audio = AudioSegment.from_mp3(path)
#         sounds[symbol]=audio
#
#     return sounds

# not used for a finish
# def generateCaptcha(output_dir,captcha_name,loaded_sounds):
#         letters=list(captcha_name)
#         audio_file = AudioSegment.empty()
#
#         for letter in letters:
#             audio_file+=loaded_sounds[letter]
#
#         audio_file.export(output_dir+captcha_name+".mp3", format="mp3")
#




# this method uses a key to access googles tts service its limited to 300 requests a minute
#and is wayyyyyyyyyyyyyy to slow
def generateCaptchaGoogle(client,voice,audio_config,output_dir,captcha_name,loaded_sounds):

    # Set the text input to be synthesized
    text="<speak>"+captcha_name+"</speak>"
    synthesis_input = texttospeech.types.SynthesisInput(ssml=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open("inputFolder/"+captcha_name+'.mp3', 'wb') as out:
    # Write the response to the output file.
        out.write(response.audio_content)


# genrates audio file from google tts system
# top tip: google doesnt appriaciate using their service 100,000 times and tries
# to throttle you by slowing your IP address, to stop that use a VPN
def generateCaptchaGoogleCurl(captcha_name,filepath):
    processed_captcha=""
    letter_list=list(captcha_name)
    letter_list.reverse()

    for letter in letter_list:
        processed_captcha=letter+"%20"+processed_captcha

    # use this line to throttle your connection if you dont have access to a vpn
    #time.sleep(.1) # Delay for 1 minute (60 seconds).

    # this sends a http request to googles tts service and saves the result in the file system must be run on an Linux or mac machine
    os.system("curl 'https://translate.google.com/translate_tts?ie=UTF-8&q="+processed_captcha+"&tl=en&total=1&idx=0&textlen=15&tk=32541.448351&client=tw-ob\' -H \'user-agent: stagefright/1.2 (Linux;Android 5.0)\' -H \'referer: https://translate.google.com/\' > "+"./inputFolder/"+captcha_name+".mp3")


# tries to change the speed of text didnt work very well
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', help='enter path of input MP3 files', type=str)
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--scramble', help='Whether to scramble image names', default=False, action='store_true')
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.input_dir is None:
        print("Please specify the input mp3 files")
        exit(1)

    if args.length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()
    print(symbols_file)

    print("Generating captchas with symbol set {" + captcha_symbols + "}")

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)


    for i in range(args.count):
        captcha_text = ''.join([random.choice(captcha_symbols) for j in range(args.length)])
        image_name_scrambled = captcha_text
        if args.scramble:
            image_name_scrambled = scramble_image_name(captcha_text)
        image_path = os.path.join(args.output_dir, image_name_scrambled+'.mp3')
        if os.path.exists(image_path):
            version = 1
            while os.path.exists(os.path.join(args.output_dir, image_name_scrambled + '_' + str(version) + '.mp3')):
                version += 1
            image_path = os.path.join(args.output_dir, image_name_scrambled + '_' + str(version) + '.mp3')

        generateCaptchaGoogleCurl(image_name_scrambled,args.output_dir)
if __name__ == '__main__':
    main()
