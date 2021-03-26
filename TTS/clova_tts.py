import os
import pickle
import urllib.request


class clovaTTS(object):
    def __init__(self, speaker_name="nara", client_id=client_id, client_secret=client_secret, use_cache=False,
                 cache_dir=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.speaker_name = speaker_name
        self.use_cache = use_cache
        if self.use_cache == True:
            self.cache_file = os.path.join(cache_dir, "clovatts_cache.pkl")
            self.tts_cache = {}
            if os.path.exists(self.cache_file):
                self.tts_cache = self.load_obj(self.cache_file)

    def save_obj(self, obj, name):
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        with open(name, 'rb') as f:
            return pickle.load(f)

    def tts(self, text, save=False, save_dir='./'):
        if save:
            speech = self.naver_clova_tts(text)
            self.save(os.path.join(save_dir, "{}.mp3".format(text)), speech)
            return speech
        else:
            return self.naver_clova_tts(text)

    def save(self, filename, speech):
        with open(filename, 'wb') as f:
            f.write(speech)

    def naver_clova_tts(self, text):
        encText = urllib.parse.quote(text)
        if self.use_cache is True and encText in self.tts_cache:
            tts_data = self.tts_cache[encText]
        else:
            data = "speaker=" + self.speaker_name + "&volume=0&speed=0&pitch=0&emotion=0&format=mp3&text=" + encText
            url = "https://naveropenapi.apigw.ntruss.com/voice-premium/v1/tts"
            request = urllib.request.Request(url)
            request.add_header("X-NCP-APIGW-API-KEY-ID", self.client_id)
            request.add_header("X-NCP-APIGW-API-KEY", self.client_secret)
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
            rescode = response.getcode()
            if rescode == 200:
                tts_data = response.read()
                if self.use_cache is True:
                    self.tts_cache[encText] = tts_data
                    self.save_obj(self.tts_cache, self.cache_file)
            else:
                tts_data = None
        return tts_data

if __name__ == '__main__':
    clovaTTS().tts("내용을 넣으세요~", save=True)
