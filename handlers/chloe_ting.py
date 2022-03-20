import os

def get_titles():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(file_dir, '../workout_files/chloe_ting_challenges.txt')
    filename = os.path.abspath(os.path.realpath(filename)) 
    f = open(filename, 'r')   
    titles = []
    for line in f:
        if line[0] == 'T':
            title = line.rstrip().split('>')[1] 
            if '&amp;' in title:
                title = title.replace('&amp;', 'and')
            titles.append(title)
    f.close()
    return titles

def get_challenges():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(file_dir, '../workout_files/chloe_ting_challenges.txt')
    filename = os.path.abspath(os.path.realpath(filename)) 
    f = open(filename, 'r')   
    challenges = {}

    title = ''
    for line in f:
        if line[0] == 'T':
            # title of challenge            
            title = line.rstrip().split('>')[1]
            if '&amp;' in title:
                title = title.replace('&amp;', 'and')
            challenges[title] = dict()
        elif line[0].isdigit():
            # day of challenge
            day, videos = line.split('>')
            videos_list = videos.rstrip().split(',')
            formatted_videos = []
            for video in videos_list:
                link, vid_title = video.split('|') if len(video.split('|')) == 2 else ('', '')
                if '&amp;' in vid_title: vid_title = vid_title.replace('&amp;', 'and')
                if link == '_blank': link = 'This video has not been released yet!'
                formatted_videos.append(dict(title=vid_title, link=link))
            challenges[title][int(day)] = formatted_videos
    
    f.close()
    return challenges

def chloe_ting_challenge(selected_challenge, selected_day):
    ''' 
    chloe_ting_challenge.txt

    - challenge titles begin with T>  (eg. T>4 Weeks Summer Shred Challenge)
    - day number is separated from videos with ">"
    - videos each day are separated with ","
    - videos that are not out yet are denoted by _blank
    - optional videos begin with * (eg. *https://youtu.be/-p0PA9Zt8zk|title1,https://youtu.be/OBSUUi0FAKo|title2,...)
    - video titles are stored after the link, separated from link with "|" (eg. look at example above)
    '''

    challenges = get_challenges()

    if not selected_day.isdigit(): 
        return 'Oops, you did not enter a number for your day number!'

    selected_day = int(selected_day)
    if selected_day > len(challenges[selected_challenge]):
        return 'Oops, this challenge is not that long!'

    reply = f'<b>{selected_challenge} Day {selected_day}</b>\nHere are your videos for today!\nWhile you do not have to complete the videos in this order, it is recommended by Chloe that you do so.\n\n'
    selected_videos = challenges[selected_challenge][selected_day]
    rest_day = True
    for cur_video in selected_videos:
        if cur_video['link'] != '':
            rest_day = False
            if cur_video['link'][0] == '*': 
                reply += f'Optional:\n{cur_video["title"]}: {cur_video["link"].lstrip("*")}\n\n'
            else:
                reply += f'{cur_video["title"]}: {cur_video["link"]}\n\n'
        
    if rest_day: reply = f'*{selected_challenge} Day {selected_day}*\nLooks like today is your rest day! You have no videos for today.'
    return reply

def chloe_ting_handler(update, context):
    text = update.message.text.strip()
    titles = get_titles()

    if text == '/chloeting':
        reply = f"Here are Chloe Ting's Challenges.\n\n" + '\n'.join([f"{index+1}) {title}" for (index, title) in enumerate(titles)]) + f"\n\nPlease enter the number of the challenge you are looking for, followed by the day number using the /chloeting command. (eg. for day 7 of {titles[0]}, enter /chloeting 1 7)"
    else:
        if len(text.split(' ')) != 3:
            reply = 'Oops, the format of your request was incorrect!'
        elif int(text.split(' ')[1]) > len(titles):
            reply = 'Oops, there isn\'t a challenge with that number!'
        else:
            command, challenge_index, day = text.split(' ')
            reply = chloe_ting_challenge(titles[int(challenge_index)-1], day)
    update.message.reply_html(reply)
