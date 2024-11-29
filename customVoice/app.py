from flask import Flask, request, Response
import io
import requests
from pydub import AudioSegment
app = Flask(__name__)



def convert_mp3_to_pcm(input_file, sample_rate=16000):
    try:
        # Load the MP3 file
        audio = AudioSegment.from_file(input_file, format="mp3")
        
        # Set to 1 channel (mono) and desired sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(sample_rate)
        
        # Export audio as raw PCM in-memory
        pcm_audio = io.BytesIO()
        audio.export(pcm_audio, format="s16le")
        pcm_audio.seek(0)
        
        return pcm_audio
    except Exception as e:
        raise RuntimeError(f"Error during conversion: {e}")




@app.route('/voice', methods=['POST'])
def handle_voice_request():
    try:
        # Parse the incoming JSON data
        data = request.json
        # print("Received request data:", data)
        text = data.get("message", {}).get("text", "No text provided")
        print(text)
        # convert_to_mp3(text)
        pcm_audio = convert_mp3_to_pcm(input_file="response.mp3")

        return Response(
            pcm_audio.read(),
            mimetype='audio/raw',  # MIME type for raw PCM
            headers={
                'Content-Disposition': 'inline; filename="response.pcm"',
                'Content-Type': 'audio/raw',
            }
        )


    except Exception as e:
        print("Error handling request:", str(e))
        return {"error": "Invalid request"}, 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)
