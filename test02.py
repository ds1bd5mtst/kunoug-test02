# -*- coding: utf-8 -*-
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess

account_name='ds1bd5mtst'
account_key='QRW6ikCh6i2TAOZsJnAuliDJX03xU8xmm3GVhsLFD8cw3Z9yjOLZVE3CYdgKpV+74D4y1dKCsK6bd5fjUup3LQ=='
container_name='testcontainer'
file_name='test02.csv'

service = BlockBlobService(account_name=account_name,account_key=account_key)
# service.create_container(container_name)
# service.create_blob_from_path(container_name,'test02.csv',file_path)
service.get_blob_to_path(container_name,file_name,'test02.csv')


import pandas as pd
#df = pd.read_csv(file_name)
#print(df)

# url="https://ds1bd5mtst.blob.core.windows.net/testcontainer/test02.csv"
#table=pd.read_csv(file_name)
df = pd.DataFrame(columns=['title', 'ID', 'status', 'owner', 'rentaldate', 'limitdate', 'place'])
title = "book1"
ID = 1
status = 0
owner = ""
rentaldate = 0
limitdate = 0
place = "shelf1"
se = pd.Series([title,ID,status,owner,rentaldate,limitdate,place],['title', 'ID', 'status', 'owner', 'rentaldate', 'limitdate', 'place'])
df = df.append(se, ignore_index=True)

title = "book2"
ID = 1
status = 0
owner = ""
rentaldate = 0
limitdate = 0
place = "shelf2"
se = pd.Series([title,ID,status,owner,rentaldate,limitdate,place],['title', 'ID', 'status', 'owner', 'rentaldate', 'limitdate', 'place'])
df = df.append(se, ignore_index=True)

df = df.append(se, ignore_index=True)
title = "book13"
ID = 1
status = 0
owner = ""
rentaldate = 0
limitdate = 0
place = "shelf2"
se = pd.Series([title,ID,status,owner,rentaldate,limitdate,place],['title', 'ID', 'status', 'owner', 'rentaldate', 'limitdate', 'place'])
df = df.append(se, ignore_index=True)

title = "book1"
ID = 2
status = 0
owner = ""
rentaldate = 0
limitdate = 0
place = "shelf1"
se = pd.Series([title,ID,status,owner,rentaldate,limitdate,place],['title', 'ID', 'status', 'owner', 'rentaldate', 'limitdate', 'place'])
df = df.append(se, ignore_index=True)

df.to_csv(file_name)

# 読み込み
a = pd.read_csv(file_name)
print(a)

# 検索
kensaku = "k1"
list = []
for index, row in df.iterrows():
    print(row["title"])
    if row["title"].find(kensaku) != -1:
        #print("あった")
        list.append(row["title"])
    else:
        print("なかった")
# 重複排除して表示する
result_list = set(list)
print(result_list)


# blobにアップロード
service.create_blob_from_path(container_name, file_name, 'test02.csv')

# ファイルの削除
import os
os.remove(file_name)
