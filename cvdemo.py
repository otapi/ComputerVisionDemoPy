import requests
import json
from io import BytesIO
import tkinter as tk
from PIL import ImageTk, Image
"""
Computer Vision Demo 
Demo Microsoft's Computer Visio

Requirements: Python 3.6+
python -m pip install pillow

"""
# Set image_url to the URL of an image that you want to analyze.
image_url = "https://kep.cdn.indexvas.hu/1/0/3156/31562/315621/31562139_2422923_7002e673ede4c75128eabfe8265c224c_wm.jpg"
# Add your Computer Vision subscription key and endpoint to your environment variables.
subscription_key = ""

endpoint = "https://westcentralus.api.cognitive.microsoft.com/"
analyze_url = endpoint + "vision/v2.1/analyze"
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

# API reference: https://westus.dev.cognitive.microsoft.com/docs/services/5cd27ec07268f6c679a3e641/operations/56f91f2e778daf14a499f21b
params = {'visualFeatures': 'Adult,Brands,Categories,Description,Color,Faces,ImageType,Objects,Tags',
            'details': 'Celebrities,Landmarks',
            'language': 'en'}
data = {'url': image_url}
response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(json.dumps(analysis, indent=4, sort_keys=True))

image_caption = analysis["description"]["captions"][0]["text"].capitalize()

root = tk.Tk()
caption = tk.Label(root, text=image_caption)
caption.pack()

jsontext = tk.Text(root)
jsontext.insert(tk.INSERT, json.dumps(analysis, indent=4, sort_keys=True))
jsontext.width = 10

vbar=tk.Scrollbar(root,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=jsontext.yview)
jsontext.config(yscrollcommand=vbar.set)
jsontext.pack(side = tk.RIGHT, fill=tk.Y)

photo = ImageTk.PhotoImage(Image.open(BytesIO(requests.get(image_url).content)), master=root)
label = tk.Label(root, image = photo)
label.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES)

root.mainloop()