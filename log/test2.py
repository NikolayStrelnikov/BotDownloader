## ВИДЕО
## --------------------------------------------------------------------
async def download_video(message, audio=False, format_id="mp4"):
    await check_url(message)

    url_info = urlparse(message.text)
    if url_info.scheme:
        msg = await message.reply(message, 'Downloading...')
        unique_filename = str(uuid.uuid4())
        url = message.text

        with YoutubeDL(
                {'format': format_id,
                 'outtmpl': f'downloads/{unique_filename}.%(ext)s',
                 'postprocessors': [{  # Extract audio using ffmpeg
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
        }] if audio else [], 'max_filesize': config.max_filesize}) as ydl:
            info = ydl.extract_info(url, download=True)

            try:
                message.edit_text('Sending file to Telegram...')
                try:
                    if audio:
                        message.send_audio(message.chat.id, open(
                            info['requested_downloads'][0]['filepath'], 'rb'), reply_to_message_id=message.message_id)

                    else:
                        width = info['requested_downloads'][0]['width']
                        height = info['requested_downloads'][0]['height']

                        message.send_video(message.chat.id, open(
                            info['requested_downloads'][0]['filepath'], 'rb'), reply_to_message_id=message.message_id,
                                       width=width, height=height)
                    message.delete_message(message.chat.id, msg.message_id)
                except Exception:
                    message.edit_text(f"Couldn't send file, make sure it's supported by Telegram "
                                      f"and it doesn't exceed *{round(config.max_filesize / 1000000)}MB*",
                                        parse_mode="MARKDOWN")

            except Exception as e:
                if isinstance(e, DownloadError):
                    message.edit_text('Invalid URL')
                else:
                    message.edit_text(f"There was an error downloading your video, "
                                      f"make sure it doesn't exceed *{round(config.max_filesize / 1000000)}MB*",
                                        parse_mode="MARKDOWN")

    else:
        await message.reply(message, 'Invalid URL')


## --------------------------------------------------------------------
## ВИДЕО