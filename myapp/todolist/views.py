from __future__ import unicode_literals

from .models import TodoList, Category
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render,redirect
import random
import datetime
from .models import TodoList, Category, Fruits


# Idea: make a fruit and a task for each task you make
#     When you delete the task, the fruit is not deleted
#     when the task is checked, the fruit appears and will stay there since it exists
#     eventually, the "fruit" wiill be checked



def index(request):  # the index view
    todos = TodoList.objects.all()  # quering all todos with the object manager
    categories = Category.objects.all()  # getting all categories with object manager
    allFruits = Fruits.objects.all()
    fruitTypes = ["apple", "orange", "lemon", "pear"]

    # TODO: If you want to associate a certain category with a fruit, make it a dictionary

    if request.method == "POST":  # checking if the request method is a POST
        if "taskAdd" in request.POST:  # checking if there is a request to add a todo
            title = request.POST["description"]  # title
            date = str(request.POST["date"])  # date
            category = request.POST["category_select"]  # category
            content = title + " -- " + date + " " + category  # content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()  # saving the todo
            return redirect("/list")  # reloading the page

        if "taskDelete" in request.POST:  # checking if there is a request to delete a todo
            checkedList = request.POST.getlist("checkedbox")
            for i in checkedList:
                toDelete = TodoList.objects.get(id = int(i))
                toDelete.delete()

        if "addBasket" in request.POST:
            checkedList = request.POST.getlist("checkedbox")
            for i in checkedList:
                toDelete = TodoList.objects.get(id=int(i))
                toDelete.delete()
                fruitInfo = "{category}: '{taskName}' completed on {timezone}".format(
                                                        category=str(toDelete.category),
                                                        taskName=toDelete.title,
                                                       timezone=datetime.datetime.now().strftime("%m-%d-%Y"))

                chosenFruit = random.choice(fruitTypes)
                newFruit = Fruits(info = fruitInfo, type = chosenFruit)
                newFruit.save()

        if "emptyBasket" in request.POST:
            for i in allFruits:
                i.delete()
            return redirect("/list")


    return render(request, "index.html", {"todos": todos, "categories": categories, "allFruits": allFruits})


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            username = request.POST['username']
            request.session['username'] = username
            return redirect("/list")
        else:
            # Return an 'invalid login' error message.
            return render(request, "loginErrors.html", {})
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")
