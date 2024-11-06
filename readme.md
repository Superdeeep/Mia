<div align="center">

# VTuber Mia

> 孩子不懂事，一通乱写的。

</div>
## quick start :

## About src:

main.py 
vtube_control.py
llm.py

## About Mia:





```bash
conda create -n Mia python=3.10

conda activate Mia

python.exe -m pip install --upgrade pip

pip install realtimetts[coqui]

ollama run gemma2:2b

pip install ollama 

pip install websockets

中文：pip install pypinyin

pip install torch==2.3.1+cu118 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118
```


Fix for to resolve compatility issues: If you run into library compatility issues, try setting these libraries to fixed versions:
修复以解决兼容性问题：如果遇到库兼容性问题，请尝试将这些库设置为修复版本：

```bash
pip install networkx==2.8.8
pip install typing_extensions==4.8.0
pip install fsspec==2023.6.0
pip install imageio==2.31.6
pip install networkx==2.8.8
pip install numpy==1.24.3
pip install requests==2.31.0
```

xiaolingyun:
pip install SpeechRecognition
pip install textblob
pip install pocketsphinx

