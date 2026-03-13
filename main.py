import streamlit as st
import yt_dlp
import os

st.title("YouTube MP3/MP4 ダウンローダー")

url = st.text_input("YouTubeのURLを貼り付けてください", placeholder="https://www.youtube.com/watch?v=...")

option = st.selectbox("保存形式を選んでください", ("mp3 (音声のみ)", "mp4 (動画)"))

if st.button("変換・準備開始"):
    if url:
        with st.spinner("処理中... 少々お待ちください"):
            try:
                ydl_opts = {
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                    'format': 'bestaudio/best' if option == "mp3 (音声のみ)" else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'nocheckcertificate': True,
                }

                if option == "mp3 (音声のみ)":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if option == "mp3 (音声のみ)":
                        filename = filename.rsplit('.', 1)[0] + '.mp3'

                with open(filename, "rb") as f:
                    st.success("準備ができました！")
                    st.download_button(
                        label="ファイルを保存する",
                        data=f,
                        file_name=f"{info['title']}.{'mp3' if option == 'mp3 (音声のみ)' else 'mp4'}",
                        mime="audio/mpeg" if option == "mp3 (音声のみ)" else "video/mp4"
                    )
                
                os.remove(filename)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:

        st.warning("URLを入力してください")
