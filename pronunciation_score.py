# pronunciation_score.py
import whisper
import numpy as np
import librosa
import Levenshtein
from dtw import dtw

# load model once
model = whisper.load_model("small")

def transcribe(audio_path):
    res = model.transcribe(audio_path, language="so")
    return res["text"].lower().strip()

def levenshtein_score(ref, hyp):
    if not ref and not hyp: return 1.0
    dist = Levenshtein.distance(ref, hyp)
    max_len = max(len(ref), len(hyp), 1)
    return max(0, 1 - dist/max_len)

def mfcc_score(ref_path, hyp_path):
    a1, sr1 = librosa.load(ref_path, sr=16000)
    a2, sr2 = librosa.load(hyp_path, sr=16000)
    mf1 = librosa.feature.mfcc(a1, sr1).T
    mf2 = librosa.feature.mfcc(a2, sr2).T
    dist, _, _, _ = dtw(mf1, mf2, dist=lambda x,y: np.linalg.norm(x-y))
    return float(np.exp(-dist/200))

def grade_attempt(ref_audio_path, ref_text, user_audio_path):
    user_transcript = transcribe(user_audio_path)
    lex = levenshtein_score(ref_text.lower(), user_transcript)
    try:
        acoustic = mfcc_score(ref_audio_path, user_audio_path)
    except Exception:
        acoustic = 0.0
    final = 0.6 * lex + 0.4 * acoustic
    return {
        "score": int(round(final * 100)),
        "transcript": user_transcript,
        "components": {
            "lexical": round(lex, 3),
            "acoustic": round(acoustic, 3)
        }
    }
