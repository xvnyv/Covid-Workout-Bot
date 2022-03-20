import googleapiclient.discovery
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))
db = client.workout_bot

class Playlist():
    def __init__(self, title, playlist_id):
        self.title = title
        self.id = playlist_id
        self.videos = []

    def make_request(self, pageToken=None):
        request = youtube.playlistItems().list(
            part="contentDetails, snippet",
            playlistId=self.id,
            maxResults=50,
            pageToken= pageToken if pageToken else None
        )
        return request.execute()
        

    def populate_videos(self):
        links = []
        response = self.make_request()
        for video in response['items']:
            if video['snippet']['title'] != 'Private video' and video["contentDetails"]["videoId"] not in links:
                vid_request = youtube.videos().list(
                    part="snippet",
                    id=video["contentDetails"]["videoId"],
                )
                vid_response = vid_request.execute()
                self.videos.append(dict(link=f'youtube.com/watch?v={video["contentDetails"]["videoId"]}', title=video['snippet']['title'].replace('&', 'and'), author=vid_response['items'][0]['snippet']['channelTitle']))            
                links.append(video['contentDetails']['videoId'])
        
        while 'nextPageToken' in response.keys():
            response=self.make_request(response['nextPageToken'])
            
            for video in response['items']:
                if video['snippet']['title'] != 'Private video' and video["contentDetails"]["videoId"] not in links:
                    vid_request = youtube.videos().list(
                        part="snippet",
                        id=video["contentDetails"]["videoId"],
                    )
                    vid_response = vid_request.execute()
                    self.videos.append(dict(link=f'youtube.com/watch?v={video["contentDetails"]["videoId"]}', title=video['snippet']['title'].replace('&', 'and'), author=video['snippet']['channelTitle']))            
                    links.append(video['contentDetails']['videoId'])

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

WORKOUT_TITLES = ['Core', 'Upper Body', 'Lower Body', 'Full Body','Song Workout']

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

request = youtube.playlists().list(
    part="snippet",
    channelId="UCCu-qCNKlg6roet9B1lBCZw",
    maxResults=50
)

response = request.execute()
playlists = [Playlist(item['snippet']['title'], item['id']) for item in response['items'] if item['snippet']['title'] in WORKOUT_TITLES]
playlists.append(Playlist('Song Workout', 'PLN99XDk2SYr5CRS7c1hk62yEultl8KaYn'))

for playlist in playlists:
    playlist.populate_videos()

    ### USING MONGODB 
    for video in playlist.videos:
        video_obj = {
            'link': video['link'],
            'author': video['author'],
            'title': video['title'],
            'category': playlist.title
        }
        result = db.workout_videos.insert_one(video_obj)

    ### USING LOCAL .TXT FILES

    # file_dir = os.path.dirname(os.path.realpath(__file__))
    # filename = os.path.join(file_dir, f'../workout_files/{playlist.title.replace(" ", "")}.txt')
    # filename = os.path.abspath(os.path.realpath(filename))    

    # workouts = dict(workouts=playlist.videos)
    # with open(filename, 'w') as outfile:
    #     json.dump(workouts, outfile)

    ### USING CLOUD FIRESTORE
    
    # docs = db.collection(f"{playlist.title} Videos").stream()
    # db_links = [doc.to_dict()['link'] for doc in docs]
    # for video in playlist.videos:
    #     if video['link'] not in db_links:
    #         doc_ref = db.collection(f"{playlist.title} Videos").document(str(uuid.uuid4()))
    #         doc_ref.set({
    #             u'link': video["link"],
    #             u'author': video["author"],
    #             u'title': video["title"],
    #         })

print('done')