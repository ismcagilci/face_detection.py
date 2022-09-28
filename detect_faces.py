import base64
import requests
import pandas as pd
import time

with open("football_team.jpeg", "rb") as image_file:
  encoded_string = base64.b64encode(image_file.read()).decode("utf8")

def get_job_id():
    while True:
        try:
            #send image
            api_call = requests.post("https://platform.api.cameralyze.com/application/triggers/programatic/run", json={"applicationUuid": "26a2015b-91a9-49ca-8e8e-246033b09ad4", "apiKey": "DZT13xVbPjxPCYhS", "image": encoded_string})
            if api_call.status_code == 200:
                response = api_call.json()
                get_job_id = response["data"]["job_id"]
                return get_job_id
            else:
                print("Request was failed, It will try again in 2 seconds")
                time.sleep(2)
        except Exception as e:
            print(e)

def get_face_images_data(job_id):
    # get detected faces
    get_faces_url = "https://platform.api.cameralyze.com/application/triggers/programatic/result/get"
    while True:
        try:
            api_call_v2 = requests.post(get_faces_url, json={"apiKey": "DZT13xVbPjxPCYhS", "jobId":job_id})
            if api_call_v2.status_code == 200:
                response_v2 = api_call_v2.json()
                return response_v2
            else:
                print("Request was failed, It will try again in 2 seconds")
                time.sleep(2)
        except Exception as e:
            print(e)

def load_data(req):
    while True:
        try:
            return req["data"]["detections"]
        except:
            print("Data is still preparing...")
            time.sleep(5)

job_id = get_job_id()
get_req = get_face_images_data(job_id)
face_images_data = load_data(get_req)

new_dict = {"confidence": [], "left": [], "top": [], "width": [], "height": []}
for image in face_images_data:
    for key, value in image.items():
        get_data_list = new_dict[key]
        get_data_list.append(value)
        new_dict[key] = get_data_list

new_df = pd.DataFrame(new_dict)
new_df.to_excel("face_images.xlsx")