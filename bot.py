import requests
import json
import re
import time
import random

def get_live():
    # Sử dụng nhiều link dự phòng của web
    urls = ["https://hoiquan2.live", "https://sv2.hoiquan2.live/trang-chu"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://hoiquan2.live/"
    }

    final_channels = []
    
    for target_url in urls:
        try:
            res = requests.get(target_url, headers=headers, timeout=15)
            # Tìm link các trận đấu
            matches = re.findall(r'/truc-tiep/[^"\'>\s]+', res.text)
            matches = list(dict.fromkeys(matches))

            for path in matches:
                m_url = f"https://sv2.hoiquan2.live{path}"
                try:
                    m_res = requests.get(m_url, headers=headers, timeout=10)
                    # Quét tất cả các link m3u8 có trong trang
                    links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', m_res.text)
                    if links:
                        # Ưu tiên link có chứa token session
                        stream = max(links, key=len)
                        name = path.split('/')[-1].replace('-', ' ').title()
                        
                        # Thêm mã ngẫu nhiên sau tên để ép App cập nhật danh sách mới
                        rand_id = random.randint(100, 999)
                        
                        final_channels.append({
                            "name": f"⚽ {name} [{rand_id}]",
                            "link": stream,
                            "headers": {
                                "User-Agent": headers["User-Agent"],
                                "Referer": "https://sv2.hoiquan2.live/",
                                "Origin": "https://sv2.hoiquan2.live"
                            }
                        })
                except:
                    continue
            if final_channels: break # Nếu đã có trận thì không cần quét web dự phòng nữa
        except:
            continue

    # Nếu vẫn không có trận nào, lấy tạm kênh K+ nhưng phải đổi link mới
    if not final_channels:
        final_channels = [{
            "name": f"🔄 Đang cập nhật trận mới ({time.strftime('%H:%M')})",
            "link": "https://tftv0gr3uomttgr31hcjt8rzdncbafi1g1hdcgyhdrpjqci1gq3mpcfhgg3dq.100ycdn.com/live/kplus_sport1/playlist.m3u8",
            "headers": {"Referer": "https://sv2.hoiquan2.live/"}
        }]

    output = {
        "name": f"VINH LIVE - {time.strftime('%d/%m %H:%M')}",
        "groups": [{"group_name": "LIVE FOOTBALL", "channels": final_channels}]
    }

    with open("list.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_live()
