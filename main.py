from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
import requests
import urllib.parse
from mutagen.mp3 import MP3
import time
from moviepy.editor import *
from tkinter.tix import *
import os
import pygame

# hiding pygame version output at import
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


root = Tk()
root.title("Music Player")

width = 650
height = 420

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = ((screen_width / 2) - (width / 2))
y = ((screen_height / 2) - (height / 2))

root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
root.resizable(False, False)

font1 = ('Montserrat ExtraBold', 11)
font2 = ('Seven Segment', 20)
matrix_green = "#A8B6A6"

t1 = 0

# initialize pygame-mixer
pygame.mixer.init()


# -------------------------------Functions--------------------------------------
def add_song():
    try:
        song = filedialog.askopenfilename(initialdir=r'C:\Users\HP\Music', title='Choose a song',
                                          filetypes=(('mp3 files', '*.mp3'),))
        application_name(song)
        playlist_box.insert(END, strip_result[add_song.counter])
        add_song.counter += 1
    except:
        pass


def add_url():
    global top
    top = Toplevel(root)
    # top.geometry("750x250")

    widthC = 500
    heightC = 150

    screen_widthC = top.winfo_screenwidth()
    screen_heightC = top.winfo_screenheight()

    x = ((screen_widthC / 2) - (widthC / 2))
    y = ((screen_heightC / 2) - (heightC / 2))

    top.geometry(f'{widthC}x{heightC}+{int(x)}+{int(y)}')
    top.title("Audio Streaming")
    top.resizable(False, False)
    Label(top, text="Enter Audio URL", font=('Montserrat ExtraBold', 20)).pack(pady=10)
    audio_url = Entry(top, font=font1, width=30)
    audio_url.pack()
    okay_button = Button(top, text="OK", font=font1, width=10, command=lambda: getUrl(audio_url.get()))
    okay_button.place(x=(widthC - 150), y=(heightC - 50))


def getUrl(url_string):
    try:
        URL = url_string
        isHttp = URL[0:4]
        correct_url = URL.replace("\\", "/")
        isLocalFile = correct_url[1:3]
        if isHttp == 'http':
            # print("this is a http. nice one matte")
            url_format_name(URL)
            playlist_box.insert(END, strip_result[add_song.counter])
            if not (os.path.isfile(f'streams/{strip_result[add_song.counter]}.mp3')):
                try:
                    response = requests.get(URL, stream=True)
                    open(f"streams/{strip_result[add_song.counter]}.mp3", "wb").write(response.content)
                except:
                    os.mkdir('streams')
                    response = requests.get(URL, stream=True)
                    open(f"streams/{strip_result[add_song.counter]}.mp3", "wb").write(response.content)
                    playlist_box.insert(END, strip_result[add_song.counter])
                add_song.counter += 1
            else:
                add_song.counter += 1

        elif isLocalFile == r':/' and ((correct_url.split(".")[-1] == "mp4") or (correct_url.split(".")[-1] == "mp3")):
            if correct_url.split(".")[-1] == "mp3":
                # print("this is a local file my guy")
                application_name(correct_url)
                playlist_box.insert(END, strip_result[add_song.counter])
                add_song.counter += 1

            elif correct_url.split(".")[-1] == "mp4":
                mp4_files_locations(correct_url)



    except:
        pass
    top.destroy()


def application_name(song):
    if not (song in location):
        location.append(song)
        # print(location)
    else:
        return
    try:
        text = str(song).replace("/", "\\")
        a = text.rsplit('.', 1)[0]
        if not (a.rsplit('\\', 1)[1] in strip_result):
            strip_result.append(a.rsplit('\\', 1)[1])
        else:
            return
    except:
        pass


