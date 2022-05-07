# UpSpeech - Backend (Flask)

## Get to python environment first
`source YOUR_PATH/upspeech-flask/venv/bin/activate`

## Install

- Paste Google service account json credentials to a file name `upspeech-firebase-key.json`
- Install the required dependencies
<code>
pip install -r requirements.txt
</code>
<br/>
<br/>

## Run
- Run flask server
<code>
python -m flask run
</code>
<br/>
<br/>

- Local run for testing
<code>
python run_audio.py

python run_emotion.py
</code>
<br/>
<br/>

- Modify `run_audio.py` and `run_emotion.py` content to suit your need
