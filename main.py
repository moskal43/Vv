import requests
import pyaudacity as pa
import time
import os
import librosa
import soundfile as sf

apiUrl = "https://zvukogram.com/index.php?r=api/text"
apiToken = "TOKEN"
email = "MAIL"
voice = "Девочка Таня"
commandFile = "command.txt"


def getVoiceActingData(command):
    param = {
        'token': apiToken,
        'email': email,
        'voice': voice,
        'text': command,
        'format': 'ogg',
        'speed': 1,
        'pitch': 0,
        'emotion': 'neutral',
        'bitrate': 16000
    }
    resp = requests.post(apiUrl, data=param)

    return resp.json()


def downloadVoiceFile(downloadUrl, commandNumber):
    response = requests.get(downloadUrl)
    with open('original/' + commandNumber, 'wb') as file:
        file.write(response.content)


def parsingCommandFile(fileName):
    with open(fileName, encoding='utf-8') as file:
        data = file.read().split('\n')

    command = {}
    for elem in data:
        if elem:
            version = list(filter(None, elem.split(':')))
            command[version[0]] = ', '.join(version[1:])
        else:
            continue

    return command


def addSubnaticEffect(fileName):
    pa.new()
    time.sleep(2)
    pa.open('original/' + fileName)
    pa.open('original/' + fileName)
    pa.clip_right()
    pa.clip_right()
    pa.clip_right()
    pa.clip_right()
    pa.select_all()
    pa.high_pass_filter(250, 'dB6')
    pa.echo(0.002, 0.7)
    pa.export('effect/' + fileName)
    pa.save('trash/' + fileName)
    pa.close()


if __name__ == '__main__':
    commands = parsingCommandFile(commandFile)
    for commandNumber in commands:
        data = getVoiceActingData(commands.get(commandNumber))
        if data['error']:
            print('Не удалось перевести команду - ', commandNumber)
            print('Ошибка - ', data['error'])
            break
        downloadVoiceFile(data['file'], commandNumber)

    # files = os.listdir('lost')
    # for file in files:
    #     addSubnaticEffect(file)

    # files = os.listdir('effect')
    # for file in files:
    #     y, sr = librosa.load('effect/' + file, sr=16000)
    #     sf.write('resample/' + file, y, sr)