def mp4_files_locations(song):
    # print(song)
    # print(strip_result)
    # print(location)
    try:
        text = str(song).replace("/", "\\")
        a = text.rsplit('.', 1)[0]
        if not (a.rsplit('\\', 1)[1] in strip_result):
            strip_result.append(a.rsplit('\\', 1)[1])
        else:
            return
    except:
        pass
    # print(strip_result)
    try:
        if not (os.path.isfile(f'streams/{strip_result[add_song.counter]}.mp3')):
            try:
                video = VideoFileClip(os.path.join(song))
                video.audio.write_audiofile(os.path.join(f"streams/{strip_result[add_song.counter]}.mp3"),
                                            verbose=False,
                                            logger=None)
            except:
                strip_result.pop(add_song.counter)
                return
            if not (f"streams/{strip_result[add_song.counter]}.mp3" in location):
                location.append(f"streams/{strip_result[add_song.counter]}.mp3")
            playlist_box.insert(END, strip_result[add_song.counter])
            # print(strip_result[add_song.counter])
            # print(location)
            add_song.counter += 1
        else:
            location.append(f"streams/{strip_result[add_song.counter]}.mp3")
            # print(strip_result)
            # print(location)
            playlist_box.insert(END, strip_result[add_song.counter])
            add_song.counter += 1
    except:
        pass


def url_format_name(song):
    try:
        text = str(song).replace("/", "\\")
        a = text.rsplit('.', 1)[0]
        url = urllib.parse.unquote(a.rsplit('\\', 1)[1])
        # print(url)
        if not (url in strip_result):
            strip_result.append(url)
        else:
            return
        if not (f"streams/{strip_result[add_song.counter]}.mp3" in location):
            location.append(f"streams/{strip_result[add_song.counter]}.mp3")
        else:
            return
        # print(location)
    except:
        pass


def get_audio_length(path):
    audio = MP3(path)
    return audio.info.length


def update_timer(duration):
    try:
        # print("multiprocessing")
        update_timer.duration = 0
        update_timer.elapsed_time = 0
        update_timer.duration = duration
        if t1.is_alive():
            while update_timer.elapsed_time < update_timer.duration and not (update_timer.elapsed_time < 0):
                time.sleep(1 / 2)
                update_timer.elapsed_time = pygame.mixer.music.get_pos() / 1000
                # print(update_timer.elapsed_time)
                player_bar['value'] = (update_timer.elapsed_time * 100) / update_timer.duration
                w = convert_to_standard_time(update_timer.elapsed_time)
                # print(pygame.mixer.music.get_pos())
                if int(w.split(":")[-1]) < 10:
                    w = f'{w.split(":")[0:-1][0]}:0{w.split(":")[-1]}'
                    timer.configure(text=f'{w}')
                else:
                    timer.configure(text=f'{w}')
            else:
                if loop_many.state == 'ON' and not (stop.stopper == 1):
                    # print("playing the next song")
                    next_song()
                elif loop_many.state == 'NEUTRAL' and not (stop.stopper == 1):
                    # print("looping once")
                    stop_completely()
                    play()
                else:
                    # print("stopping")
                    play.isSongPlaying = 0
                    pass
    except:
        stop()
        pass


def update_play(audio_length, length_in_seconds):
    if int(audio_length.split(":")[-1]) < 10:
        audio_length = f'{audio_length.split(":")[0:-1][0]}:0{audio_length.split(":")[-1]}'
        total_timer.config(text=audio_length)
    else:
        total_timer.config(text=audio_length)
    global t1
    t1 = threading.Thread(target=update_timer, args=[length_in_seconds])
    t1.start()


def play():
    stop.stopper = 0
    play.isSongPlaying = 1
    a = pygame.mixer.music.get_pos()
    time.sleep(1 / 10)
    b = pygame.mixer.music.get_pos()
    # check if music is playing - only music that is playing can be paused
    # if false music is playing and therefore can be paused
    if a == b:
        pass
    else:
        # print(playlist_box.get(ACTIVE))
        state = "paused"
        # print("music is playing")
        pause_music(state)
        return

    try:
        timer.configure(text="00:00")
        current_song = playlist_box.get(ACTIVE)
        play.s = int(strip_result.index(current_song)) + play.song_number
        playlist_box.select_set(play.s)

        actually_play(play.s)
    except:
        pass


