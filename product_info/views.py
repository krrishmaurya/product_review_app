from django.shortcuts import render, redirect
from django.views import View
from . import forms
import dbinfo
import gridfs
import string
import random
from bson.objectid import ObjectId
import base64


class NewProduct(View):
    def get(self, request):
        if request.user.is_superuser:
            content = {
                "page_title": "Add new product",
                "new_product_form": forms.NewProductForm(),
            }
            return render(request, "new_product.html", content)

        return redirect("/")

    def get_random_string(self):
        length = 10
        collection = dbinfo.database['fs.files']
        chars = string.ascii_letters + '0123456789'
        while True:
            file_name = ''.join(random.choices(chars, k=length))
            if file_name not in collection.find():
                break

        return file_name

    def post(self, request):
        
        image = request.FILES["product_image"]
        name, extension = image.name.split(".")
        uid = self.get_random_string()
        file_name = f"{uid}.{extension}"

        print(file_name)
        collection = dbinfo.database["product_details"]
        fs = gridfs.GridFS(dbinfo.database)
        file_id = fs.put(image, filename=file_name)
        new_product = {
            "product_name": request.POST["product_name"],
            "price": request.POST["price"],
            "description": request.POST["description"],
            "image_id": file_id,
            'uid': uid,
            'reviews':[]
        }
        collection.insert(new_product)
        return redirect("/")


class ProductInfo(View):
    def get(self, request):
        collection = dbinfo.database['product_details']
        fs = gridfs.GridFS(dbinfo.database)
        uid = request.GET['uid']
        product_info = collection.find_one({'uid': uid})
        image_id = product_info['image_id'] 
        image_path = fs.get(ObjectId(image_id))
        
        content = {
            'page_title': 'Product Info',
            'product_info': product_info,
            'image_path': base64.b64encode(image_path.read()).decode('utf-8'),
        }

        return render(request, 'product_info.html', content)


class NewReview(View):
    def post(self,request):
        collection = dbinfo.database['product_details']
        uid = request.POST['uid']
        user_name = request.user.username,
        rating = request.POST['rating']
        feedback = request.POST['feedback']
        product = collection.find_one({'uid':uid})
        old_data = product['reviews']
        
        data_to_add = {
                'user_name':user_name[0],
                'feedback':feedback,
                'rating':rating
        }
        
        new_data = list()
        new_data.append(data_to_add)
        new_data = new_data+old_data
        collection.update_one(
            {
                'uid':uid
            },
            {
                '$set':{
                    'reviews':new_data
                }
            },
            upsert=False,
        )
        return redirect('/')


# {
#     'uid':{
#         'user_1':{
#             'rating':3,
#             'feedback':'sdfdfsd'
#         }
#     }
# }

# {
#     "_id": {"$oid": "616058bfa1199fe3d117c2d9"}, 
#     "product_name": "Dosa", 
#     "price": "999999",
#     "description": "This is best dosa in the world including gold dust",
#      "image_id": {"$oid": "616058bea1199fe3d117c2d7"}, 
#      "uid": "ucyt2mPRNZ"
# }

