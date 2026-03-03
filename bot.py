import requests
import json
import re
import time

def get_all_live_links():
    target_url = "https://sv2.hoiquan2.live/trang-chu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://sv2.hoiquan2.live/",
        "Origin": "https://sv2.hoiquan2.live"
    }

    final_channels = []
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        # Tìm tất cả các link trận đấu
        match_paths = re.findall(r'/truc-tiep/[^"\'>\s]+', response.text)
        match_paths = list(dict.fromkeys(match_paths)) # Xóa trùng nhưng giữ thứ tự

        for path in match_paths:
            match_url = f"https://sv2.hoiquan2.live{path}"
            try:
                # Thêm một chút thời gian nghỉ để tránh bị chặn
                time.sleep(1)
                match_res = requests.get(match_url, headers=headers, timeout=10)
                
                # Tìm link m3u8 có token wsSession (Đây là link đang phát thật)
                # Chúng ta quét rộng hơn để lấy link từ server CDN
                m3u8_links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', match_res.text)
                
                if m3u8_links:
                    # Lấy link dài nhất (thường là link chứa nhiều Token nhất)
                    link_stream = max(m3u8_links, key=len)
                    
                    # Tạo tên trận đấu sạch sẽ
                    name_parts = path.strip('/').split('/')
                    clean_name = name_parts[-1].replace('-', ' ').title() if name_parts else "Trận đấu trực tiếp"

                    final_channels.append({
                        "name": f"⚽ {clean_name}",
                        "link": link_stream,
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

    # Cấu trúc JSON có thêm dấu thời gian để App không bị Cache
    output = {
        "name": f"Vinh Lee Live ({time.strftime('%H:%M')})",
        "groups": [
            {
                "group_name": "🔥 BÓNG ĐÁ TRỰC TIẾP",
                "channels": final_channels
            }
        ],
        "updated_at": time.time() # Ép App phải nhận diện đây là file mới
    }

    with open("list.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_all_live_links()
