# BGM Generation with Video Input   
AI BGM Generator using some state of the art open sources and wrapping it in Rest API.  

It'sexpected to be used as a BGM Generator for SBS with PDS which is the main content producing system in SBS.  
  
It uses Meta's [Audiocraft](https://github.com/facebookresearch/audiocraft) as a main music generation model, and [LLaVA](https://huggingface.co/llava-hf/LLaVA-NeXT-Video-7B-hf) as a main video processor.    
Also, for optional uses like manual description input, it uses [Dl Translate](https://github.com/xhluca/dl-translate) to deal with Korean input which is expected most common input language in SBS.  

## How to use
### requirements
python and dependencies. It needs to be `python=3.9` but not really have to be in a conda environment.  
``` shell
conda create -n [ENV_NAME] python=3.9
conda activate [ENV_NAME]
```
``` shell
pip install numpy==1.26.4  # numpy<2
pip install 'torch==2.1.0'
pip install setuptools wheel
pip install -U audiocraft
pip install dl-translate
# Below is to host REST API, so do it only when you need it
pip install fastapi uvicorn python-multipart
```
ffmpeg
``` shell
sudo apt install ffmpeg
```

### Run and use API
```shell
nohup python MusicGenAPI.py
```
*All the core functions are defined in MusicGenAPI.py*  
*You can basically use these without using RestAPI*  

