import os
from dotenv import load_dotenv

load_dotenv()

def add_video(category, link, youtube, db):
        if 'youtu.be/' in link:
            # mobile link
            vid_id = link.split('.be/')[1]
        elif 'youtube.com/watch?v=' in link:
            vid_id = link.split('v=')[1]
        else:
            return 'That was not a YouTube video link!'
        
        video_request = youtube.videos().list(
                    part="snippet",
                    id=vid_id,
                )
        video_response = video_request.execute()
        if len(video_response['items']):
            video = video_response['items'][0]
            video_obj = {
                'link': f"youtube.com/watch?v={vid_id}",
                'title': video['snippet']['title'].replace('&', 'and'),
                'author': video['snippet']['channelTitle'],
                'category': category
            }
            db.workout_videos.insert_one(video_obj)
            return 'Video has been added!'
        else:
            return 'That was an invalid link!'
    

def add_video_handler(update, context, youtube, db):
    CATEGORIES = ['Full Body', 'Upper Body', 'Lower Body', 'Core', 'Song Workout']

    text = update.message.text.strip()
    if text == '/addvideo':
        if update.message.chat.id != int(os.getenv("AUTHORIZED_CHAT_ID")):
            reply = 'Oops, you don\'t have permission to add a video!'
        else:
            categories = "\n".join([f"{index+1}) {cat}" for (index, cat) in enumerate(CATEGORIES)])
            reply = f'The categories are:\n{categories}\n\nAdd videos in this format: /addvideo 2 youtube.com/watchblahv=blah to add a video as an Upper Body workout!'
    else:
        text_lst = text.split(' ')
        if len(text_lst) == 3:
            _, category, link = text_lst
            if int(category) <= len(CATEGORIES) and int(category) >= 1:
                reply = add_video(CATEGORIES[int(category) -1], link.strip(), youtube, db)
            else:
                reply = 'Did you mistype the category number?'
        else:
            reply = 'You didn\'t leave spaces, did you?'
    
    update.message.reply_html(reply)