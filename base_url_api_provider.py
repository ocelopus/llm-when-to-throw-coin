# --- 配置 ---

with open("base-url.txt", "r") as f:
    BASE_URL = f.read()  # 确保末尾没有 /


with open("API-key.txt", "r") as f:
    API_KEY = f.read()

API_KEYS = [
    API_KEY
]
