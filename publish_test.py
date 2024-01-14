# Misalnya, Anda memiliki daftar badge seperti ini:
badges = [
    Badge(badge_scene_type=10, image=TikTokImage(urls=['https://p16-webcast.tiktokcdn.com/webcast-va/fans_badge_icon_lv10_v0.png~tplv-obj.image', 'https://p19-webcast.tiktokcdn.com/webcast-va/fans_badge_icon_lv10_v0.png~tplv-obj.image'], uri='webcast-va/fans_badge_icon_lv10_v0.png'), label=None, name='Ⅱ')
]

# Variabel untuk menyimpan nilai masing-masing atribut
badge_scene_type = badges[0].badge_scene_type
image_urls = badges[0].image.urls
uri = badges[0].uri
label = badges[0].label
name = badges[0].name

# Cetak nilai variabel
print(f"Badge Scene Type: {badge_scene_type}")
print(f"Image URLs: {image_urls}")
print(f"URI: {uri}")
print(f"Label: {label}")
print(f"Name: {name}")
