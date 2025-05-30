from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import MusicGenMain

# /docs 혹은 /redoc 에서 API 문서 확인 가능
app = FastAPI(title="Music Generation API",
              description="Can Generate Music either with given text, melody or video",
              contact={
                  "name":"Duck",
                  "email":"duck@sbs.co.kr"
              })

origins = [
    "http://10.10.123.65:1004"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 임시 파일 저장 디렉토리
TEMP_DIR = "temp"
OUTPUT_DIR = "outputs"

# 디렉토리가 없으면 생성
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/generate-basic/")
async def generate_basic(description: str = Form(...), duration: float = Form(...)):
    """텍스트 설명을 기반으로 음악 생성"""
    output_name = f"{OUTPUT_DIR}/{uuid.uuid4()}"
    
    MusicGenMain.MusicGenerate(description, duration, output_name)
    
    return FileResponse(f"{output_name}.wav", media_type="audio/wav", filename=f"generated_music.wav")

@app.post("/generate-with-melody/")
async def generate_with_melody(description: str = Form(...), duration: float = Form(...), melody: UploadFile = File(...)):
    """주어진 멜로디와 텍스트 설명을 기반으로 음악 생성"""
    # 업로드된 멜로디 파일 저장
    melody_path = f"{TEMP_DIR}/{uuid.uuid4()}.wav"
    with open(melody_path, "wb") as f:
        f.write(await melody.read())
    
    output_name = f"{OUTPUT_DIR}/{uuid.uuid4()}"
    
    MusicGenMain.MusicGenerateWithMelody(description, duration, melody_path, output_name)
    
    # 임시 파일 삭제
    os.remove(melody_path)
    
    return FileResponse(f"{output_name}.wav", media_type="audio/wav", filename=f"generated_music_with_melody.wav")

@app.post("/bgm-from-video/")
async def bgm_from_video(video: UploadFile = File(...)):
    """비디오를 파악해 분위기에 맞는 BGM 생성"""
    # 업로드된 비디오 파일 저장
    video_path = f"{TEMP_DIR}/{uuid.uuid4()}.mp4"
    with open(video_path, "wb") as f:
        f.write(await video.read())
    
    output_name = f"{OUTPUT_DIR}/{uuid.uuid4()}"
    
    MusicGenMain.bgmGenerateWithVideo(video_path, output_name)
    
    # 임시 파일 삭제
    os.remove(video_path)
    
    return FileResponse(f"{output_name}.wav", media_type="audio/wav", filename=f"video_bgm.wav")

@app.post("/bgm-from-video-with-melody/")
async def bgm_from_video_with_melody(video: UploadFile = File(...),melody: UploadFile = File(...)):
    """비디오를 파악해 분위기에 맞는 사용자 멜로디기반 BGM 생성"""
    # 업로드된 파일들 저장
    video_path = f"{TEMP_DIR}/{uuid.uuid4()}.mp4"
    with open(video_path, "wb") as f:
        f.write(await video.read())
    
    melody_path = f"{TEMP_DIR}/{uuid.uuid4()}.wav"
    with open(melody_path, "wb") as f:
        f.write(await melody.read())
    
    output_name = f"{OUTPUT_DIR}/{uuid.uuid4()}"
    
    MusicGenMain.bgmGenerateWithVideoAndMelody(video_path, melody_path, output_name)
    
    # 임시 파일 삭제
    os.remove(video_path)
    os.remove(melody_path)
    
    return FileResponse(f"{output_name}.wav", media_type="audio/wav", filename=f"video_bgm_with_melody.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4820)
