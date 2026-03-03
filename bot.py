import requests
import json
import re

def get_live_links():
    target_url = "https://sv2.hoiquan2.live/trang-chu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://sv2.hoiquan2.live/"
    }

    channels = []
    try:
        # Bước 1: Truy cập trang chủ để tìm các trận đang Live
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text
        
        # Tìm các link trận đấu (thường có dạng /truc-tiep/...)
        matches = re.findall(r'/truc-tiep/[^"\']+', html)
        # Loại bỏ các link trùng lặp
        matches = list(set(matches))

        for match_path in matches[:10]: # Lấy tối đa 10 trận hot nhất
            match_url = f"https://sv2.hoiquan2.live{match_path}"
            
            # Bước 2: Vào từng trận để tìm link m3u8
            match_res = requests.get(match_url, headers=headers, timeout=10)
            # Tìm link m3u8 có chứa token (wsSession)
            m3u8_links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', match_res.text)
            
            if m3u8_links:
                # Lấy link đầu tiên tìm thấy
                final_link = m3u8_links[0]
                # Tách tên trận đấu từ đường dẫn cho đẹp
                match_name = match_path.split('/')[-1].replace('-', ' ').title()
                
                channels.append({
                    "name": f"⚽ {match_name}",
                    "link": final_link,
                    "headers": {
                        "User-Agent": headers["User-Agent"],
                        "Referer": "https://sv2.hoiquan2.live/",
                        "Origin": "https://sv2.hoiquan2.live"
                    }
                })

    except Exception as e:
        print(f"Lỗi rồi: {e}")

    # Nếu không quét được trận nào, thêm 2 kênh K+ dự phòng để file không bị trống
    if not channels:
        channels = [
            {"name": "📺 K+ Sport 1 (Dự phòng)", "link": "https://tftv0gr3uomttgr31hcjt8rzdncbafi1g1hdcgyhdrpjqci1gq3mpcfhgg3dq.100ycdn.com/live/kplus_sport1/playlist.m3u8"},
            {"name": "📺 K+ Sport 2 (Dự phòng)", "link": "https://tftv0gr3uomttgr31hcjt8rzdncbafi1g1hdcgyhdrpjqci1gq3mpcfhgg3dq.100ycdn.com/live/kplus_sport2/playlist.m3u8"}
        ]

    # Cấu trúc JSON cuối cùng
    full_data = {
        "name": "Vinh Lee - Auto Update",
        "groups": [{"group_name": "Bóng Đá Trực Tiếp", "channels": channels}]
    }

    with open("list.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_live_links()
