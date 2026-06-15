class Song:                #Song class 
   def __init__(self, title, album, artist, genre, status, year, rating): 
      self.title = title
      self.album = album
      self.artist = artist
      self.genre = genre
      self.status = status
      self.year = year
      self.rating = rating



class Library:             #Library class 
   def __init__(self):
      self.library = []            #empty list to add songs to
      self.playlists =[]           #empty list to add playlists to
      self.plays = Playlist("")
      self.liked_playlist = Liked_playlist()

   def add_song(self, Song):       #when user adds song this will add it to the library list
      self.library.append(Song)

   def add_playlist(self,name):   #when user adds playlist this will add it to the playlists list
      self.playlists.append(name)  

   def change_song_rating(self, title, new_rating):   # changes the original rating that the user put in
      for song in self.library:
         if song.title == title:
           song.rating = new_rating
           return True
      return False 

   def add_to_playlist(self,playlist,title):      #user adds song to a certain playlist
      for song in self.library:
         if song.title == title:
            self.plays.add_song_playlist(playlist,title)
            return True
      return False
    

   def add_to_liked_playlist(self,title):     #if user likes a song, it will be added to the liked playlist
      for song in self.library:
         if song.title == title:
            self.liked_playlist.add_liked_song(song)
            return True
      return False  
   
   def view_liked_playlist(self):           
      return self.liked_playlist.view_liked_playlist_contents()
   
   def search_by_title(self,title):          #user can search by title
       return [song.title for song in self.library if song.title == title]
   
   def search_by_artist(self, artist):      #user can search by artist
      return [song.title for song in self.library if song.artist == artist]
   
   def search_by_album(self, album):       #user can search by album
      return [song.title for song in self.library if song.album == album]
   
   def search_by_genre(self,genre):          #user can search by genre
      return [song.title for song in self.library if song.genre == genre]
   
   def search_by_rating(self, rating):        # user can search by rating
      return [song.title for song in self.library if song.rating == rating]
   
   def search_by_year(self, year):         #user can search by year
      return [song.title for song in self.library if song.year == year]
   
   def print_playlists(self):              #print playlists that are available that the user made
      p = []
      for playlist in self.playlists:
         p.append(playlist.name)
      return p


   
class Playlist:           #Playlist class
   def __init__(self,name):              
      self.songs = []       #Empty list to put songs in for playlists
      self.name = name

   def add_song_playlist(self,playlist, title):     #adds songs to playlists created
      self.songs.append(title)
           

   def remove_song(self, playlist, title):         #removes songs from playlist 
        for i, song in enumerate(self.songs):
            if song.title == title:
                del self.songs[i]
                return True
        return False
  
   
class Liked_playlist:        #Liked Playlist clss
   def __init__(self):
      self.liked_songs = []        #empty list to add liked songs to

   def add_liked_song(self,song):     #adds liked songs to the liked_songs list
      self.liked_songs.append(song)

   def view_liked_playlist_contents(self):   #gives a list of the liked songs
      lp = []
      for songs in self.liked_songs:
         lp.append(songs)
      return lp



class Queue:               #Queue class
   def __init__(self):
      self.queue = []       #empty list to add songs to for the queue

   def add_song_to_queue(self, song):   #adds song to queue list
      self.queue.append(song)   

   def view_queue_contents(self):  #gives a list of the queue
      q = []
      for songs in self.queue:
         q.append(songs)
      return q   

   def play(self):       #plays the first of the list that was added and then removes it
      for song in self.queue:
         print(f"Now Playing {self.queue[0]}....") #display function
         self.queue.remove(song)
      

 #Songs can be liked after they add them to the library just like Spotify 
   
  
         

print("-----------------------------------")
print("Welcome to Kaitlyn's Music System!")         #introduction to the music system
print("-----------------------------------")
print("Here you can make a playlist, rating your songs, and find your favorite")
print("DO NOT INPUT A STRING INTO THE ACTION INPUT") #gives you a rule


