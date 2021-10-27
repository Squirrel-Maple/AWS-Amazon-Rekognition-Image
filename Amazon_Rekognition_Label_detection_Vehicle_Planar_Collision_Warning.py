# In[0] 前置作業區塊
import boto3
import csv
from playsound import playsound
import cv2

#將AWS_accessKeys帶入
with open('Squirrel_accessKeys.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]
        
# 使用Amazon Rekognition服務
client = boto3.client('rekognition',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key,region_name='us-west-1')

# 讀取之原圖檔案
img = cv2.imread(r'imgs\complex.jpg')  
#print(img.shape)  顯示原圖像數大小

x = 500  # 裁切區域的 x 與 y 座標（左上角）
y = 0
w = 1800  # 裁切區域的長度與寬度
h = 4000

crop_img = img[y:y+h, x:x+w]  # 裁切圖片
cv2.imwrite(r'imgsupdate\updateimg.jpg', crop_img)  #裁切後圖片寫入檔案，並另存至專屬裁切後圖片資料夾

# 讀取裁切後之檔案
photo=r'imgsupdate\updateimg.jpg'

# with open(photo, 'rb') as imgfile:
#     imgbytes = imgfile.read()
# response = client.detect_labels(Image={'Bytes': imgbytes}, Attributes=['ALL'])

with open(photo, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})
    
# In[1] 後續分析資料輸出

#圖片檢測到Labels
print('\nDetected labels in ' + photo+'\n')  

#對於每個類別Labels偵測準確性之可信度分數，以百分比顯示
print('每類別Labels偵測準確性之可信度分數(以%顯示) : ')
for label in response['Labels']:print(label['Name'] + ' : ' + str(round(label['Confidence'],3)) + '%')
    
#類別Labels的個數
label_count=len(response['Labels'])
print("\nLabels detected: " + str(label_count)+'\n') 
  
wh=i=j=k=0
#判斷類別名稱為Person(人)、Car(汽車)、Motorcycle(機車)、Bus(公車)、Bicycle(自行車)
while i<len(response['Labels']):
    #d1[i]=response['Labels'][i]
    totaltext=['Person','Car','Motorcycle','Bus','Bicycle']
    for j in range(len(totaltext)):
        #判斷totaltext當中需要提取的類別Labels
        if response['Labels'][i]['Name']==totaltext[j]:
            print('*'*35)
            #顯示各類別Labels的位置
            print('類別為 '+totaltext[j]+' 的(Index)位置 : ' + str(i))
             
            #計算各類別邊界框(BoundingBox)個數
            whnum=len(response['Labels'][i]['Instances'])
            print('其邊界框(BoundingBox)個數 : '+str(whnum)+'\n')
            
            w=[0]*whnum
            h=[0]*whnum
            # for wh in range(whnum):
            #     #寬度(Width) — 週框方塊的寬度，以整體影像寬度的比例表示。
            #     #高度(Height) — 週框方塊的高度，以整體影像高度的比例表示。
            #     w[wh]=round(response['Labels'][i]['Instances']\
            #                 [wh]['BoundingBox']['Width']*100,3)
            #     h[wh]=round(response['Labels'][i]['Instances']\
            #                 [wh]['BoundingBox']['Height']*100,3)
                  #預設時數50km，則占比>=5則執行警告音(根據所需類別Labels數量執行)
                  #預設時數60km，則占比>=4則執行警告音(根據所需類別Labels數量執行)
            #     if w[wh]>=5 or h[wh]>=5:
            #         playsound('explosion-yin-xiao.mp3', block=True)
            #         break
             
            #顯示各類別邊界框(BoundingBox)各占比多少    
            for wh in range(whnum):
                #寬度(Width) — 週框方塊的寬度，以整體影像寬度的比例表示。
                #高度(Height) — 週框方塊的高度，以整體影像高度的比例表示。
                w[wh]=round(response['Labels'][i]['Instances']\
                            [wh]['BoundingBox']['Width']*100,3)
                h[wh]=round(response['Labels'][i]['Instances']\
                            [wh]['BoundingBox']['Height']*100,3)
                print('第 '+str(wh+1)+' 個邊界框寬度(Width)占比 : '+str(w[wh])+'%')
                print('第 '+str(wh+1)+' 個邊界框高度(Height)占比 : '+str(h[wh])+'%'+'\n') 
                #預設時數50km，則占比>=5則執行警告音(只執行一次)
                #預設時數60km，則占比>=4則執行警告音(只執行一次)
                if (w[wh]>=5 or h[wh]>=5) and k!=1:
                    playsound(r'E:\AI BigData Programming\20210727group_part1_thematic_plan\explosion-yin-xiao.mp3', block=True)
                    k=1
    i+=1