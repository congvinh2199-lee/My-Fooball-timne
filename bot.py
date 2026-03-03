import requests
import json
import re
import time

def get_live():
    url = "https://sv2.hoiquan2.live/trang-chu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://sv2.hoiquan2.live/"
    }

    channels = []
    try:
        # 1. Lấy trang chủ
        res = requests.get(url, headers=headers, timeout=15)
        # 2. Tìm link các trận
        matches = re.findall(r'/truc-tiep/[^"\'>\s]+', res.text)
        matches = list(dict.fromkeys(matches)) # Xóa trùng

        for path in matches:
            m_url = f"https://sv2.hoiquan2.live{path}"
            try:
                m_res = requests.get(m_url, headers=headers, timeout=10)
                # 3. Lấy link m3u8 thật
                links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', m_res.text)
                if links:
                    stream = max(links, key=len)
                    # Lấy tên trận đấu từ đường dẫn
                    name = path.strip('/').split('/')[-1].replace('-', ' ').title()
                    
                    channels.append({
                        "name": f"⚽ {name}",
                        "link": stream,
                        "headers": {
                            "User-Agent": headers["User-Agent"],
                            "Referer": "https://sv2.hoiquan2.live/",
                            "Origin": "https://sv2.hoiquan2.live"
                        }
                    })
            except:
                continue
    except Exception as e:
        print(f"Lỗi: {e}")

    # Nếu không quét được trận nào thì mới hiện K+
    if not channels:
        channels = [{"name": "📺 K+ Sport 1", "link": "https://tftv0gr3uomttgr31hcjt8rzdncbafi1g1hdcgyhdrpjqci1gq3mpcfhgg3dq.100ycdn.com/live/kplus_sport1/playlist.m3u8"}]

    output = {
        "name": f"VINH LIVE - {time.strftime('%H:%M')}",
        "groups": [{"group_name": "BÓNG ĐÁ HÔM NAY", "channels": channels}]
    }

    with open("list.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_live()