#Intitalizes the classes
lib = Library()
playlist = Playlist("")
liked_playlist = Liked_playlist()
que = Queue() 

while True:     #this will run until they exit or input an invalid input
   print("-------------------------")     #gives a selection of things to do in the system
   print("1. Add a song to Library")
   print("2. Like a song")
   print("3. Change Song Rating")
   print("4. Search for Song")
   print("5. Create a playlist")
   print("6. Add a song to a Playlist") 
   print("7. Remove a song to Playlist")
   print("8. View all playlist")
   print("9. View liked songs playlist")
   print("10. Add a song to queue")
   print("11. Play the queue")  
   print("12. Exit")
   print("-------------------------") 
     
# gets the users input and what they want to do 
   action = input("Please pick an action and then input the number that is associated with it: ")  

   if int(action) == 1:                #add a song
      title = input("Enter song title: ")
      album = input("Enter song album: ")
      artist = input("Enter song artist: ")
      genre = input("Enter song genre: ")
      status = "none"
      year = input("Enter song year: ")
      rating = input("Enter song rating(1-5): ")

      new_song1 = Song(title, album, artist, genre, status, year, rating)
      lib.add_song(new_song1)
      print(f"Song '{new_song1.title}' added to library!")

   elif int(action) == 2:               #like a song
      title = input("Enter song title to like: ")
      liked_playlist.add_liked_song(title)
      print(f"Song '{title}' has been liked!")


   elif int(action) == 3:             # change rating of song
      title = input("Enter song title: ")
      new_rating = input("Enter new rating(1-5): ")
      lib.change_song_rating(title, new_rating)
      print(f"Rating has for {title} been updated to {new_rating}")

   elif int(action) == 4:            #search for song
    search = input("Input how you wanna search for the song(title/album/artist/genre/year/rating): ")
    search_name = input(f"Enter {search} name: ")
    if search.lower() == "title":             #search by title
        print(lib.search_by_title(search_name))
    elif search.lower() == "album":             #search by album and gives title
        print(lib.search_by_album(search_name))
    elif search.lower() == "artist":             #search by artist and gives title
        print(lib.search_by_artist(search_name))
    elif search.lower() == "genre":             #search by genre and gives title
       print(lib.search_by_genre(search_name)) 
    elif search.lower() == "year":             #search by year and gives title
       print(lib.search_by_year(search_name))
    elif search.lower() == "rating":             #search by rating and gives title
       print(lib.search_by_rating(search_name))       
    else:
       print("false")   

   elif int(action) == 5:           #make a new playlist
      new_playlist = input("Enter name for the new playlist: ")
      lib.add_playlist(Playlist(new_playlist))
      print(f"Playlist '{new_playlist}' has been created!")

   elif int(action) == 6:           #Put song into playlist
      song_for_playlist = input("Enter Song title: ")
      added_song_playlist = input("Enter Playlist name: ")
      lib.add_to_playlist(added_song_playlist, song_for_playlist)
      print(f"Song '{song_for_playlist}' added to '{added_song_playlist}' playlist")

   elif int(action) == 7:         #Remove song from playlist
      song_from_playlist = input("Enter song title to remove: ")
      removed_song_playlist = input("Enter playlist name: ")
      playlist.remove_song(removed_song_playlist, song_from_playlist)
      print(f"Song '{song_from_playlist}' removed from '{removed_song_playlist}' playlist!")

   elif int(action) == 8:           #view all playlists
    avail_playlists = lib.print_playlists()
    print(f"Available Playlists: {avail_playlists}")

   elif int(action) == 9:
      liked_songs = liked_playlist.view_liked_playlist_contents()
      print(f"Songs in liked playlist: {liked_songs}")

   elif int(action) == 10:           #add song into queue
    add_song_queue = input("Enter song title: ")  
    que.add_song_to_queue(add_song_queue)
    print(f"Song '{add_song_queue}' added to the queue")
   elif int(action) == 11:      #play queue
    print(que.play())

   elif int(action) == 12:   # when finished user can exit the system
    print("Thank you for using Kaitlyn's Music System! Goodbye!")
    break  
   
   else:    #if they input an invalid input they get to try again
      print("Input not valid! Please try again!")
      continue       



