<div align="center">

# VTuber Mia

> 孩子不懂事，一通乱写的。
> 孩子不会python

</div>


## ⚡️ 搞快点搞快点:

> 但是并不快

装好CUDA（11.8）和cuDNN，然后安装所需的包。

我用conda搭的虚拟环境。

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



## 关于代码:

```
├─models
│  └─v2.0.2->放realtimetts[coqui] 的语音模型
├─RealtimeTTS
│  ├─RealtimeTTS
│  │  └─engines
│  └─tests
│      ├─coqui_voices
│      └─models
│          └─v2.0.2
├─voice->coqui模拟声音的文件们
llm.py
main.py
vtube_control.py
```

## 关于妙芽:

孩子不懂事，写着玩的


## 我的环境长啥样？:
> If you run into library compatility issues, try setting these libraries to fixed versions:

click [here](https://github.com/Superdeeep/Mia/blob/main/pip.txt)

## 待办事项:
- [ ] 寻找合适的TTS
- [ ] 寻找合适的STT
- [ ] 实现不依赖ollama

## 谢谢您:
- [ollama](https://github.com/ollama/ollama)
- [coqui-ai](https://github.com/coqui-ai/TTS)
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS)