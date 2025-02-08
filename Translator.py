import logging
import google.generativeai as genai
from Misc.ConfigIni import GConfig

GoogleGeminiKey = GConfig.GetItemValue("GenAI", "key")
TargetModel = GConfig.GetItemValue("GenAI", "model")
genai.configure(api_key=GoogleGeminiKey)

class Translator:
    def __init__(self):
        self.LanguageName = "None"
    def Translate(self, text):
        raise NotImplementedError("Subclasses must implement Translate()")

class KaomojiTranslator(Translator):
    def __init__(self):
        super().__init__()
        self.LanguageName = "Kaomoji"
        self.model = genai.GenerativeModel(TargetModel)
        self.chat = self.model.start_chat(history=[])
        response = self.chat.send_message(
            f"Assume that you are a translator now. You need to translate any text in any language I send to you into {self.LanguageName}. Remember you are only allowed to response with {self.LanguageName} and try to reflect the original meaning of the text I send you as much as possible. Keep doing this unless I send you '停止翻译'.")
        logging.info(f'KaomojiTranslator(): Init model({TargetModel}) with respond => {response.text}')

    def Translate(self, text):
        try:
            response = self.chat.send_message(text)
            return response.text
        except Exception as e:
            logging.error(f'KaomojiTranslator(): Exception {e}')
            return text

class EmojiTranslator(Translator):
    def __init__(self):
        super().__init__()
        self.LanguageName = "Emoji"
        self.model = genai.GenerativeModel(TargetModel)
        self.chat = self.model.start_chat(history=[])
        response = self.chat.send_message(
            f"Assume that you are a translator now. You need to translate any text in any language I send to you into {self.LanguageName}. Remember you are only allowed to response with {self.LanguageName} and try to reflect the original meaning of the text I send you as much as possible. Keep doing this unless I send you '停止翻译'.")
        logging.info(f'EmojiTranslator(): Init model({TargetModel}) with respond => {response.text}')

    def Translate(self, text):
        try:
            response = self.chat.send_message(text)
            return response.text
        except Exception as e:
            logging.error(f'EmojiTranslator(): Exception {e}')
            return text

class TranslateManager:
    def __init__(self):
        Kaomoji = KaomojiTranslator()
        Emoji = EmojiTranslator()
        self.TranslatorList = {Kaomoji.LanguageName: Kaomoji, Emoji.LanguageName: Emoji}

    def Translate(self, text, language):
        if not language:
            return text
        if language not in self.TranslatorList:
            return text
        return self.TranslatorList[language].Translate(text)


GTranslateManager = TranslateManager()