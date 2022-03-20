def song_workout_handler(update, context, db):
    reply = 'Here are MadFit\'s song workouts!\n\n'
    # docs = db.collection('Song Workout Videos').stream()
    # song_workouts = [doc.to_dict() for doc in docs]
    
    song_workouts = list(db.workout_videos.find({'category': 'Song Workout'}))
    for (index, song) in enumerate(song_workouts):
        if (index+1) % 10 == 0:
            update.message.reply_html(reply)
            reply = ''
        reply += f'{song["title"]}\n{song["link"]}\n\n'

    if reply != '':
        update.message.reply_html(reply)