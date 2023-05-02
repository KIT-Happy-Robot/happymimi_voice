from pathlib import Path
import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore
from playsound import playsound

SPEAKER_ID = 8

#　四国めたん   ・ノーマル : 2  ・あまあま : 0  ・ツンツン : 6  ・セクシー : 4
#  ずんだもん   ・ノーマル : 3  ・あまあま : 1  ・ツンツン : 7  ・セクシー : 5
#  春日部つむぎ ・ノーマル : 8
#  雨晴はう     ・ノーマル : 10
#  波音リツ     ・ノーマル : 9
#  玄野武宏     ・ノーマル : 11
#  白上虎太郎   ・ノーマル : 12
#  青山龍星     ・ノーマル : 13
#  冥鳴ひまり   ・ノーマル : 14
#  九州そら     ・ノーマル : 16 ・あまあま : 15 ・ツンツン : 18 ・セクシー : 17 ・ささやき : 19

open_jtalk_dict_dir = './open_jtalk_dic_utf_8-1.11'
text = "who are you"
out = Path('output.wav')
acceleration_mode = AccelerationMode.AUTO

def main() -> None:
    core = VoicevoxCore(
        acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
    )
    core.load_model(SPEAKER_ID)
    audio_query = core.audio_query(text, SPEAKER_ID)
    wav = core.synthesis(audio_query, SPEAKER_ID)
    out.write_bytes(wav)
    playsound(out)


if __name__ == "__main__":
    main()