def actually_play(path):
    # print(loop_music.state)
    if add_song.counter == 1:
        # print(str(location[add_song.counter - 1]))
        pygame.mixer.music.load(str(location[add_song.counter - 1]))
        current_playing_song[0] = str(location[add_song.counter - 1])
        update_play(get_length(str(location[add_song.counter - 1])),
                    get_audio_length(str(location[add_song.counter - 1])))
    else:
        # print(str(location[path]))
        pygame.mixer.music.load(str(location[path]))
        current_playing_song[0] = str(location[path])
        update_play(get_length(str(location[path])), get_audio_length(str(location[play.s])))

    pygame.mixer.music.play(loops=0)

    displaySongName(strip_result[int(strip_result.index(playlist_box.get(ACTIVE))) + play.song_number])


update_timer.elapsed_time = 0
update_timer.duration = 0


def stop():
    try:

        # update_timer.elapsed_time = update_timer.duration + 10
        pause_btn.grid_remove()
        play_btn.grid(row=0, column=2, padx=10)

        pygame.mixer.music.set_pos(-1)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        playlist_box.select_clear(ACTIVE)
        timer.configure(text="00:00")
        time.sleep(1 / 2)
    except:
        pass


def stop_completely():
    if stop.stopper == 0:
        stop.stopper = 1
        stop()


def pause_music(state):
    if state == "paused":
        pygame.mixer.music.pause()
        play_btn.grid_remove()
        pause_btn.grid(row=0, column=2, padx=10)
    else:
        pause_btn.grid_remove()
        play_btn.grid(row=0, column=2, padx=10)
        pygame.mixer.music.unpause()


def auto_run_music(event):
    # print(strip_result)
    cs = playlist_box.curselection()
    for list in cs:
        if list == int(strip_result.index(playlist_box.get(ACTIVE))):
            # print(playlist_box.get(ACTIVE))
            stop()
            play()


def update_volume_icon(level):
    volume_percentage = int((level * 100) / max_volume)
    # print(volume_percentage)
    if update_volume_icon.toggle == 0:
        brain[0] = vol_slider.get()
        update_volume_icon.toggle = 1
    else:
        brain[1] = vol_slider.get()
        update_volume_icon.toggle = 0

    # print(brain)
    if (brain[0]) > vol_slider.get():
        # print("decreasing volume")
        if volume_percentage < 1:
            # print("mute")
            volume_min.grid_remove()
            volume_average.grid_remove()
            volume_max.grid_remove()
            volume_mute.grid(row=0, column=0)
        if 0 < volume_percentage < 25:
            # print("Low")
            volume_mute.grid_remove()
            volume_average.grid_remove()
            volume_max.grid_remove()
            volume_min.grid(row=0, column=0)
        if 25 <= volume_percentage < 75:
            # print("Average")
            volume_mute.grid_remove()
            volume_min.grid_remove()
            volume_max.grid_remove()
            volume_average.grid(row=0, column=0)
        if volume_percentage >= 75:
            # print("High")
            volume_mute.grid_remove()
            volume_min.grid_remove()
            volume_average.grid_remove()
            volume_max.grid(row=0, column=0)
    elif brain[0] == vol_slider.get():
        if volume_percentage < 1:
            volume_min.grid_remove()
            volume_average.grid_remove()
            volume_max.grid_remove()
            volume_mute.grid(row=0, column=0)
        pass
    else:
        # print("increasing volume")
        if volume_percentage < 1:
            # print("mute")
            volume_min.grid_remove()
            volume_average.grid_remove()
            volume_max.grid_remove()
            volume_mute.grid(row=0, column=0)
        if 0 < volume_percentage < 25:
            # print("Low")
            volume_mute.grid_remove()
            volume_average.grid_remove()
            volume_max.grid_remove()
            volume_min.grid(row=0, column=0)
        if 25 <= volume_percentage < 75:
            # print("Average")
            volume_mute.grid_remove()
            volume_min.grid_remove()
            volume_max.grid_remove()
            volume_average.grid(row=0, column=0)
        if volume_percentage >= 75:
            # print("High")
            volume_mute.grid_remove()
            volume_min.grid_remove()
            volume_average.grid_remove()
            volume_max.grid(row=0, column=0)


