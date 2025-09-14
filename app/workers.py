import os
import uuid
from datetime import datetime
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from yt_dlp import YoutubeDL
import database.requests as db
from collections import defaultdict
import app.keyboards as kb

def get_video_info(url: str):
    ydl_opts = {'quiet': True,
                'no_warnings': True,
                'no_color': True}

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            video_format_groups = defaultdict(list)
            audio_formats = []

            for f in info['formats']:
                height = f.get('height')
                file_size_bytes = f.get('filesize')

                if file_size_bytes:
                    if height is not None:
                        video_format_groups[height].append(f)
                    else:
                        audio_formats.append(f)

            best_formats = []
            format_options = []

            if audio_formats:
                best_audio_format = max(audio_formats, key=lambda x: x.get('abr', 0))
                file_size_mb = round(best_audio_format['filesize'] / (1024 * 1024), 2)
                best_formats.append(f'🎶  Audio {file_size_mb}MB')
                format_options.append(best_audio_format['format_id'])

            for height, group in video_format_groups.items():
                best_format = max(group, key=lambda x: x.get('tbr', 0))
                file_size_mb = round(best_format['filesize'] / (1024 * 1024), 2)
                best_formats.append(f'🎞  Video {height}p {file_size_mb}MB')
                format_options.append(best_format['format_id'])

            print(f"ИНФО: {title}, {best_formats}")
            return title, best_formats, format_options

        except Exception as e:
            print(f"Error extracting video info: {e}")
            return None, None, None


async def select_format(message: Message):
    reply = await message.reply(text='Get Video Info...')
    url = message.text
    title, best_formats, format_options = get_video_info(url)
    if title and best_formats:
        await message.answer(f'{title}\n\n Выберите формат и качество:',
                             reply_markup=await kb.categories(formats=best_formats, options=format_options, url=url))
    else:
        await message.answer("Не удалось получить информацию о видео.")
    await reply.delete()




    # file_id = await db.get_file_id(file_url=message.text)
    # if file_id:
        # try:
            # await message.answer_video(video=file_id)
            # return
        # except TelegramBadRequest as e:
            # Логирование ошибки может помочь в отладке
            # print(f"Error sending video: {e}")
            # pass

    # Вызов download_proc, если файл не найден или возникла ошибка
    # await download_proc(message, audio=False)


async def download_process(message: Message, format_id: str, url: str):
    video_file_path = None
    reply = await message.reply(text='Downloading...')
    video_title = str(uuid.uuid4())

    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',  # Выбор формата с видео и аудио
        'outtmpl': f'downloads/{video_title}.%(ext)s',
         'postprocessors': [{  # Extract audio using ffmpeg
             'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', }] if audio else [],
        'quiet': True,
        'no_warnings': True,
        'no_color': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # ----------------------------------------------------------------------------------------
        # with YoutubeDL(
        #         {'format': 'best',  # Используйте 'best' для загрузки лучшего доступного качества
        #          'outtmpl': f'downloads/{video_title}.%(ext)s',
        #          'postprocessors': [{  # Extract audio using ffmpeg
        #              'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', }] if audio else [],
        #          'max_filesize': os.getenv('MAX_FILE'),
        #          # 'logger' : logger, # тут надо подумать, вероятно тупит
        #          'quiet': True  # без вывода в консоль
        #          }
        # ) as ydl:
        #     info = ydl.extract_info(url, download=True)
        #     height = info['height']

        # Найти скачанный файл
        for file in os.listdir('downloads'):
            if file.startswith(video_title):
                video_file_path = os.path.join('downloads', file)
                break
        if not video_file_path:
            await reply.edit_text('Не удалось скачать видео')
            return

        video_file = FSInputFile(video_file_path)

        await reply.edit_text(text='Sending file to Telegram...')
        # video_message = await message.answer_video(video=video_file, width=width, height=height)
        video_message = await message.answer_video(video=video_file)
        await reply.delete()

        # Добавляем в базу информацию о файле, если такого URL не было
        await db.set_link(user_id=message.from_user.id,
                          file_url=url,
                          v_format= format_id,
                          file_id=video_message.video.file_id,
                          date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                          )

    except Exception as e:
        await reply.edit_text(f'Произошла ошибка: {e}')

    finally:
        # Удаляем файл в любом случае, если он был скачан
        if video_file_path and os.path.exists(video_file_path):
            os.remove(video_file_path)

