# coding=utf8

import time
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8") 


class ImageSearchService(object):
    def __init__(self):
        super(ImageSearchService, self).__init__()
        
    def get_upload_image_path_by_id(self, image_id):
        return 'uploads/%s.jpg' % image_id

    def save_image(self, image_binary):
        image_id = "image_%d" % int(time.time() * 1000)
        with open(self.get_upload_image_path_by_id(image_id), 'wb') as f:
            f.write(image_binary)
        return image_id

    def search(self, image_id):
        image_path = self.get_upload_image_path_by_id(image_id)
        li = [('image/img/Striped_Linen_Ringer_Tee/img_00000006.jpg',1.0),('image/img/Striped_Linen_Ringer_Tee/img_00000007.jpg', 0.9902234033924513),('image/img/Striped_Linen_Ringer_Tee/img_00000007.jpg', 0.9902234033924513)]
        return {
            "time_secs": 0.1,
            "image_size": "200 × 300",
            "result": li
        }



class KeywordSearchService(object):
    def __init__(self):
        super(KeywordSearchService, self).__init__()
    def get_score(self,keyword,x):
        print keyword
        print x
        keywordli=keyword.split()
        xli=x.split('_')
        print keywordli
        print xli

        keycom=[]
        xcom=[]
        sum1=0
        sum2=0
        sum3=0
        comli=keywordli+xli
        comli=list(set(comli))
        for k in comli:
            if k in keywordli:
                keycom.append(1)
            else:
                keycom.append(0)
            if k in xli:
                xcom.append(1)
            else:
                xcom.append(0)
        for (key,x) in zip(keycom,xcom):
            sum1+=key*x
        for key in keycom:
            sum2+=key*key
        for x in xcom:
            sum3+=x*x
        print sum1/((sum2*sum3)**0.5)
        return (sum1/((sum2*sum3)**0.5))


    def search(self, keyword):
        li=[]
        keyword_image_path='images/img/'
        for x in os.listdir(keyword_image_path):
            fp = os.path.join(keyword_image_path, x)          
            if self.get_score(str(keyword),x)>=0.5:
            #if str(keyword) in x:               
                for y in os.listdir(fp):
                    img = os.path.join(fp, y) 
                    li.append(('image/'+img[7:],1.0))
        return {
            "time_secs": 0.1,
            "image_size": "200 × 300",
            "result": li
        }






        
       