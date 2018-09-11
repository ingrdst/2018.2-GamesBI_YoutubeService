import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YouTubeSearch


class YouTubeView(APIView):
    '''
        View that calls IGDB API
        and return some relevant
        information about a game
        and filter for Null value
    '''
    def get(self, request, format=None):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}&key={}'.format('PUBG', header['user-key'])
        data = requests.get(url, headers=header['Accept'])
        ndata = data.json()

        print(ndata)
        for gamedata in ndata:
            filtered_data = self.filter_data(gamedata)
            self.save_game(filtered_data)

        games = YouTubeSearch.objects.all()
        for game in games:
            print('------------')
            print(game.id)
            print(game.name)
            print('------------')

        return Response(data=ndata)

    def filter_data(self, gamedata):
        
        if 'items' in gamedata:

            if 'id' in gamedata['items']:
                
                if 'videoId' in gamedata['items']['id']:
                    id = gamedata['items']['id']['videoId']
            
                else:
                    id = None

            else:
                id = None

        else:
            id = None

                    
            if 'name' in gamedata:
                name = gamedata['name']
            else:
                name = None

            
            
        if 'items' in gamedata:    
            
            if 'viewCount' in gamedata['items']:
                count_views=gamedata['items']['viewCount']
            else:
                count_views=None

            if 'likeCount' in gamedata['items']:
                count_likes=gamedata['items']['likeCount']
            else:
                count_views=None

            if 'dislikeCount' in gamedata:
                count_dislikes=gamedata['items']['dislikeCount']

            if 'commentCount' in gamedata:
                count_comments= gamedata['items']['commentCount']
            else:
                count_comments = None

            if 'regionCode' in gamedata:
                regionCode= gamedata['items']['regionCode']
            else:
                regionCode = None

        else:
            count_views=None
            count_likes=None
            count_dislikes=None
            count_comments=None
            
        
        if 'regionCode' in gamedata:
            regionCode= gamedata['regionCode']
        else:
            regionCode = None
        
        filtered_data = {
        'id': id,
            'name': name,
            'count_views': count_views,
            'count_likes': count_likes,
            'count_dislikes': count_dislikes,
            'count_comments': count_comments,
            'regionCode': regionCode
        }
        return filtered_data

    def save_youtube_search(self, filtered_data):
        results = YouTubeSearch(
            id = filtered_data['id']
            name = filtered_data['name'],
            count_views = filtered_data['count_views'],
            count_likes = filtered_data['count_likes'],
            count_dislikes = filtered_data['count_dislikes'],
            count_comments = filtered_data['count_comments'],
            regionCode = filtered_data['regionCode']
        )
        
        results.save()
        print('o jogo salvou ' + results.name)
