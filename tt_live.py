from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, JoinEvent, GiftEvent

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="mootsfollower")


# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(event: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

# @client.on("like")
# async def on_like(event: LikeEvent):
#     print(f"@{event.user.unique_id} liked the stream!")
    
# @client.on("join")
# async def on_join(event: JoinEvent):
#     print(f"@{event.user.unique_id} joined the stream!")
        

@client.on("gift")
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")

# # Notice no decorator?
# async def on_comment(event: CommentEvent):
#     print(f"{event.user.nickname} -> {event.comment}")
    


# Define handling an event via a "callback"
# client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()