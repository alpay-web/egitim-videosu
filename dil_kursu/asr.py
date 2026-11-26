import re, numpy as np, sherpa_onnx
M="/home/claude/modeller/sherpa-onnx-whisper-small.en/small.en-"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+"encoder.int8.onnx",decoder=M+"decoder.int8.onnx",tokens=M+"tokens.txt",language="en",task="transcribe",num_threads=2)
def n(t): return re.sub(r"[^a-z ]"," ",t.lower().replace("analyze","analyse").replace("-"," ")).split()
def duy(x,sr=24000):
    z=np.zeros(int(.8*sr),np.float32); s=rec.create_stream(); s.accept_waveform(sr,np.concatenate([z,x.astype(np.float32),z])); rec.decode_stream(s); return s.result.text
def dogru_mu(metin,x): return n(duy(x))==n(metin)
