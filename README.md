# Whisper Bangla — অডিও থেকে বাংলা টেক্সট ও সাবটাইটেল

OpenAI Whisper দিয়ে যেকোনো অডিও (mp3/wav/flac) থেকে বাংলা টেক্সট বের করুন, সাথে SRT সাবটাইটেল ফাইল। Built on **openai/whisper**.

- **Original repo:** https://github.com/openai/whisper (robust speech recognition — audio to text, many languages including Bangla)

## কী আছে / What is inside

- `transcribe-bangla.py` — ট্রান্সক্রিপশন স্ক্রিপ্ট: `--language bn` ডিফল্ট, `--model` দিয়ে base/small বাছা যায়, আউটপুট `.txt` + `.srt`। `py_compile` যাচাই করা।
- `requirements.txt` — শুধু `openai-whisper` (আপস্ট্রিমের অফিসিয়াল প্যাকেজ)।

## যা ঠিক করা হয়েছে / What was fixed

- আপস্ট্রিমের CLI-তে ভাষা লিখতে হয় প্রতিবার (`whisper audio.mp3 --language bn`)। এই স্ক্রিপ্টে বাংলা ডিফল্ট — শুধু ফাইলের নাম দিলেই হয়।
- আপস্ট্রিম CLI একসাথে অনেক আউটপুট ফরম্যাট দেয়; এখানে শুধু যা দরকার — বাংলা টেক্সট (`.txt`) আর সাবটাইটেল (`.srt`)।
- মডেল সাইজ আর্গুমেন্ট দিয়ে বাছা যায় — ছোট মেশিনে `base`, ভালো নির্ভুলতার জন্য `small`।

## ব্যবহার / How to use

```bash
# 1. ffmpeg লাগবে (আপস্ট্রিমের প্রয়োজনীয়তা)
sudo apt update && sudo apt install ffmpeg

# 2. ইনস্টল করুন
pip install -r requirements.txt

# 3. ট্রান্সক্রাইব করুন (base মডেল, বাংলা)
python3 transcribe-bangla.py audio.mp3 --model base

# ভালো নির্ভুলতার জন্য small মডেল
python3 transcribe-bangla.py audio.mp3 --model small

# আউটপুট অন্য ফোল্ডারে
python3 transcribe-bangla.py audio.mp3 --model base --output-dir out/
```

আউটপুট: `audio.txt` (পুরো বাংলা টেক্সট) আর `audio.srt` (সময়সহ সাবটাইটেল) — ইনপুট ফাইলের পাশে তৈরি হয়।

## নোট

- প্রথমবার চালালে মডেল ডাউনলোড হবে (~১৪০ MB base, ~৪৬০ MB small) — ইন্টারনেট লাগবে।
- `tiny` মডেলও চলে (`--model tiny`), তবে বাংলা নির্ভুলতা কম।
- GPU থাকলে Whisper নিজে থেকে ব্যবহার করবে; না থাকলে CPU-তেই চলবে, একটু ধীরে।
