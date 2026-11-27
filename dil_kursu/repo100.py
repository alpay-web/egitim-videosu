import csv,sys
st={}
for f in ["repolar.tsv","repolar2.tsv"]:
    for r in csv.reader(open(f),delimiter="\t"):
        if len(r)>2:
            try: st[r[1].lower()]=max(st.get(r[1].lower(),0),int(r[2]))
            except: pass
K={
"Aralıklı tekrar ve hafıza":"ankitects/anki ankidroid/Anki-Android open-spaced-repetition/fsrs4anki open-spaced-repetition/py-fsrs open-spaced-repetition/ts-fsrs open-spaced-repetition/fsrs-rs open-spaced-repetition/fsrs-optimizer open-spaced-repetition/srs-benchmark open-spaced-repetition/free-spaced-repetition-scheduler open-spaced-repetition/awesome-fsrs duolingo/halflife-regression andymatuschak/orbit st3v3nmw/obsidian-spaced-repetition eudoxia0/hashcards olmps/memo kerrickstaley/genanki FooSoft/anki-connect tianshanghong/awesome-anki designfuchen/word-atlas Ecattea/COCA-English-Anki-Deck",
"Edinim, girdi ve dinleme":"Vuizur/awesome-language-learning IvanovCosmin/awesome-natural-approach jtauber/graded-reader FreeLanguageTools/vocabsieve arianneorpilla/jidoujisho umlx5h/LLPlayer Ajatt-Tools/mpvacious Ajatt-Tools/impd kantord/LibreLingo cuixueshe/earthworm mengxi-ream/read-frog chickendude/Natibo elonbing/PimSched Talljack/echo-type baturyilmaz/wordpecker-app tigertv/language-learning JonathanLaneMcDonald/ML_for_SLA artcc/freelingo xiao-zaiyi/illa-helper jqhoogland/awesome-language-learning",
"Seviye, kelime ve okunabilirlik":"rspeer/wordfreq Maximax67/cefrpy Maximax67/Words-CEFR-Dataset openlanguageprofiles/olp-en-cefrj AMontgomerie/CEFR-English-Level-Predictor yukiar/CEFR-SP textstat/textstat LSYS/LexicalRichness explosion/spaCy InternetEnzyme/textmeter-ngsl cmusphinx/cmudict KyleBing/english-vocabulary",
"Konuşma, telaffuz ve ses":"openai/whisper SYSTRAN/faster-whisper k2-fsa/sherpa-onnx snakers4/silero-vad thewh1teagle/kokoro-onnx resemble-ai/chatterbox MontrealCorpusTools/Montreal-Forced-Aligner MahmoudAshraf97/ctc-forced-aligner jianfch/stable-ts xinjli/allosaurus YuanGongND/gopt bootphon/phonemizer m-bain/whisperX OpenPronounce/OpenPronounce tbright17/kaldi-dnn-ali-gop cageyoko/CTC-Attention-Mispronunciation learnercraft/ispeakerreact",
"Yazma ve dilbilgisi değerlendirme":"languagetool-org/languagetool grammarly/gector nusnlp/m2scorer keisks/jfleg google-research-datasets/clang8 michiyasunaga/LM-Critic nusnlp/nea araloak/ieltsGPT",
"Öğrenen modelleme ve ölçme":"pykt-team/pykt-toolkit CAHLR/pyBKT chrispiech/DeepKnowledgeTracing bigdata-ustc/EduKTM bigdata-ustc/EduCDM bigdata-ustc/EduCAT douglasrizzo/catsim philchalmers/mirt philchalmers/mirtCAT eribean/girth jilljenn/ktm CAHLR/OATutor",
"Öğrenme bilimi, yapay zekâ öğretmen ve IELTS":"GarethManning/education-agent-skills nagisanzenin/engram jtangen/classbuild luffycodes/Tutorbot-Spock Geralt-Targaryen/Awesome-Education-LLM GeminiLight/gen-mentor hubeiqiao/IELTS-Speaking-Simulator shah0150/awesome-IELTS sallowayma-git/IELTS-practice mcxiaoxiao/openIELTS hefengxian/my-ielts",
}
out=[];n=0;eksik=[]
for k,v in K.items():
    for r in v.split():
        n+=1; s=st.get(r.lower())
        if s is None: eksik.append(r)
        out.append((k,r,s))
print(n, "eksik:",eksik)
import json; json.dump(out,open("/home/claude/kurs/repo100.json","w"))