def motion(event):
    try:
        player_width = player_bar.winfo_width()
        max_value = int(player_bar.cget("max"))
        percent = min(max(event.x / player_width, 0), max_value)
        value = percent * max_value
        # # var.set(value)
        # # print(update_timer.duration)
        # new_frame = (update_timer.duration * value) / 100
        # # print(pygame.mixer.music.get_pos())
        # print(new_frame)
        # pygame.mixer.music.set_pos(new_frame)
        # print(pygame.mixer.music.get_pos())
        # print(update_timer.duration * 1000)
        # pygame.mixer.music.set_pos(update_timer.duration)


    except:
        pass


def update_volume(var):
    # print(var)
    pygame.mixer.music.set_volume(vol_slider.get() / 100)
    current_volume[0] = int(var)
    update_volume_icon(current_volume[0])


def handle_volume():
    number_of_elements_in_grid = vol_container.grid_size()[0]

    vol_slider.set(current_volume[0])
    if number_of_elements_in_grid == 1:
        vol_slider.grid(row=0, column=1, padx=20)
    else:
        vol_slider.grid_remove()


# does nothing: it was substituted with other algorithm
def checkStatus():
    SONG_END_EVENT = pygame.USEREVENT + 1

    while True:
        print("listening for pygame events")
        for event in pygame.event.get():
            if event.type == SONG_END_EVENT:
                print("song has ended")


def displaySongName(song_name):
    marquee_label.configure(text=song_name)


def previous_song():
    # print("previous song")
    # print(playlist_box.get(ACTIVE))
    try:
        selected_value = location.index(current_playing_song[0])
        play.song_number = -1
        if selected_value + play.song_number < 0:
            return
        stop()
        play()
        # print(selected_value + play.song_number)
        # playlist_box.focus_set(0)
        # playlist_box.select_set(selected_value + play.song_number)
        playlist_box.select_clear
        playlist_box.activate(selected_value + play.song_number)
        playlist_box.focus_set()
        # root.focus_set()
        playlist_box.update()
        play.song_number = 0
    except:
        pass


def next_song():
    # print("next song")
    # print(len(location))
    # print(int(location.index(current_playing_song[0])) + 1)
    try:
        if location.index(current_playing_song[0]) + 1 == len(location) and not (loop_many.state == 'ON'):
            return
    except:
        return
    try:
        if int(location.index(current_playing_song[0])) + 1 == len(location):
            try:
                # print("your playlist is over")
                playlist_box.select_clear
                playlist_box.activate(0)
                playlist_box.focus_set()
                playlist_box.update()
                # print(playlist_box.get(ACTIVE))
                stop()
                play()
            except:
                pass
            return

        selected_value = location.index(current_playing_song[0])
        play.song_number = 1
        stop()
        play()
        # print(selected_value + play.song_number)
        # playlist_box.focus_set(0)
        # playlist_box.select_set(selected_value + play.song_number)
        playlist_box.select_clear
        playlist_box.activate(selected_value + play.song_number)
        playlist_box.focus_set()
        # root.focus_set()
        playlist_box.update()
        play.song_number = 0
    except:
        pass


def loop_many():
    # print("loop on")
    pygame.mixer.music.set_endevent()
    loop_btn.grid_remove()
    loop_many_btn.grid(row=0, column=4, padx=10)
    loop_many.state = "ON"


def loop_one():
    # print("loop off")
    loop_many_btn.grid_remove()
    loop_one_btn.grid(row=0, column=4, padx=10)
    loop_many.state = 'NEUTRAL'


