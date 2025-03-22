import requests
import re

session = requests.Session()

# دریافت هش به صورت خودکار
def get_upload_hash():
	response = session.get("https://uupload.ir/")
	match = re.search(r'name="hash" value="(.*?)"', response.text)
	return match.group(1) if match else None

# آدرس آپلود
upload_url = "https://s6.uupload.ir/sv_process.php"

# مسیر فایل برای آپلود
file_path = "test.mp3"  # میتونی jpg یا mp3 باشه

# دریافت هش به صورت خودکار
hash_value = get_upload_hash()

if not hash_value:
    print("❌ Error: Hash value not found!")
    exit()
else:
    print("✅ Hash received: ", hash_value)
	
# تنظیم مدت زمان برای 1 روز (86400 ثانیه)
data = {
	"hash": hash_value,
	"ittl": "86400"
}

headers = {
	"User-Agent": "Mozilla/5.0",
	"Referer": "https://uupload.ir/",
	"Origin": "https://uupload.ir"
}

# ارسال فایل
with open(file_path, "rb") as file:
	files = {"__userfile[]": file}
	response = session.post(upload_url, data=data, files=files, headers=headers)

# بررسی پاسخ سرور
if response.status_code == 200:
	response_text = response.text

	# استخراج لینک مستقیم برای عکس
	direct_link_match = re.search(r'https://s\d+.uupload.ir/files/[\w\d_-]+\.(jpg|jpeg|png|gif|bmp|mp3)', response_text)
	# استخراج لینک صفحه دانلود (برای mp3)
	page_link_match = re.search(r'https://uupload.ir/view/[\w\d_-]+\.(mp3|jpg|jpeg|png|gif|bmp)', response_text)

	if direct_link_match:
		print("✅ Direct file link:", direct_link_match.group())
	elif page_link_match:
		print("📌 Download page link:", page_link_match.group())
	else:
		print("❌ Error: No valid link found in server response!")
else:
	print(f"❌ Upload failed! Status code: {response.status_code}")
