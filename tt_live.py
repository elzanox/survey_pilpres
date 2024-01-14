from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *
import csv
import json
from datetime import datetime
comment_path = "data/data_comment.json"
gift_path = "data/data_gift.json"

# like_path = "data/data_like.json"
# follow_path = "data/data_follow.json"
# share_path = "data/data_share.json"

# Menyimpan ke file CSV
csv_comment_fields = ["date","time","user_id", "comment"]  # Ganti dengan nama kolom yang sesuai
csv_gift_fields = ["date","time","user_id", "count","gift"]  # Ganti dengan nama kolom yang sesuai
csv_comment_path = "comments.csv"  # Ganti dengan path file CSV yang sesuai
csv_gift_path = "gifts.csv"  # Ganti dengan path file CSV yang sesuai
allowed_gifts = ["Rose", "Coffee", "Orange Juice"]
allowed_comments = ["1", "2", "3",
                    "01","02","03"]
# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="@majnunmlbb")
    
# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)
    
@client.on("disconnect")
async def on_disconnect(event: DisconnectEvent):
    print("Disconnected")
    
# @client.on("like")
# async def on_like(event: LikeEvent):
#     print(f"@{event.user.unique_id} liked the stream!")
    
# @client.on("join")
# async def on_join(event: JoinEvent):
#     print(f"@{event.user.unique_id} joined the stream!")
    
# @client.on("follow")
# async def on_follow(event: FollowEvent):
#     print(f"@{event.user.unique_id} followed the streamer!")
    
# @client.on("share")
# async def on_share(event: ShareEvent):
#     print(f"@{event.user.unique_id} shared the stream!")


class TikTokCommentExtractor:
        def __init__(self, comment_event):
            self.comment_event = comment_event

        def to_dict(self):
            data_user = {
                "user_id": self.comment_event.user.user_id,
                "nickname": self.comment_event.user.nickname,
                "avatar": {
                    "urls": self.comment_event.user.avatar.urls,
                    "uri": self.comment_event.user.avatar.uri
                },
                "unique_id": self.comment_event.user.unique_id,
                "sec_uid": self.comment_event.user.sec_uid,
                "info": {
                    "following": self.comment_event.user.info.following,
                    "followers": self.comment_event.user.info.followers,
                    "follow_role": self.comment_event.user.info.follow_role
                }
                # ,
                # "badges": self.comment_event.user.badges
            }

            data_komentar = {
                "user": data_user,
                "comment": self.comment_event.comment,
                "mentions": self.comment_event.mentions,
                "images": self.comment_event.images,
                "language": self.comment_event.language
            }

            return data_komentar
        
# Notice no decorator?
@client.on("comment")
async def on_comment(event: CommentEvent):
    # Mengasumsikan comment_event adalah instance dari TikTokLive.types.events.CommentEvent
    comment_event = event  # Ganti ... dengan instance sebenarnya

    # Membuat instance dari TikTokCommentExtractor
    comment_extractor = TikTokCommentExtractor(comment_event)

    # Ekstraksi data dan konversi ke format JSON
    data_json_komentar = json.dumps(comment_extractor.to_dict(), indent=2)
    # Data yang akan ditulis ke dalam file CSV
    
    # Menyimpan ke file atau digunakan sesuai kebutuhan
    with open(comment_path, 'a') as file:
        
        try:
            
            file.write(data_json_komentar +',' +'\n' )
        except TypeError as e:
            print(f"TypeError: {e}")
            
    # print("Data komentar berhasil diekstraksi dan disimpan dalam data_komentar.json")
    print(type(event.comment))
    print(event.comment)
    if event.comment in allowed_comments:
        current_datetime = datetime.now()
        
        # Data yang akan ditulis ke dalam file CSV
        data = {"date":current_datetime.strftime("%d/%m/%y"),
                "time":current_datetime.strftime("%H:%M:%S"),
                "user_id": event.user.user_id,
                "comment": event.comment}
        with open(csv_comment_path, 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_comment_fields)

            try:
            # Menulis header hanya jika file CSV baru
                if csv_file.tell() == 0:
                    csv_writer.writeheader()

                # Menulis data ke file CSV
                csv_writer.writerow(data)
            except UnicodeEncodeError as e:
                print(f"UnicodeEncodeError: {e}")
                # Handle kesalahan di sini, jika diperlukan

