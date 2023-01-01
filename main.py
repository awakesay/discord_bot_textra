
import os
import json
from typing import Union    
from functools import cache
import discord
from wrapped_textra import WrappedTextra

def run_bot(jp_speakers_id: list[int], en_speakers_id: list[int]):

    intents = discord.Intents.all()
    
    bot = discord.Bot(intents=intents)

    @bot.event
    async def on_ready():
        """起動メッセージ"""
        print('on_ready')
        print(f'version: {discord.__version__}')

    @bot.listen('on_message')
    async def on_message(message):
        """メッセージ投稿ハンドラー"""
        if message.author.bot:
            return  # ボットの投稿は無視（早期リターン）
        
        # 翻訳方向セット
        if (id := message.author.id) in jp_speakers_id:
            from_lang, to_lang = 'ja', 'en'
        elif id in en_speakers_id:
            from_lang, to_lang = 'en', 'ja'
        else:
            return  # 指定ユーザー以外は無視（早期リターン）

        # Textraオブジェクト取得
        trans = WrappedTextra()
        # 翻訳
        trans_text = trans.translate(from_lang, to_lang, message.content)
        # 再翻訳
        retrans_text = trans.translate(to_lang, from_lang, trans_text['to_text'])

        # 投稿メッセージ取得
        embed_description = '\n'.join([
            f"{from_lang}->{to_lang}: {trans_text['to_text']}",
            f"{to_lang}->{from_lang}: {retrans_text['to_text']}"
        ])

        # 投稿
        embed = discord.Embed(description=embed_description, colour=discord.Colour.blurple())
        await message.channel.send(embed=embed)

    bot.run(get_config_json('discord_bot')['token'])


@cache  # キャッシュによる高速化
def get_config_json(name: str) -> Union[list, dict]:
    """configフォルダ内の設定を取得して返します。"""
    path = f'{os.path.abspath(os.path.dirname(__file__))}/config/{name}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':

    speakers = get_config_json('speakers')
    run_bot(
        jp_speakers_id=speakers['jp'],
        en_speakers_id=speakers['en']
    )
