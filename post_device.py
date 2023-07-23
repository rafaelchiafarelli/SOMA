import requests
res = requests.post('http://localhost:5000/device_register', json={ "character":"SOMA",
"IP":"192.168.15.1",
"PORT":"80",
"type":"Messenger",
"endpoints":["Fundo", "Magistrado"],
"animations":{
    "window":[1080,1920],
    "window_number":1,
    "step_ms":200,
    "ondemand_max":5,
    
    "sequences":[
    {
    "name":"Fundo",
    "type":"permanent",
    "order":"background",
    "repeat":3,
    "pos":{"x":0, "y":0,"w":800, "h":600},
    "names":[
    "/home/skiafa/workspace/VideoManager/pictures/sleep_1.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_2.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_3.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_4.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_5.png"
    ],
    "last_one":{
        "has_last":True,
        "file_name":"/home/skiafa/workspace/VideoManager/pictures/sleep_over.png"
        }

    },
    {
    "name":"Magistrado",
    "type":"ondemand",
    "order":"foreground",
    "repeat":10,
    "pos":{"x":0, "y":0,"w":800, "h":600},
    "names":[
    "/home/skiafa/workspace/VideoManager/pictures/sleep_1.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_2.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_3.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_4.png",
    "/home/skiafa/workspace/VideoManager/pictures/sleep_5.png"
    ],
    "last_one":{
        "has_last":True,
        "file_name":"/home/skiafa/workspace/VideoManager/pictures/sleep_over.png"
        }
    }]
}
})
if res.ok:
    print(res.json())