# import requests
# import json
# import time

# BASE_URL = "http://127.0.0.1:8000"
# HEALTH_URL = f"{BASE_URL}/health"
# GENERATE_URL = f"{BASE_URL}/generate"

# payload = {
#     "prompt": "Giải thích trí tuệ nhân tạo là gì trong 2 câu ngắn gọn.",
#     "max_new_tokens": 100,
#     "temperature": 0.7,
#     "top_p": 0.9
# }

# def wait_for_service(timeout=180):
#     print(">> Checking service health...")
#     start = time.time()

#     while time.time() - start < timeout:
#         try:
#             r = requests.get(HEALTH_URL, timeout=5)
#             if r.status_code == 200:
#                 print(">> Service is healthy:", r.json())
#                 return True
#             else:
#                 print(f">> Health not ready: {r.status_code} - {r.text}")
#         except requests.RequestException:
#             pass

#         time.sleep(2)

#     return False

# def call_generate():
#     print("\n>> Sending request to /generate with payload:")
#     print(json.dumps(payload, indent=2, ensure_ascii=False))

#     try:
#         response = requests.post(GENERATE_URL, json=payload, timeout=180)
#         print(f"\n>> Status code: {response.status_code}")

#         try:
#             print(json.dumps(response.json(), indent=2, ensure_ascii=False))
#         except ValueError:
#             print(response.text)

#     except requests.exceptions.RequestException as e:
#         print(f"\n>> Request error: {e}")

# if __name__ == "__main__":
#     if wait_for_service():
#         call_generate()
#     else:
#         print(">> Service did not become healthy in time.")
        
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
HEALTH_URL = f"{BASE_URL}/health"
GENERATE_URL = f"{BASE_URL}/generate"

valid_payload_1 = {
    "prompt": "Giải thích AI là gì trong 2 câu ngắn.",
    "max_new_tokens": 80,
    "temperature": 0.7,
    "top_p": 0.9
}

valid_payload_2 = {
    "prompt": "Viết 3 gạch đầu dòng về lợi ích của học Python.",
    "max_new_tokens": 120,
    "temperature": 0.6,
    "top_p": 0.95
}


invalid_payload = {
    "prompt": "   ",
    "max_new_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.9
}


def wait_for_service(timeout=180):
    print(">> Checking service health...")
    start = time.time()

    while time.time() - start < timeout:
        try:
            r = requests.get(HEALTH_URL, timeout=5)
            if r.status_code == 200:
                print(">> Service is healthy:", r.json())
                return True
            else:
                print(f">> Health not ready: {r.status_code} - {r.text}")
        except requests.RequestException:
            pass

        time.sleep(2)

    return False


def run_test(test_name, payload, expected_status):
    print(f"\n===== {test_name} =====")
    print(">> Payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(GENERATE_URL, json=payload, timeout=180)
        print(f">> Status code: {response.status_code} (expected {expected_status})")

        try:
            body = response.json()
            print(">> Response:")
            print(json.dumps(body, indent=2, ensure_ascii=False))
        except ValueError:
            print(">> Response text:")
            print(response.text)

        if response.status_code == expected_status:
            print(">> RESULT: PASS")
        else:
            print(">> RESULT: FAIL")

    except requests.exceptions.RequestException as e:
        print(f">> Request error: {e}")
        print(">> RESULT: FAIL")


if __name__ == "__main__":
    if wait_for_service():
        run_test("TEST 1 - VALID INPUT", valid_payload_1, 200)
        run_test("TEST 2 - VALID INPUT", valid_payload_2, 200)
        run_test("TEST 3 - INVALID INPUT (EMPTY PROMPT)", invalid_payload, 400)
    else:
        print(">> Service did not become healthy in time.")