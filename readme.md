<div align="center">

# VTuber Mia

> 孩子不懂事，一通乱写的。
> 孩子不会python

</div>

[老子要看中文](https://github.com/Superdeeep/Mia/blob/main/readme_zh.md)

## ⚡️ Quick start:

> A not-so-quick quick start

You need install CUDA(11.8) and cuDNN, and then install the required packages.

I perfer to use conda to build the environment.

```bash
conda create -n Mia python=3.10

conda activate Mia

python.exe -m pip install --upgrade pip

pip install realtimetts[coqui]

ollama run gemma2:2b

pip install ollama 

pip install websockets

pip install torch==2.3.1+cu118 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

```



## About src:

```
├─models
│  └─v2.0.2->here is realtimetts[coqui] model
├─RealtimeTTS
│  ├─RealtimeTTS
│  │  └─engines
│  └─tests
│      ├─coqui_voices
│      └─models
│          └─v2.0.2
├─voice->here is the voice files,coqui can simulate the voice
llm.py
main.py
vtube_control.py
```

## About Mia:

孩子不懂事，写着玩的


## My Environment:
> If you run into library compatility issues, try setting these libraries to fixed versions:

click [here](https://github.com/Superdeeep/Mia/blob/main/pip.txt)

## TODO:

- [ ] 寻找合适的TTS
- [ ] 寻找合适的STT
- [ ] 实现不依赖ollama

## Thanks:
- [ollama](https://github.com/ollama/ollama)
- [coqui-ai](https://github.com/coqui-ai/TTS)
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS)


