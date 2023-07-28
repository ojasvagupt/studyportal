from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import *
import requests
import wikipedia


# Create your views here.

def home(request):
    return render(request,'study/home.html')

def notes(request):
    if request.method == 'POST':
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
    else:
        form=NotesForm

    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'study/notes.html',context)

def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


def homework(request):
    if request.method =='POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished==False
            except:
                finished=False
            homeworks=Homework(
                                user=request.user,
                                subject=request.POST['subject'],
                                title=request.POST['title'],
                                description=request.POST['description'],
                                due=request.POST['due'],
                                is_finished=finished
                           )
            homeworks.save()
    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    context={
                'homeworks':homework,
                'form':form,
        }
    return render(request,'study/homework.html',context)


def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished == False
    else:
        homework.is_finished == True
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def todo(request):
    if request.method=='POST':
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todos=Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    context={
        'todos':todo,
        'forms':form,
    }
    return render(request,'study/todo.html',context)

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')


def books(request):
    if request.method=='POST':
        form=studyform(request.POST)
        text=request.POST['text']
        url='https://www.googleapis.com/books/v1/volumes?q='+text
        r=requests.get(url)
        answer = r.json()
        result_list=[]
        for i in range(7):
            result_dict={

                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context={
                'forms':form,
                'results':result_list
            }
        return render(request,'study/books.html',context)
    else:
        form=studyform()
    context={
        'forms':form
       }
    return render(request,'study/books.html',context)

    
def dictionary(request):
    if request.method=="POST":
        form=studyform(request.POST)
        text=request.POST['text']
        url='https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['defintions'][0]['definition']
            example = answer[0]['meanings'][0]['defintions'][0]['example']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example
            }
        except:
            context = {
                'forms':form,
                'input':''
            }
        return render(request,"study/dictionary.html",context)

    else:
        form=studyform()
        context = {'forms':form}
    return render(request,"study/dictionary.html",context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = studyform(request.POST)
        search = wikipedia.page(text)
        context = {
            'forms':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'study/wiki.html',context)
    else:
        form=studyform()
        context={
            'forms':form,
        }
    return render(request,'study/wiki.html',context)

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context={
        'forms':form
    }
    return render(request,'study/register.html',context)
