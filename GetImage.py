import wget
import json
import requests
import os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def Select():
    ##----------------Select rover------------------------------
    RoverNames = []
    dict = {}
    response = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={key}")
    response = response.json()
    for rover in response["rovers"]:
        RoverNames.append(rover)

    for i in range(len(RoverNames)):
        print(f"[{i+1}] {RoverNames[i]['name']}: Landing date={RoverNames[i]['landing_date']}, Newest images={RoverNames[i]['max_date']}, Status={RoverNames[i]['status']}, Total photos={RoverNames[i]['total_photos']}")

    dict["rover"] = RoverNames[int(input(':'))-1]
    ##--------------Select Date--------------------------------
    print("Date format YYYY-MM-DD.")
    dict["date"] = input("Date: ")
    ##--------------Select camera------------------------------
    for i in range(len(dict["rover"]["cameras"])):
        print(f"[{i+1}] {dict['rover']['cameras'][i]['full_name']}")

    inp = input(": ")
    dict["camera"] = {}
    if inp.upper() == "ALL":
        dict["camera"]["option"]=""
        dict["camera"]["name"] = f'all'

    elif int(inp) in range(20):
        dict["camera"]["option"] = f'&camera={dict["rover"]["cameras"][int(inp)-1]["name"]}'
        dict["camera"]["name"] = f'{dict["rover"]["cameras"][int(inp)-1]["full_name"]}'

    return dict

def move(y, x):
    print("\033[%d;%dH" % (y, x))

try:
    TEMP = []
    f = open("api_key.txt")
    for line in f:
        TEMP.append(line)
    key = TEMP[0].rstrip("\n")

except:
    print("no api_key.txt file found using demo key.\n you can only make 30 requests per hour")
    print("Create a key at api.nasa.gov to get 1000 requests per hour.")
    key = "DEMO_KEY"

if requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={key}").status_code != 200:
    print("Api key invalid or overused\nExiting...")
    exit()
images = []



clear()
options = Select()



data = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{options['rover']['name']}/photos?earth_date={options['date']}{options['camera']}&api_key={key}")

data = data.json()

print(f"Downloading {len(data['photos'])} photos.")

for photo in data["photos"]:
    images.append(photo["img_src"])

os.chdir("./imgs/")
for i in range(len(images)):
    clear()
    print(f"[{i+1}/{len(images)}]\n\n")
    print(f"{wget.download(images[i])}")

print("\n")
print("--------Options--------")
print(f"Rover: {options['rover']['name']}")
print(f"Date: {options['date']}")
print(f"Camera: {options['camera']['name']}")
