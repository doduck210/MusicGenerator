# referring https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import Modules.DlTranslator as Translator
import Modules.VideoDescription as VideoDescription

def MusicGenerateBasic(description, duration, outputName):
    description = [Translator.translator(description)]
    print(description)

    model = MusicGen.get_pretrained('facebook/musicgen-melody')
    model.set_generation_params(duration=duration)
    # top_K : 클수록 다양성(창의성), 작을수록 반복적이고 결정적
        # 잠재적 토큰중 확률에 따라 순위를 매기고 이 목록에서 상위 K개의 토큰 선택
    # top_q : top_k가 고정된 숫자, q는 순위 매겨진 토큰의 누적 확률 분포 고려.
        # 기본값 0 일떄는 k사용
    # temperature : 이것도 높을수록 출력의 무작위성 증가
    wav = model.generate(description)

    for idx, one_wav in enumerate(wav):
        # Will save under {outputName}.wav, with loudness normalization at -22 dbW LUFS which is maximum of TV Protocol.
        audio_write(outputName, one_wav, model.sample_rate, strategy="loudness", loudness_headroom_db=22, loudness_compressor=True)

def MusicGenerateWithMelody(description,duration,melody,outputName):
    description = [Translator.translator(description)]
    description=[description]
    print(description)

    model = MusicGen.get_pretrained('facebook/musicgen-melody')
    model.set_generation_params(duration=duration)

    melody, sr = torchaudio.load(melody)
    wav=model.generate_with_chroma(description,melody,sr)

    for idx, one_wav in enumerate(wav):
        audio_write(outputName, one_wav, model.sample_rate, strategy="loudness", loudness_headroom_db=22, loudness_compressor=True)

def bgmGenerateWithVideo(inputVideo,outputName):
    duration, description = VideoDescription.BGMPromptGenerator(inputVideo)
    MusicGenerateBasic(description,duration,outputName)

def bgmGenerateWithVideoAndMelody(inputVideo,melody,outputName):
    duration, description = VideoDescription.BGMPromptGenerator(inputVideo)
    MusicGenerateWithMelody(description,duration,melody,outputName)

if __name__ == "__main__":
    bgmGenerateWithVideo('./assets/graduation.mp4','./output')
