import requests
import json
import re

def get_links():
    # Bước này bot sẽ truy cập web để lấy link
    # Tạm thời tôi để link mẫu, sau này mình sẽ nâng cấp code cào thực tế
    target_url = "https://sv2.hoiquan2.live/trang-chu"
    
    # Cấu trúc JSON chuẩn Monplayer
    data = {
        "name": "Vinh Lee Auto",
        "groups": [
            {
                "group_name": "Bóng Đá Live",
                "channels": [
                    {
                        "name": "K+ Sport 1 (Auto)",
                        "link": "https://tftv0gr3uomttgr31hcjt8rzdncbafi1g1hdcgyhdrpjqci1gq3mpcfhgg3dq.100ycdn.com/live/kplus_sport1/playlist.m3u8",
                        "headers": {"Referer": "https://sv2.hoiquan2.live/"}
                    }
                ]
            }
        ]
    }
    
    with open("list.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_links()
