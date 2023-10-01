from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here. 
def home(request):
    return render(request, "dashboard/home.html")

@login_required
def notes(request):
    form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    context = {"notes": notes, "form": form}

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"{note.title} added successfully!")
            return redirect("notes")
            
        return render(request, "dashboard/notes.html", context)
    
    return render(request, "dashboard/notes.html", context)

@login_required
def delete_note(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    messages.success(request, f"{note.title} deleted successfully!")
    return redirect("notes")


class NotesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = "dashboard/notes_detail.html"

@login_required
def homework(request):
    form = HomeWorkForm()
    homeworks = HomeWork.objects.filter(user=request.user).order_by("finished", "due")
    homework_done = True if len(homeworks.filter(finished=False)) == 0 or len (homeworks) == 0 else False
    context = {"homeworks": homeworks, "homework_done": homework_done, "form": form}

    if request.method == "POST":
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            messages.success(request, f"{homework.title} added successfully!")
            return redirect("homeworks")
        
        return render(request, "dashboard/homework.html", context)

    return render(request, "dashboard/homework.html", context)

@login_required
def update_homework(request, pk):
    homework = HomeWork.objects.get(pk=pk)
    homework.finished = True if homework.finished==False else False
    homework.save()
    return redirect("homeworks")

@login_required
def delete_homework(request, pk):
    homework = HomeWork.objects.get(pk=pk)
    homework.delete()
    messages.success(request, f"{homework.title} deleted successfully!")
    return redirect("homeworks")


def youtube(request):
    form = DashboardForm()
    context = {"form": form}
    if request.method== "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        video = VideosSearch(text, limit=10)
        result_list = []
        for video in video.result()["result"]:
            result_dict = {
                "input": text,
                "title": video["title"],
                "duration": video["duration"],
                "thumbnail": video["thumbnails"][0]["url"],
                "channel": video["channel"]["name"],
                "link": video["link"],
                "views": video["viewCount"]["short"],
                "published": video["publishedTime"],
            }
            desc = ""
            if video["descriptionSnippet"]:
                for text in video["descriptionSnippet"]:
                    desc += text["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)
        context["results"] = result_list
        return render(request, "dashboard/youtube.html", context)

    return render(request, "dashboard/youtube.html", context)

@login_required
def todo(request):
    todos = Todo.objects.filter(user=request.user).order_by("finished")
    form = TodoForm()
    todo_done = True if len(todos.filter(finished=False)) == 0 or len(todos) ==0 else False
    context = {"todos": todos, "todo_done": todo_done, "form": form}

    if request.method == "POST":
        form = TodoForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, f"{todo.title} added successfully!")
            return redirect("todos")
        
        return render(request, "dashboard/todo.html", context)
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.finished = True if todo.finished==False else False
    todo.save()
    return redirect("todos")


@login_required
def delete_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.delete()
    messages.success(request, f"{todo.title} deleted successfully!")
    return redirect("todos")


def books(request):
    form = DashboardForm()
    context = {"form": form}
    if request.method== "POST":
        form = DashboardForm(request.POST)
        context = {"form": form}
        text = request.POST["text"]
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                "title": answer["items"][i]["volumeInfo"]["title"],
                "subtitle": answer["items"][i]["volumeInfo"].get("subtitle"),
                "description": answer["items"][i]["volumeInfo"].get("description"),
                "count": answer["items"][i]["volumeInfo"].get("pageCount"),
                "categories": answer["items"][i]["volumeInfo"].get("categories"),
                "rating": answer["items"][i]["volumeInfo"].get("averageRating"),
                "thumbnail": answer["items"][i]["volumeInfo"].get("imageLinks")['thumbnail'],
                "preview": answer["items"][i]["volumeInfo"].get("previewLink"),
            }
            result_list.append(result_dict)
        context["results"] = result_list
        return render(request, "dashboard/books.html", context)

    return render(request, "dashboard/books.html", context)

def dictionary(request):
    form = DashboardForm()
    context = {"form": form}
    if request.method== "POST":
        form = DashboardForm(request.POST)
        context = {"form": form}
        text = request.POST["text"]
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]["phonetics"][0]["text"]
        except: phonetics = ""
        try:
            audio= answer[0]["phonetics"][0]["audio"]
        except: audio = ""
        try:
            definition = answer[0]["meanings"][0]["definitions"][0]["definition"]
        except: definition = ""
        try:
            example = answer[0]["meanings"][0]["definitions"][0]["example"]
        except: example = ""
        try:
            synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
        except: synonyms = ""
        context["input"] = text
        context["phonetics"] = phonetics
        context["audio"] = audio
        context["definition"] = definition
        context["example"] = example
        context["synonyms"] = synonyms
        return render(request, "dashboard/dictionary.html", context)
    return render(request, "dashboard/dictionary.html", context)


def wiki(request):
    form = DashboardForm()
    context = {"form": form}
    if request.method== "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        search = wikipedia.page(text)
        context = {"form": form, "title":search.title, "link": search.url, "details": search.summary}
        return render(request, "dashboard/wiki.html", context)
    return render(request, "dashboard/wiki.html", context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST["measurement"] == "length":
            measurement_form = ConversionLengthForm()
            context = {"form":form, "m_form":measurement_form, "input": True}
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input)>=0:
                    if first == "yard" and second == "foot":
                        answer = f"{input} yard = {int(input)*3} foot"
                    elif first == "foot" and second == "yard":
                        answer = f"{input} foot = {int(input)/3} yard"
                context = {"form":form, "m_form":measurement_form, "input": True, "answer":answer}
        elif request.POST["measurement"] == "mass":
            measurement_form = ConversionMassForm()
            context = {"form":form, "m_form":measurement_form, "input": True}
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input)>=0:
                    if first == "pound" and second == "kilogram":
                        answer = f"{input} pound = {int(input)*0.453592} kilogram"
                    elif first == "kilogram" and second == "pound":
                        answer = f"{input} kilogram = {int(input)/0.453592} pound"
                context = {"form":form, "m_form":measurement_form, "input": True, "answer":answer}

        return render(request, "dashboard/conversion.html", context)


    form = ConversionForm()
    context = {"form": form, "input": False}

    return render(request, "dashboard/conversion.html", context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(f"Account created for {form.cleaned_data['username']} successfully!")
            return redirect("login")
        context = {"form": form}
        return render(request, "dashboard/register.html", context)
        
    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "dashboard/register.html", context)

@login_required
def profile(request):
    homeworks = HomeWork.objects.filter(finished=False, user=request.user)
    todos = Todo.objects.filter(finished=False, user=request.user)
    homeworks_done = True if len(homeworks) == 0 else False
    todos_done = True if len(todos) == 0 else False
    context = {"homeworks":homeworks, "todos":todos, "homeworks_done": homeworks_done, "todos_done":todos_done}
    return render(request, "dashboard/profile.html", context)