from yt_dlp import YoutubeDL
from collections import defaultdict

def get_video_info(url: str):
    ydl_opts = {'quiet': True, 'no_warnings': True, 'no_color': True}

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            video_format_groups = defaultdict(list)
            audio_formats = []

            # Разделяем форматы на видео и аудио
            for f in info['formats']:
                height = f.get('height')
                file_size_bytes = f.get('filesize')

                if file_size_bytes:
                    if height is not None:  # Видео формат
                        video_format_groups[height].append(f)
                    else:  # Аудио формат
                        audio_formats.append(f)

            best_formats = []

            # Выбираем лучший аудио формат
            if audio_formats:
                best_audio_format = max(audio_formats, key=lambda x: x.get('abr', 0))  # Выбираем по наибольшему abr
                file_size_mb = round(best_audio_format['filesize'] / (1024 * 1024), 2)
                best_formats.append(f'Audio {file_size_mb}MB')

            # Выбираем лучший видео формат из каждой группы по разрешению
            for height, group in video_format_groups.items():
                best_format = max(group, key=lambda x: x.get('tbr', 0))  # Выбираем по наибольшему tbr
                file_size_mb = round(best_format['filesize'] / (1024 * 1024), 2)
                best_formats.append(f'Video {height}p {file_size_mb}MB')

            print(f"ИНФО: {title}, {best_formats}")
            return title, best_formats

        except Exception as e:
            print(f"Error extracting video info: {e}")
            return None, None

# Пример вызова функции
url = "https://youtu.be/IPDxtclZzVU"
get_video_info(url)