import unittest

class TestMusicSystem(unittest.TestCase):
   def setUp(self):
      self.lib = Library()               #Initialization for Library class
      self.play = Playlist("")           #Initialization for Playlist class
      self.liked_play = Liked_playlist() #Initialization for Liked Playlist class
      self.que = Queue()                 #Initialization for Queue class
      self.song1 = Song("Love Story", "Fearless", "Taylor Swift", "Pop", "none", 2008, 4.0)     #creation of song
      self.song2 = Song("Boot Scootin Boogie", "Brand New Man", "Brooks & Dunn", "Country", "none", 1991, 3.9)   #creation of song
      self.play1 = Playlist("Kaitlyn's Tunes")         #creation of Playlist
      self.liked_play.add_liked_song(self.song1.title)   #add song to liked playlist
      self.lib.add_song(self.song1)                      #add song to library
      self.lib.add_song(self.song2)                      #add song to library
      self.lib.add_playlist(self.play1)                  #add playlist to library
      self.que.add_song_to_queue(self.song1.title)       #add song to queue

   def test_add_song(self):    #tests if the song is added into the library
      self.assertIn(self.song1, self.lib.library)
      self.assertIn(self.song2, self.lib.library)  

   def test_change_song_rating(self):  #tests if song rating changes
      self.assertTrue(self.lib.change_song_rating("Love Story", 4.5))  
      self.assertEqual(self.song1.rating, 4.5)
      self.assertFalse(self.lib.change_song_rating("You Belong with Me", 5.0))  

   def test_add_to_playlist(self):     #tests if song goes into playlist
      self.assertTrue(self.lib.add_to_playlist("Kaitlyn's Tunes", "Love Story"))
      self.assertIn(self.song1.title, self.lib.plays.songs)   
      self.assertFalse(self.lib.add_to_playlist("Kaveh's Tunes","You belong with me"))

   def test_view_all_playlist(self):   #tests if all playlists show up
      playlist_contents = self.lib.print_playlists()   
      self.assertEqual(len(playlist_contents), 1)
      self.assertIn("Kaitlyn's Tunes", playlist_contents)

   def test_view_liked_playlist(self):    #tests if songs are in liked playlist
      playlist_contents = self.liked_play.view_liked_playlist_contents()   
      self.assertEqual(len(playlist_contents), 1)
      self.assertIn("Love Story", playlist_contents)   

   def test_search_methods(self):   #tests the searching methods for a library
      #Search by title 
      result = self.lib.search_by_title("Love Story")
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], "Love Story" )  

      #Search by album 
      result = self.lib.search_by_album("Fearless")
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], "Love Story" )

      #Search by artist
      result = self.lib.search_by_artist("Taylor Swift")
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], "Love Story" )

      #Search by genre 
      result = self.lib.search_by_genre("Pop")
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], "Love Story" )

      #Search by year 
      result = self.lib.search_by_year(2008)
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], "Love Story" )

      #Search by rating 
      result = self.lib.search_by_rating(4.0)
      self.assertEqual(len(result),1)
      self.assertEqual(result[0], 4.0)

   def test_remove_song_from_playlist(self):     #tests if song is removed from a playlist
      self.lib.add_to_playlist("Kaitlyn's Tunes","Love Story")
      self.play.remove_song("Kaitlyn's Tunes", "Love Story")
      self.assertEqual(self.play.songs, [])
      self.assertFalse(self.play.remove_song("Kaitlyn's Tunes","Love story")) #This song has already been removed  

   def test_view_queue(self):           #tests if queue has contents
      queue_contents = self.que.view_queue_contents()   
      self.assertEqual(len(queue_contents), 1)
      self.assertIn("Love Story", queue_contents)   


if __name__ == '__main__':
   unittest.main()