def unloop_music():
    # print("loop off")
    loop_one_btn.grid_remove()
    loop_btn.grid(row=0, column=4, padx=10)
    loop_many.state = 'OFF'


def delete_song():
    try:
        # print(add_song.counter)
        # print("deleting a song")
        # print(play.isSongPlaying)
        if (current_playing_song[0] == location[strip_result.index(playlist_box.get(ACTIVE))]) and (play.isSongPlaying == 1):
            return
        if add_song.counter == 1:
            displaySongName("no song playing")
            total_timer.configure(text="00:00")
            # return
        selected_song = strip_result.index(playlist_box.get(ACTIVE))
        # print(selected_song)
        playlist_box.delete(selected_song)
        strip_result.pop(selected_song)
        location.pop(selected_song)
        add_song.counter -= 1
        # print(strip_result)
        # print(location)
    except:
        pass


def get_length(path):
    audio = MP3(path)
    return convert_to_standard_time(audio.info.length)


def convert_to_standard_time(seconds):
    minutes = 0 if (seconds / 60) < 1 else int((seconds / 60))
    remaining_seconds = int(seconds) if minutes < 1 else float(f'0.{str((seconds / 60)).split(".")[1]}') * 60
    hours = 0 if minutes < 60 else int((minutes / 60))
    c_minutes = minutes if minutes < 60 else minutes - (hours * 60)
    result = '00:00'

    # formatting output
    if hours == 0:
        if c_minutes < 10:
            result = f'0{c_minutes}:{round(remaining_seconds)}'
        elif c_minutes >= 10:
            result = f'{c_minutes}:{round(remaining_seconds)}'
        elif round(remaining_seconds) < 10:
            result = f'{c_minutes}:0{round(remaining_seconds)}'
        elif round(remaining_seconds) >= 10:
            result = f'{c_minutes}:{round(remaining_seconds)}'
        elif c_minutes < 10 and round(remaining_seconds) < 10:
            result = f'0{c_minutes}:0{round(remaining_seconds)}'
        else:
            result = f'{c_minutes}:{round(remaining_seconds)}'
    else:
        if c_minutes < 10:
            result = f'{hours}:0{c_minutes}:{round(remaining_seconds)}'
        elif c_minutes >= 10:
            result = f'{hours}:{c_minutes}:{round(remaining_seconds)}'
        elif round(remaining_seconds) < 10:
            result = f'{hours}:{c_minutes}:0{round(remaining_seconds)}'
        elif round(remaining_seconds) >= 10:
            result = f'{hours}:{c_minutes}:{round(remaining_seconds)}'
        elif c_minutes < 10 and round(remaining_seconds) < 10:
            result = f'{hours}:0{c_minutes}:0{round(remaining_seconds)}'
        else:
            result = f'{hours}:{c_minutes}:{round(remaining_seconds)}'

    return result


# -------------------------------end--------------------------------------------
add_song.counter = 0
global location
location = []
global strip_result
strip_result = []
play.toggle = 0
play.s = 0
pos = [0, 0]
handle_volume.toggle = 0
max_volume = 100
current_volume = [max_volume]
brain = [max_volume, max_volume]
update_volume_icon.toggle = 0
motion.the_time = pygame.mixer.music.get_pos() / 1000
play.song_number = 0
loop_many.state = "OFF"
current_playing_song = [0]
stop.stopper = 0
play.isSongPlaying = 0

# playlist-box #fg = B4BAA3
playlist_box = Listbox(root, bg="#2B2B2B", fg=matrix_green, width=60, selectbackground='#3C3F41',
                       selectforeground='#02A101', font=font1)
playlist_box.bind('<Double-1>', auto_run_music)
playlist_box.pack(pady=20)

# create Marquee
marquee_frame = Canvas(root, background=matrix_green, width=200, height=200, bg='red')
# marquee_frame.pack()
marquee_frame.pack(anchor="ce")
marquee_frame.pack_propagate(0)

