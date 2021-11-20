from django.shortcuts import render,redirect
from django.views import View
from . import forms
from django.contrib.auth.models import auth,User
import dbinfo
import gridfs
import base64
from bson.objectid import ObjectId


class HomePage(View):
    def get(self,request):
        collection = dbinfo.database['product_details']
        
        data = list()
        fs = gridfs.GridFS(dbinfo.database)
        for item in collection.find():
            image_path = fs.get(ObjectId(item['image_id']))
           
            product_info = {
                'uid':item['uid'],
                'price':item['price'],
                'product_name':item['product_name'],
                'image_path': base64.b64encode(image_path.read()).decode('utf-8')
            }
            data.append(product_info)
            
        content = {
            'page_title':'Home Page',
            'product_list': data
        }
        
        return render(request,'index.html',content)



class LoginUser(View):
    def get(self,request):
        content = {
            'page_title':'Login Page',
            'login_form':forms.LoginForm()
        }
        return render(request,'login_page.html',content)

    def post(self,request):
        user_name = request.POST['user_name']
        password = request.POST['password']

        user = auth.authenticate(username = user_name , password = password)

        if user is not None:
            auth.login(request,user)
        
        return redirect('/')


class SignupUser(View):
    def get(self,request):
        content = {
            'page_title':'Signup Page',
            'signup_form':forms.SignupForm()
        }
        return render(request,'signup_page.html',content)

    def post(self,request):
        user_name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']
        confirmed_password = request.POST['confirmed_password']

        if password == confirmed_password:
            new_user = User.objects.create_user(
                username = user_name,
                password = password,
                email = email
            )
            new_user.save()

        return redirect('/login')




class LogoutUser(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/')
