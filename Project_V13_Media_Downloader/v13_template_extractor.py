import sys
from PIL import Image
import os

# Cấu hình encoding cho Console Windows
sys.stdout.reconfigure(encoding='utf-8')

# Đường dẫn ảnh mẫu
input_file = r"C:\Users\vu.hoang\.gemini\antigravity\scratch\ces-academy-automation\Project_V12_Desktop_Capture\zalo_pro_captures\page_001.png"
output_icon = "zalo_download_icon.png"

def extract_template():
    if not os.path.exists(input_file):
        print("❌ Không tìm thấy ảnh mẫu page_001.png")
        return

    img = Image.open(input_file)
    width, height = img.size
    print(f"📐 Kích thước ảnh gốc: {width}x{height}")

    # Ước tính tọa độ Icon Download trong Zalo (Dựa trên page_001.png)
    # File nằm ở phía dưới, icon download thường nằm ở mép phải của khung File
    # Toạ độ ước tính từ ảnh crop:
    # Thử cắt một vùng nhỏ xung quanh vị trí file
    # X: ~680 to 710, Y: ~320 to 350 (Tỉ lệ tương đối)
    
    # Để chắc chắn, em sẽ cắt một vùng 40x40 chứa icon
    # Toạ độ này cần được kiểm chứng qua việc xem lại ảnh page_001.png
    # Dựa trên ảnh: icon nằm bên phải chữ 'docx', kích thước khoảng 24x24
    
    # Cắt thử vùng chứa icon download (Vị trí x=311, y=411 trong ảnh crop 1296x816?)
    # Thực tế trong page_001.png (đã crop): 
    # Left=0.28 (362), Right=0.73 (946)
    # Icon nằm gần mép phải (946). Thử lấy x=550 to 580 trong ảnh đã crop.
    
    # Dùng toạ độ cố định từ quan sát pixel:
    # x: 555, y: 412, size: 22
    icon_region = (554, 411, 578, 435) 
    
    icon = img.crop(icon_region)
    icon.save(output_icon)
    print(f"✅ Đã trích xuất và lưu icon tại: {output_icon}")

if __name__ == "__main__":
    extract_template()
