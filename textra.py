

import json
from typing import Literal
import requests
from requests_oauthlib import OAuth1


"""
Textraを利用するための自作クラスです。
"""

class TexTra():

    def __init__(
        self,
        name: str,
        api_key: str,
        api_secret: str,
        url: str,
        type: Literal['xml', 'json'] = 'json',
        api_name: Literal['mt'] = 'mt',
        limit: int = 200,
        offset: int = 0
    ):

        # api connection
        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = url

        # api name
        self.api_name = api_name

        # response type
        self.type = type
        self.limit = limit
        self.offset = offset


    def translate(self, src_lang: Literal['ja', 'en'], dest_lang: Literal['ja', 'en'], text: str) -> dict:

        # create requests param
        auth = OAuth1(self.api_key, self.api_secret)

        param = {
            'key': self.api_key,
            'name': self.name,
            'type': self.type,
            'text': text,
            'api_name': self.api_name,
            'api_param': f'generalNT_{src_lang}_{dest_lang}',
            'limit': self.limit,
            'offset': self.offset
        }

        try:
            res = requests.post(url=self.url, data=param, auth=auth)
            res.encoding='utf-8'
            res_text = json.loads(res.text)
        except Exception as e:
            print(e)

        return {
            'response': res,
            'response_text': res_text,
            'from_text': res_text['resultset']['result']['information']['text-s'],
            'to_text': res_text['resultset']['result']['information']['text-t']
        }


if __name__ == '__main__':
    """test"""

    # Textraパラメーター（事前に取得してください。）
    NAME = ''
    API_KEY = ''
    API_SECRET = ''
    URL = 'https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt_standard/get/'

    # Textraオブジェクト取得
    textra = TexTra(name=NAME, api_key=API_KEY, api_secret=API_SECRET, url=URL, type='json')
    
    # 翻訳結果取得
    res = textra.translate(src_lang='ja', dest_lang='en', text='あなたは誰ですか？')

    # 翻訳後のテキストを出力
    print(res['to_text'])
