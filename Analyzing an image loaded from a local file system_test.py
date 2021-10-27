import boto3
import csv
import json
from playsound import playsound

with open('Squirrel_accessKeys.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]

# rekognition
client = boto3.client('rekognition',
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      region_name='us-west-1')
# 要讀取之檔案
photo='imgs\complex.jpg'

# with open(photo, 'rb') as imgfile:
#     imgbytes = imgfile.read()
# response = client.detect_labels(Image={'Bytes': imgbytes}, Attributes=['ALL'])

with open(photo, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

#圖片檢測到Labels
print('Detected labels in ' + photo)  

#對於每個Labels偵測準確性之可信度分數，以百分比顯示。
for label in response['Labels']:
    print (label['Name'] + ' : ' + str(round(label['Confidence'],3)))
    
label_count=len(response['Labels'])
print("Labels detected: " + str(label_count)) 

# for label in response['Labels']:
#     print(label['Name']=='Person')
  
wh=wnum=namenum=i=0
n=len(response['Labels'])
d1=[0]*n
d2=[0]*4

# for label in response['Labels']:
#     if label['Name']=='Person':
#         print(i)
#         break
#     i+=1
        
while i<n:
    d1[i]=response['Labels'][i]
    if response['Labels'][i]['Name']=='Person':namenum=i
    i+=1
print('\nPerson位置 : ' + str(namenum))
print('\nInstances內容 : \n'+ str(response['Labels'][namenum]['Instances']))
wnum=len(response['Labels'][namenum]['Instances'])
print('\nBoundingBox個數(代表Person人數) : '+str(wnum))

for w in range(wnum):
    print(str(response['Labels'][namenum]['Instances'][w]['BoundingBox']['Width']))
    print(str(response['Labels'][namenum]['Instances'][w]['BoundingBox']['Height'])+'\n')
    
w=h=[0]*wnum
while wh<wnum:
    w[wh]=response['Labels'][namenum]['Instances'][wh]['BoundingBox']['Width']
    h[wh]=response['Labels'][namenum]['Instances'][wh]['BoundingBox']['Height']
    if w[wh]>=0.4 or h[wh]>=0.4:
        playsound('explosion-yin-xiao.mp3', block=True)
        break
    wh+=1
    
# Instancesnums=response['Labels'][i]['Instances'][0]

# d2 =  json.dumps(response['Labels'])
# type(label['Name'])
# type(response['Labels'][0])
# d2.keys()

# d1 =  json.dumps(response['Labels'][0]['Instances'])
# num=d1.count('BoundingBox') 
