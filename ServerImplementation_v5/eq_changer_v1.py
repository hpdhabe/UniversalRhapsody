# Python program to implement client side of chat room. 
import socket 
import vlc
import select 
import sys 
import pickle


genres = {
	'Flat' : 1,
	'Classical' : 2,
	'Club' : 3,
	'Dance' : 4,
	'Full bass' : 5,
	'Full bass and treble' : 6,
	'Full treble' : 7,
	'Headphones' : 8,
	'Large Hall' : 9,
	'Live' : 10,
	'Party' : 11,
	'Pop' : 12,
	'Reggae' : 13,
	'Rock' : 14,
	'Ska' : 15,
	'Soft' : 16,
	'Soft rock' : 17,
	'Techno': 18
}
genre2 = {
	1:17,
	2:8,
	3:10,
	4:2,
	5:13,
	6:4,
	7:18,
	8:11,
	9:17,
	10:11,
	11:17,
	12:12,
	13:1
}
instance = vlc.Instance()
media = instance.media_new("audio.mp3")
player = instance.media_player_new()
player.set_media(media)
player.play()
duration = libvlc_media_get_duration()
duration/=100 

pickle_in = open("data2send","rb")
genre_dict = pickle.load(pickle_in)
dict_size = len(genre_dict)

time = 0
while True: 
	# message = server.recv(2048)
	if(vlc.libvlc_media_player_get_time(player)>=genre_dict[time][0]):
		vlc.libvlc_audio_equalizer_release(player)
		vlc.libvlc_media_player_set_equalizer(player, vlc.libvlc_audio_equalizer_new_from_preset(genres.get(genre2.get(genre_dict[time][1]))))
		time++
		if(time>=dict_size):
			break