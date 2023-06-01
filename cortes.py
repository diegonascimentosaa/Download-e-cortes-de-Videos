from moviepy.editor import VideoFileClip, TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from pytube import YouTube
import os


def split_video_by_duration():
    video_url = input("Digite a URL do vídeo: ")
    video_name = input("Digite o nome do vídeo: ")
    # Baixar o vídeo do YouTube
    youtube = YouTube(video_url)
    # Filtrar streams em formato mp4 e qualidade média (720p)
    stream = youtube.streams.filter(file_extension='mp4', res='720p').first()
    video_path = stream.download('videos', filename=f'{video_name}.mp4')

    video = VideoFileClip(video_path)

    # Redimensionar o vídeo
    video = video.resize(height=1920)

    # Recortar o vídeo
    x1 = 1166.6
    y1 = 0
    x2 = 2246.6
    y2 = 1920
    video = video.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # Obter a duração do vídeo em segundos
    video_duration = video.duration

    # Verificar se a duração do vídeo é menor que quarenta segundos
    if video_duration < 40:
        print("O vídeo é menor que um minuto. Nenhuma divisão é necessária.")
        return

    # Calcular o número de partes com base na duração do vídeo
    num_parts = int(video_duration / 40)

    # Verificar se há uma parte final com duração menor que o tamanho especificado
    remaining_duration = video_duration - (num_parts * 40)
    if remaining_duration > 0 and remaining_duration < 40:
        num_parts += 1

    # Criar a pasta "cortes" se ela não existir
    if not os.path.exists("cortes"):
        os.makedirs("cortes")

    # Carregar a imagem do logo
    logo = ImageClip("logo/logo.png")  # Substitua "logo.png" pelo caminho para a sua imagem de logotipo

    # Ajustar o tamanho do logo
    logo = logo.resize(height=300)  # Ajuste a altura conforme necessário

    # Posicionar o logo no canto superior direito
    logo = logo.set_position(("right", "top"))

    # Dividir o vídeo em partes iguais e adicionar o texto correspondente e o logo a cada parte
    parts = []
    for i in range(num_parts):
        start_time = i * 40
        end_time = min((i + 1) * 40, video_duration)
        part = video.subclip(start_time, end_time)

        # Adicionar texto à parte do vídeo
        text = f"Parte {i+1}"
        text_clip = TextClip(text, fontsize=200, font='Arial', color='yellow', bg_color='gray',
                             stroke_color='gray', stroke_width=2, method='caption')
        text_clip = text_clip.set_position(('center', 'bottom')).set_duration(part.duration)

        # Adicionar o logo à parte do vídeo
        video_with_text = CompositeVideoClip([part, text_clip])
        video_with_text = CompositeVideoClip([video_with_text, logo.set_start(0).set_duration(part.duration)])

        parts.append(video_with_text)

    # Salvar as partes divididas na pasta "cortes"
    for i, part in enumerate(parts):
        output_path = os.path.join("cortes", f"{video_name}_parte_{i+1}.mp4")
        part.write_videofile(output_path, codec="libx264")

    print(f"O vídeo foi dividido em {num_parts} partes.")


# Exemplo de uso:
split_video_by_duration()
