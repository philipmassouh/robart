'''# EXAMPLE USAGE

from modules.stt.record import Recorder
from modules.watson_stt import SpeechToText

s = SpeechToText()
r = Recorder()
frames, rate, channels = r.record()
r.send_to_file()
print(s.recognize_speech(frames, rate, channels))
# [{'transcript': 'Mary had a little lamb', 'confidence': 0.99}]
'''


from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException


default_key = 'R9hW3VQy4vgbFAHYoq9WWnzKoI5QioBVH9UAsWovlwVk'
default_loc = ('https://api.us-south.speech-to-text.watson.cloud.ibm.com'
               + '/instances/1aafab97-84e5-4963-8fdc-8d078b522a15')


class SpeechToText:
    # these are the credentials associated with 'massouh.3@osu.edu'
    # you may initialize the speech-to-text service with your own credentials

    def __init__(self, ssl_disable=False, key=default_key, loc=default_loc):

        authenticator = IAMAuthenticator(key)

        self.speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )

        self.speech_to_text.set_service_url(loc)

        self.speech_to_text.set_disable_ssl_verification(ssl_disable)

    def recognize_speech(self, frames, rate, channels):

        try:
            speech_recognition_results = self.speech_to_text.recognize(
                audio=frames,
                content_type=f"audio/l16;rate={rate};channels={channels}",
            ).get_result()
            return speech_recognition_results.get("results")[0]['alternatives']
        except ApiException as ex:
            print("Function failed with status code " +
                  str(ex.code) + ": " + ex.message)
        except IndexError:
            print("Nothing heard")
