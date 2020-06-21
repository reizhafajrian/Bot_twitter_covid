#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 01:12:41 2020

@author: reizha
"""
import requests
import tweepy
import time
CONSUMER_KEY=''#api consumer key dari twitter developer
CONSUMER_SECRET=''#api consumer secret dari twitter developer
ACCESS_KEY=''#api access key dari twitter developer
ACCESS_SECRET=''#api access secret dari twitter developer

auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api=tweepy.API(auth,wait_on_rate_limit=True)#menginisialisasi api


FILENAME='Covid_19.txt'#txt sebagai temp sementara untuk membandingkan data baru
resp=requests.get("https://api.kawalcorona.com/indonesia/")#api untuk covid 19 indonesia
res_prov=requests.get("https://api.kawalcorona.com/indonesia/provinsi")#api covid 19 untuk provinsi di indo

new_data=resp.json()#mengambil data sebagai list dict
data_provinsi=res_prov.json()#mengambil data sebagai list dict
new_data.extend(data_provinsi)#menambahkan data provinsi kedalam new data

#membaca file txt
n=open(FILENAME,"r")
data_txt=str(n.read())
n.close
#mengubah data di dalam txt menjadi list dict
data_from_txt=list(eval(data_txt))

#looping untuk selama lamanya
while True:
    for i in range(len(new_data)):#looping sebanyak data di dalam newdata
        if data_from_txt[i]==new_data[i]:#mengecek apakah data update atau tidak
            print("data sama ", i )
        else:#jika terjadi perbedaan maka data telah di update
        #melakukan write ke txt lama di isi dengan data baru
            print("data Beda", i)
            f=open(FILENAME,"w")
            f.write(str(new_data))
            f.close()
            kasus_indo_positif=(new_data[0].get('positif'))
            kasus_indo_dirawat=(new_data[0].get('dirawat'))
            kasus_indo_meninggal=(new_data[0].get('meninggal'))
            kasus_indo_sembuh=(new_data[0].get('sembuh'))
            if i!=0:
                provinsi=(new_data[i].get('attributes')).get('Provinsi')
                Kasus_positif=(new_data[i].get('attributes')).get('Kasus_Posi')
                Kasus_sembuh=(new_data[i].get('attributes')).get('Kasus_Semb')
                Kasus_meninggal=(new_data[i].get('attributes')).get('Kasus_Meni')
                hasil=("Update Corona di Provinsi : "+str(provinsi)+",Kasus Positif Sebanyak : "+str(Kasus_positif)+
                                  ",Kasus Sembuh sebanyak : "+str(Kasus_sembuh)+",Korban Meninggal Dunia Sebanyak : "+str(Kasus_meninggal))
                api.update_status('{}'.format(hasil))
                
                hasil_prov=("Dengan bertambahnya kasus Covid-19 di provinsi : "+str(provinsi)+",maka jumlah kasus postif Covid-19 di Indonesia menjadi : "+
                                  str(kasus_indo_positif)+",jumlah kasus yang berhasil disembuhan sebanyak : "+str(kasus_indo_sembuh)+
                                  "jumlah kasus yang masih dalam perawatan sebanyak : "+str(kasus_indo_dirawat)+"jumlah kasus meninggal sebanyak "+str(kasus_indo_meninggal))
                api.update_status('{}'.format(hasil_prov))
            else:
               hasil_ind=("Update jumlah kasus postif Covid-19 di Indonesia menjadi : "+
                                 str(kasus_indo_positif)+",jumlah kasus yang berhasil sembuh sebanyak : "+str(kasus_indo_sembuh)+
                                 ",jumlah kasus yang masih dalam perawatan sebanyak : "+str(kasus_indo_dirawat)+"jumlah kasus meninggal sebanyak : "
                                 +str(kasus_indo_meninggal))
               api.update_status('{}'.format(hasil_ind))
    time.sleep(43200)
               

