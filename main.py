import FreeSimpleGUI as sg
from ytmusicapi import YTMusic
import vlc
import yt_dlp

sg.theme("DarkGreen4")
ytmusic = YTMusic()

def Title(Song):
    search = ytmusic.search(Song, "songs", None, 1, False)
    return str(search[0]['title'])

def findLink(Song):
    search = ytmusic.search(Song, "songs", None, 1, False)
    Link = "https://youtube.com/watch?v=" + str(search[0]['videoId'])
    return Link

layout = [
        [sg.Text("Youtube-Music-MusicMusic-Player")],
        [sg.Text("Enter the Title (maybe with the Artist) here:"), sg.InputText()],
        [sg.Button("Play!"), sg.Button("Pause") ,sg.Button("Stop")],
        [sg.Text(key="-Playing-")]
]

window = sg.Window("Youtube Music-Musicplayer", icon="Icon.png", element_justification='c').Layout(layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "Play!":
        try:
            song = Title(values[0])
            link = findLink(values[0])
            ydl_opts = {
                "format": "bestaudio/best",
                "quiet": True,
                "nocheckcertificate": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                if "url" in info:
                    url = info["url"]
                else:
                    url = info["formats"][-1]["url"]
                media = vlc.MediaPlayer(url)
                media.play()
                window["-Playing-"].update(f"Playing: {song}")
        except:
            window["-Playing-"].update(f"Not a valid Name")
    elif event == "Pause":
        try:
            if media.is_playing() == True:
                media.set_pause(1)
                window["-Playing-"].update(f"Paused: {song}")
            elif media.is_playing() == False:
                media.set_pause(0)
                window["-Playing-"].update(f"Playing: {song}")
        except:
            window["-Playing-"].update(f"No Song is playing")
    elif event == "Stop":
        try:
            media.stop()
            window["-Playing-"].update(f"Stopped: {song}")
        except:
            window["-Playing-"].update(f"No Song is playing")

window.close()
