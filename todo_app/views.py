from django.shortcuts import render,redirect
from django.views.generic import View,FormView
from todo_app.forms import RegistrationForm,LoginForm,TaskForm,PasswordResetForm
from django.contrib.auth.models import User
from todo_app.models import Task
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.

def sign_required(fn):

    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you should login first")
            return redirect("signin")
        return fn(request,*args,**kw)
    return wrapper


class SignUpView(View):
    model = User
    template_name = "register.html"
    form_class = RegistrationForm

    def get(self,request,*args,**kw):
        form = self.form_class
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kw):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully registered!")
            return redirect("signin")
        return render(request,self.template_name,{"form":form})
    
class SignInView(View):
    model = User
    template_name = "login.html"
    form_class = LoginForm

    def get(self,request,*args,**kw):
        form = self.form_class
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kw):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pd = form.cleaned_data.get('password')
            usr = authenticate(request,username=uname, password = pd)
            if usr:
                login(request,usr)
                messages.success(request, "logined successfully")
                return redirect("index")
            messages.error(request, "login unsuccessfull")
            return render(request,self.template_name,{"form":form})
        
def signout_view(request,*args,**kw):
    logout(request)        
    messages.success(request,"logout succesfully")
    return redirect("signin")

@method_decorator(sign_required,name="dispatch")
class IndexView(View):
    template_name = "index.html"
    def get(self,request,*args,**kw):
        return render(request,self.template_name)
@method_decorator(sign_required,name="dispatch")
class TaskCreateView(View):
    model = Task
    template_name = "task-add.html"
    form_class = TaskForm
    def get(self,request,*args,**kw):
        form = self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kw):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"success")
            return redirect('task-list')
        messages.error(request,"unsuccess")
        return render(request,{"form":form})
@method_decorator(sign_required,name="dispatch")        
class TaskListView(View):
    model = Task
    template_name = "task-list.html"
    def get(self,request,*args,**kw):
        qs = Task.objects.filter(user = request.user).order_by("-created_date")
        return render(request,self.template_name,{"tasks":qs})
@method_decorator(sign_required,name="dispatch")
class TaskDetailView(View):
    model = Task
    template_name = "task-detail.html"

    def get(self,request,*args,**kw):
        id = kw.get('pk')
        qs = Task.objects.get(id = id)
        return render(request,self.template_name,{"task":qs})
@method_decorator(sign_required,name="dispatch")
class TaskEditView(View):
    model = Task
    form_class = TaskForm
    template_name = "task-edit.html"

    def get(self,request,*args,**kw):
        id = kw.get('pk')
        obj = Task.objects.get(id=id)
        form = self.form_class(instance=obj)
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kw):
        id = kw.get('pk')
        obj = Task.objects.get(id=id)
        form = self.form_class(instance=obj,data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"todo changed")
            return redirect("task-list")
        messages.error(request,"failed")
        return render(request,self.template_name,{"form":form})

@sign_required    
def task_delete_view(request,*args,**kw):
    id = kw.get("pk")
    Task.objects.get(id=id).delete() 
    return redirect('task-list')

class PasswordResetView(FormView):
    model = User
    template_name = 'passwordreset.html'
    form_class = PasswordResetForm

    def post(self,request,*args,**kw):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            pwd1= form.cleaned_data.get("password1")
            pwd2 = form.cleaned_data.get("password2")

        if pwd1 == pwd2:
            try:
                usr = User.objects.get(username = username, email = email)
                usr.set_password(pwd1)
                usr.save()
                messages.success(request,"password changed")
                return redirect('signin')
            except Exception as e:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})
        else:
            messages.error(request,"password mismatch")
            return render(request,self.template_name,{"form":form})
