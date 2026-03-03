import requests
import json
import re

def get_all_live_links():
    target_url = "https://sv2.hoiquan2.live/trang-chu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://sv2.hoiquan2.live/"
    }

    final_channels = []
    try:
        # Bước 1: Lấy toàn bộ trang chủ
        response = requests.get(target_url, headers=headers, timeout=20)
        html = response.text
        
        # Bước 2: Tìm tất cả các đường dẫn trận đấu (Regex quét rộng hơn)
        # Tìm các link có cấu trúc /truc-tiep/bong-da/... hoặc các môn khác
        match_paths = re.findall(r'/truc-tiep/[^"\'>\s]+', html)
        # Loại bỏ trùng lặp và sắp xếp
        match_paths = sorted(list(set(match_paths)))

        print(f"Tìm thấy {len(match_paths)} trận đấu đang chờ quét...")

        for path in match_paths:
            match_url = f"https://sv2.hoiquan2.live{path}"
            try:
                # Bước 3: Truy cập từng trận để bóc tách link m3u8
                match_res = requests.get(match_url, headers=headers, timeout=10)
                match_html = match_res.text
                
                # Tìm link m3u8 (ưu tiên các link có token/session)
                m3u8_links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', match_html)
                
                if m3u8_links:
                    # Lấy link đầu tiên (thường là Server chính)
                    link_stream = m3u8_links[0]
                    
                    # Làm sạch tên trận đấu từ URL (Ví dụ: mu-vs-arsenal -> MU Vs Arsenal)
                    raw_name = path.split('/')[-1].split('.')[-2] if '.' in path else path.split('/')[-1]
                    clean_name = raw_name.replace('-', ' ').title()
                    
                    final_channels.append({
                        "name": f"⚽ {clean_name}",
                        "link": link_stream,
                        "headers": {
                            "User-Agent": headers["User-Agent"],
                            "Referer": "https://sv2.hoiquan2.live/",
                            "Origin": "https://sv2.hoiquan2.live"
                        }
                    })
                    print(f"Đã lấy link cho: {clean_name}")
            except:
                continue # Nếu lỗi 1 trận thì bỏ qua, quét tiếp trận sau

    except Exception as e:
        print(f"Lỗi tổng: {e}")

    # Bước
