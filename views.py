from django.http import HttpResponse
from django.shortcuts import render
from moviepy.editor import AudioFileClip
import os
from tempfile import NamedTemporaryFile


def convert_mp4_to_mp3(request):
    if request.method == 'POST':
        file = request.FILES['file']

        try:
            # Create a NamedTemporaryFile object to save the uploaded file
            with NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()

                # Create an AudioFileClip object from the uploaded file
                with AudioFileClip(temp_file.name) as clip:
                    # Create the output file path with the same name and .mp3 extension
                    file_name, extension = os.path.splitext(temp_file.name)
                    mp3_file_path = f"{file_name}.mp3"

                    # Write the audio of the clip to the output file
                    clip.write_audiofile(mp3_file_path)

            # Open the MP3 file as a binary file and return it as a response
            with open(mp3_file_path, 'rb') as mp3_file:
                response = HttpResponse(mp3_file.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(mp3_file_path)
                return response

        except Exception as e:
            return HttpResponse('Error occurred: {}'.format(str(e)))
        finally:
            # Delete the temporary file and the output file
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
            if os.path.exists(mp3_file_path):
                os.remove(mp3_file_path)

    return render(request, 'converter.html')
