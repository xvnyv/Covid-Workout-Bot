import random

def generate_combination(category, db):
    '''
    Combinations:
    - Full Body: 1 full body, 1 core, 1 song 
    - Upper Body: 2 upper body, 1 core
    - Lower Body: 2 lower body, 1 core
    - Core: 2 core
    - Song: 3 song
    '''

    reply = 'Here are the videos chosen for you!\n\n'
    
    # docs = db.collection(f'{category} Videos').stream()
    # workouts = [doc.to_dict() for doc in docs]
    workouts = list(db.workout_videos.find({'category': category}))
    vid_num = 1 if category == 'Full Body' else 2 if category != 'Song Workout' else 3
    for i in range(vid_num):
        chosen_vid = random.choice(workouts)
        workouts.remove(chosen_vid)
        reply += f'<b>{chosen_vid["title"]}</b> by {chosen_vid["author"]}\n{chosen_vid["link"]}\n\n'

    if category != 'Core' and category != 'Song Workout':
        workouts = list(db.workout_videos.find({'category': 'Core'}))
        # docs = db.collection('Core Videos').stream()
        # workouts = [doc.to_dict() for doc in docs]
        chosen_vid = random.choice(workouts)
        reply += f'<b>{chosen_vid["title"]}</b> by {chosen_vid["author"]}\n{chosen_vid["link"]}\n\n'

    if category == 'Full Body':
        song_workouts = list(db.workout_videos.find({'category': 'Song Workout'}))
        # docs = db.collection('Song Workout Videos').stream()
        # song_workouts = [doc.to_dict() for doc in docs]
        chosen_vid = random.choice(song_workouts)
        reply += f'<b>{chosen_vid["title"]}</b> by {chosen_vid["author"]}\n{chosen_vid["link"]}\n\n'
            
    return reply

def generate_handler(update, context, db):
    CATEGORIES = ['Full Body', 'Upper Body', 'Lower Body', 'Core', 'Song Workout']
    
    text = update.message.text.strip()
    if text == '/generate':
        cat_string = "\n".join([f"{index+1}) {cat}" for (index, cat) in enumerate(CATEGORIES)])
        reply = f'Here are {len(CATEGORIES)} categories of workout videos!\n\n{cat_string}\nPlease select a category in the following format:\n\n/generate 1 for {CATEGORIES[0]},\n/generate 2 for {CATEGORIES[1]} etc.'
    else:
        index = text.split(' ')[1] if len(text.split(' ')) == 2 else ''
        if (index.isdigit):
            if (int(index) <= len(CATEGORIES) and int(index) >= 1):
                reply = generate_combination(CATEGORIES[int(index)-1], db)
            else:
                reply = 'Oops, that number does not correspond to any category!'
        else:
            reply = 'Oops, that was not an integer!'

    update.message.reply_html(reply)