marquee_label = Label(marquee_frame, text="No song playing", font=font2, pady=20)
marquee_label.grid(column=1, row=1, sticky="nesw")

# create controls
back_btn_img = PhotoImage(file='images/backward.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')
loop_btn_img = PhotoImage(file='images/loop.png')
loop_many_btn_img = PhotoImage(file='images/loop-many.png')
loop_one_btn_img = PhotoImage(file='images/loop-one.png')
volume_max_img = PhotoImage(file='images/volume-max.png')
volume_average_img = PhotoImage(file='images/volume-average.png')
volume_min_img = PhotoImage(file='images/volume-min.png')
mute_img = PhotoImage(file='images/mute.png')
delete_img = PhotoImage(file='images/delete.png')

controls_frame = Frame(root)
controls_frame.pack()

vol_container = Frame(root)
vol_container.place(x=width - 145, y=height - 84)
vol_slider = Scale(vol_container, orient=HORIZONTAL, from_=0, to=max_volume, length=50, command=update_volume)

back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause_music("playing"))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop_completely)
loop_btn = Button(controls_frame, image=loop_btn_img, borderwidth=0, command=loop_many)
loop_many_btn = Button(controls_frame, image=loop_many_btn_img, borderwidth=0, command=loop_one)
loop_one_btn = Button(controls_frame, image=loop_one_btn_img, borderwidth=0, command=unloop_music)
volume_max = Button(vol_container, image=volume_max_img, borderwidth=0, command=handle_volume)
volume_mute = Button(vol_container, image=mute_img, borderwidth=0, command=handle_volume)
volume_min = Button(vol_container, image=volume_min_img, borderwidth=0, command=handle_volume)
volume_average = Button(vol_container, image=volume_average_img, borderwidth=0, command=handle_volume)
delete_btn = Button(root, image=delete_img, borderwidth=0, command=delete_song)

tip = Balloon(root)
tip.bind_widget(delete_btn, balloonmsg="Delete")
tip.bind_widget(stop_btn, balloonmsg="Stop")
tip.bind_widget(back_btn, balloonmsg="Previous")
tip.bind_widget(play_btn, balloonmsg="Play")
tip.bind_widget(pause_btn, balloonmsg="Pause")
tip.bind_widget(forward_btn, balloonmsg="Next")
tip.bind_widget(loop_btn, balloonmsg="Loop Off")
tip.bind_widget(loop_many_btn, balloonmsg="Loop Many")
tip.bind_widget(loop_one_btn, balloonmsg="Loop One")
tip.bind_widget(volume_min, balloonmsg="Volume")
tip.bind_widget(volume_average, balloonmsg="Volume")
tip.bind_widget(volume_max, balloonmsg="Volume")
tip.bind_widget(volume_mute, balloonmsg="Mute")

stop_btn.grid(row=0, column=0, padx=10)
back_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
forward_btn.grid(row=0, column=3, padx=10)
loop_btn.grid(row=0, column=4, padx=10)
volume_max.grid(row=0, column=0)

delete_btn.place(x=50, y=height - 83)

# create the menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add songs menu
add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add one song to the playlist', command=add_song)
add_song_menu.add_command(label="Add song from URL", command=add_url)

# Timer
timer = Label(root, text="00:00", font=("Montserrat", 11))
timer.place(x=42, y=height - 175)

total_timer = Label(root, text="00:00", font=("Montserrat", 11))
total_timer.place(x=width - 92, y=height - 175)

# ProgressBar
s = ttk.Style()
s.theme_use("default")
s.configure("TProgressbar", thickness=2, troughcolor='#2B2B2B', background='#0C8CE9')
player_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=width - 200, mode="determinate", style="TProgressbar")
# bind a single click(on click) to the playerBar
player_bar.bind('<Button-1>', motion)
player_bar.place(x=100, y=height - 162)

if __name__ == "__main__":
    # processes = []
    root.mainloop()
    stop()
    pygame.mixer.quit()
    pygame.quit()
