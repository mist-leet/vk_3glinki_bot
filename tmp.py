import urllib.request
from bs4 import BeautifulSoup
import pafy
import vlc
from time import sleep
import sys



class Player:
    def __init__(self):
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        #self.player.set_media(Player.get_media('кащенко', self.Instance))
        #self.player.play()

    def play(self, req):
        self.player.set_media(Player.get_media(req, self.Instance))
        self.player.play()
        sleep(5)
        while self.player.is_playing():
            sleep(4)

    @staticmethod
    def get_url(req):
        query = urllib.parse.quote(req)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            if vid['href'].find('watch') >= 0:
                return 'https://www.youtube.com' + vid['href']

    @staticmethod
    def get_best_url(url):
        video = pafy.new(url)
        best = video.getbest()
        return best.url

    @staticmethod
    def get_media(req, player_inst):
        s_url = Player.get_best_url(Player.get_url(req))
        print(s_url)
        Media = player_inst.media_new(s_url)
        Media.get_mrl()
        return Media

mypl = Player()
mypl.play(sys.argv[1])