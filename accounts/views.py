from django.shortcuts import render,redirect
from django.views import View
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout




class SignupView(View):
    def get(self,request):
        form=SignupForm()
        return render(request,'accounts/signup.html',{'form':form})
    def post(self,request):
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'signup successful')
            return redirect('accounts:login')
        return render(request,'accounts/signup.html',{'form':form})
    
    

class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'accounts/login.html',{'form':form})
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            u=form.cleaned_data['username']
            p=form.cleaned_data['password']
            user=authenticate(request,username=u,password=p)
            if user is None:
                messages.error(request,"invalid username or password")
                return redirect('accounts:login')
            login(request,user)
            messages.success(request,"Login successful")
            if user.is_superuser:
                return redirect('adminpanel:admin-dashboard')
            return redirect('bookings:user-home')
        else:
            messages.error(request,"form not valid")
            return redirect('accounts:login')
        
        
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('accounts:login')
            