class TikTokGiftExtractor:
        def __init__(self, gift_event):
            self.gift_event = gift_event

        def to_dict(self):
            data_user = {
                "user_id": self.gift_event.user.user_id,
                "nickname": self.gift_event.user.nickname,
                "avatar": {
                    "urls": self.gift_event.user.avatar.urls,
                    "uri": self.gift_event.user.avatar.uri
                },
                "unique_id": self.gift_event.user.unique_id,
                "sec_uid": self.gift_event.user.sec_uid,
                "info": {
                    "following": self.gift_event.user.info.following,
                    "followers": self.gift_event.user.info.followers,
                    "follow_role": self.gift_event.user.info.follow_role
                }
                # ,
                # "badges": self.gift_event.user.badges
            }
            data_gift = {
                "gift_id": self.gift_event.gift.id,
                "count": self.gift_event.gift.count,
                "repeat_end": self.gift_event.gift.repeat_end,
                "info": {
                    "name": self.gift_event.gift.info.name,
                    "diamond_count,": self.gift_event.gift.info.diamond_count,
                    "type,": self.gift_event.gift.info.type,
                    "description,": self.gift_event.gift.info.description,
                },
                "recipient": {
                    "timestamp": self.gift_event.gift.recipient.timestamp,
                    "user_id": self.gift_event.gift.recipient.user_id
                }
                # ,
                # "recipient": {
                #     "timestamp": self.gift_event.gift.recipient.timestamp,
                #     "user_id": self.gift_event.gift.info.user_id
                # }
                # ,
                # "badges": self.gift_event.user.badges
            }
            
            gift_data = {
                "user": data_user,
                "gift": data_gift
                # "mentions": self.gift_event.mentions,
                # "images": self.gift_event.images,
                # "language": self.gift_event.language
            }

            return gift_data
        
@client.on("gift")
async def on_gift(event: GiftEvent):
    # print(event)
    
    
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")
            # Mengasumsikan comment_event adalah instance dari TikTokLive.types.events.CommentEvent
        gift_event = event  # Ganti ... dengan instance sebenarnya

        # Membuat instance dari TikTokgiftExtractor
        gift_extractor = TikTokGiftExtractor(gift_event)
        # Ekstraksi data dan konversi ke format JSON
        data_json_gift = json.dumps(gift_extractor.to_dict(), indent=2)

        
        # Menyimpan ke file atau digunakan sesuai kebutuhan
        with open(gift_path, 'a') as file:
            file.write(data_json_gift +'\n'+','+'\n')
        # print("Data gift berhasil diekstraksi dan disimpan dalam data_gift.json")
        
        if event.gift.info.name in allowed_gifts:
            current_datetime = datetime.now()
            # Data yang akan ditulis ke dalam file CSV
            data = {"date":current_datetime.strftime("%d/%m/%y"),
                    "time":current_datetime.strftime("%H:%M:%S"),
                    "user_id": event.user.user_id,
                    "count": event.gift.count,
                    "gift":event.gift.info.name
                    }
            with open(csv_gift_path, 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=csv_gift_fields)
                try:
                # Menulis header hanya jika file CSV baru
                    if csv_file.tell() == 0:
                        csv_writer.writeheader()

                    # Menulis data ke file CSV
                    csv_writer.writerow(data)
                except UnicodeEncodeError as e:
                    print(f"UnicodeEncodeError: {e}")
                    # Handle kesalahan di sini, jika diperlukan

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")
            # Mengasumsikan comment_event adalah instance dari TikTokLive.types.events.CommentEvent
        gift_event = event  # Ganti ... dengan instance sebenarnya

        # Membuat instance dari TikTokgiftExtractor
        gift_extractor = TikTokGiftExtractor(gift_event)
        # Ekstraksi data dan konversi ke format JSON
        data_json_gift = json.dumps(gift_extractor.to_dict(), indent=2)

        # Menyimpan ke file atau digunakan sesuai kebutuhan
        with open(gift_path, 'a') as file:
            file.write(data_json_gift +'\n'+','+'\n')
        # print("Data gift berhasil diekstraksi dan disimpan dalam data_gift.json")

        if event.gift.info.name in allowed_gifts:
            current_datetime = datetime.now()
            # Data yang akan ditulis ke dalam file CSV
            data = {"date":current_datetime.strftime("%d/%m/%y"),
                    "time":current_datetime.strftime("%H:%M:%S"),
                    "user_id": event.user.user_id,
                    "count": event.gift.count,
                    "gift":event.gift.info.name
                    }
            with open(csv_gift_path, 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=csv_gift_fields)
                try:
                # Menulis header hanya jika file CSV baru
                    if csv_file.tell() == 0:
                        csv_writer.writeheader()

                    # Menulis data ke file CSV
                    csv_writer.writerow(data)
                except UnicodeEncodeError as e:
                    print(f"UnicodeEncodeError: {e}")
                    # Handle kesalahan di sini, jika diperlukan


# Define handling an event via a "callback"
# client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()