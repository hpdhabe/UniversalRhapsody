# Python program to implement client side of chat room. 
import socket 
import vlc
import select 
import sys 
import pickle
import time
import os

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
	0:0,
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

def get_key(val): 
    for key, value in genres.items(): 
         if val == value: 
             return key 

def changer(file_name):
	instance = vlc.Instance()
	media = instance.media_new(file_name)
	player = instance.media_player_new()
	player.set_media(media)
	player.play()
	# duration = vlc.libvlc_media_get_duration(media)
	# duration/=100 
	# print(duration)

	while True:
		time.sleep(0.2)
		if(os.path.isfile('received')):
			time.sleep(2)
			break

	pickle_in = open("received","rb")
	genre_dict = pickle.load(pickle_in)
	dict_size = len(genre_dict)
	# print(dict_size)

	time1 = 0
	while True: 
		# message = server.recv(2048)
		time.sleep(0.2)
		if(vlc.libvlc_media_player_get_position(player) >= genre_dict[time1][0]):
			eq_handle = vlc.libvlc_audio_equalizer_new_from_preset(genre2.get(genre_dict[time1][1].item()))
			vlc.libvlc_media_player_set_equalizer(player,eq_handle)
			vlc.libvlc_audio_equalizer_release(eq_handle)
			print(get_key(genre2.get(genre_dict[time1][1].item())))
			time1 = time1 + 1
			if(time1>=dict_size):
				break
def main():
	print("In eq_changer")
	changer(sys.argv[1])

if __name__ == "__main__":
	main()
