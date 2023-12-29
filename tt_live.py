from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, JoinEvent, GiftEvent, ShareEvent, FollowEvent, EnvelopeEvent
from datetime import datetime
# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="yourtakdir")


def save_to_csv(user_id, user_nick, event, filename):
    print(user_id)
    # Mendapatkan waktu saat ini
    current_time = datetime.now()
    # Mencetak waktu saat ini dalam format tertentu (opsional)
    # Memisahkan waktu menjadi tanggal dan jam
    formatted_date = current_time.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%H:%M:%S")
    # Menyimpan alamat IP ke dalam file CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Menulis alamat IP baru
        writer.writerow([formatted_date, formatted_time, event, user_id, user_nick])  

        
        
# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(event: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("like")
async def on_like(event: LikeEvent):
    # save_to_csv(event.user.unique_id,event.user.nickname,1,'output.csv')
    # print(f"@{event.user.unique_id} liked the stream!")
    pass

@client.on("comment")
async def on_connect(event: CommentEvent):
    # print(f"{event.user.nickname} -> {event.comment}")
    pass
@client.on("join")
async def on_join(event: JoinEvent):
     save_to_csv(event.user.unique_id,event.user.nickname,1,'output.csv')
    # print(f"@{event.user.unique_id} joined the stream!")
    # pass
        
@client.on("share")
async def on_share(event: ShareEvent):
    # print(f"@{event.user.unique_id} shared the stream!")
    pass
@client.on("follow")
async def on_follow(event: FollowEvent):
    # print(f"@{event.user.unique_id} followed the streamer!")
    pass
@client.on("gift")
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")


@client.on("envelope")
async def on_connect(event: EnvelopeEvent):
    print(f"{event.treasure_box_user.unique_id} -> {event.treasure_box_data}")
    

@client.on("error")
async def on_connect(error: Exception):
    # Handle the error
    if isinstance(error, SomeRandomError):
        print("Handle some error!")
        return

    # Otherwise, log the error
    # You can use the internal method, but ideally your own
    client._log_error(error)


# # Notice no decorator?
# async def on_comment(event: CommentEvent):
#     print(f"{event.user.nickname} -> {event.comment}")
    
# # Define handling an event via a "callback"
# client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()