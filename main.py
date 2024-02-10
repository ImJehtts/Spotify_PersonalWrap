#main
from backend import search,tokens
import customtkinter
import requests
from PIL import Image, ImageTk
from io import BytesIO

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

window = customtkinter.CTk()
window.geometry("990x750")
window.title("Spotify Wrapped Project")
window.resizable(False, False)

time_option = customtkinter.StringVar(value = "short_term")
number_of_songs = customtkinter.StringVar(value = "10")

songs_scroll_frame = customtkinter.CTkScrollableFrame(window,height = 500, width = 930)

dictionary_of_songs = {}

def clear_label(area):
   for label in area.winfo_children():\
       label.destroy()


def formating_artists(artists_names):
   artists = artists_names.split(', ')
   final_string = ""
   for i, artist in enumerate(artists):
       final_string += artist
       if i < len(artists) - 1 and i % 2 == 1:
           final_string += "\n"
       else:
           final_string += ", "

   return final_string.rstrip(', '), len(artists)

def update_songs(time_option_picked,song_number):
   global dictionary_of_songs
   dictionary_of_songs = search(tokens,time_option_picked)

   clear_label(songs_scroll_frame)

   for i in range(1,int(song_number)+1):
       dic = dictionary_of_songs.get(str(i), 0)

       song_name = customtkinter.StringVar(value=dic[0])
       artist_string, artist_length = formating_artists(dic[1])
       song_artist = customtkinter.StringVar(value=artist_string)
       image_url = dic[2]

       image_data = requests.get(image_url).content
       image_opening = Image.open(BytesIO(image_data))
       image = customtkinter.CTkImage(image_opening,size=(65,65))

       customtkinter.CTkLabel(songs_scroll_frame, text= str(i)+".", text_color="green",
                              font=("Times New Roman", 25)).grid(row=i, column=0, sticky = 'w')
       customtkinter.CTkLabel(songs_scroll_frame,text="",image = image).grid(row=i, column=1, sticky = 'w')
       customtkinter.CTkLabel(songs_scroll_frame, textvariable = song_name, text_color="green",
                              font=("Times New Roman", 25)).grid(row=i, column=2, sticky = 'w')
       customtkinter.CTkLabel(songs_scroll_frame, text="  By: ", text_color="green",
                              font=("Times New Roman", 20)).grid(row=i, column=3, sticky = 'w')
       if artist_length > 2:
           customtkinter.CTkLabel(songs_scroll_frame, textvariable=song_artist, text_color="green",
                              font=("Times New Roman", 20)).grid(row=i, column=4, sticky = 'sw')
       else:
           customtkinter.CTkLabel(songs_scroll_frame, textvariable=song_artist, text_color="green",
                                  font=("Times New Roman", 20)).grid(row=i, column=4, sticky='w')

   songs_scroll_frame.columnconfigure(0, minsize=40)
   songs_scroll_frame.columnconfigure(1,minsize = 80)

title_label = customtkinter.CTkLabel(window,text="Spotify Wrapped Project", text_color="green",font=("Times New Roman", 30))

update_songs("short_term","10")

options_of_time = customtkinter.CTkOptionMenu(master = window,values=["short_term","medium_term","long_term"],command=lambda value: update_songs(value,number_of_songs.get()), variable=time_option, font=("Times New Roman", 25), width = 100, height = 45)
number_of_songs_shown = customtkinter.CTkOptionMenu(master = window,values=["5","10","15","20","25"],command=lambda value: update_songs(time_option.get(), value), variable=number_of_songs, font=("Times New Roman", 25), width = 100, height = 45)

time_choice_label = customtkinter.CTkLabel(window,text="Time Period", text_color="green",font=("Times New Roman", 25))
song_number_label = customtkinter.CTkLabel(window,text="# of Songs", text_color="green",font=("Times New Roman", 25))

title_label.place(x=360, y = 25)
options_of_time.place(x=315,y=125)
time_choice_label.place(x=315,y=85)
number_of_songs_shown.place(x=610,y=125)
song_number_label.place(x=610,y=85)
songs_scroll_frame.place(x=20,y=200)


window.mainloop()
