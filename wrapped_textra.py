
import os
import json
from typing import Union
from functools import cache
from textra import TexTra

"""
textraモジュールのTextraクラスのラッパーです。
Textraクラスを継承してパラメーターをセットしているだけです。
"""

class WrappedTextra(TexTra):

    def __init__(self):

        # パラメーター取得
        param = get_config_json('textra_param')

        # 親クラスにパラメーターをセット
        super().__init__(
            name=param['name'],
            api_key=param['api_key'],
            api_secret=param['api_secret'],
            url=param['url']
        )


@cache  # キャッシュによる高速化
def get_config_json(name: str) -> Union[list, dict]:
    """configフォルダ内の設定を取得して返します。"""
    path = f'{os.path.abspath(os.path.dirname(__file__))}/config/{name}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    """test"""

    # Textraオブジェクト取得（パラメーターは自動セット）
    wt = WrappedTextra()

    # 翻訳結果取得
    res = wt.translate('ja', 'en', '私の名前はうんこマンです。')

    # 翻訳後のテキストを出力
    print(res['to_text'])








