import markdown2
import random
# from bs4 import BeautifulSoup
from django import forms
from django.shortcuts import render

from . import util


class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, title):
    entry = util.get_entry(title)
    if entry:
        entry = markdown2.markdown(entry)
    else:
        return render(request, "encyclopedia/notfound.html", {
            "error": entry
        })

    return render(request, "encyclopedia/content.html", {
        "title": title,
        "entry": entry,
    })


def search(request):
    if request.method == 'POST':
        query = request.POST.get('value', '')
        print(query)
        search_value = util.get_entry(query)
        if search_value:
            search_value = markdown2.markdown(search_value)
        else:
            return render(request, "encyclopedia/list.html", {
                "entries": util.list_entries()
            })

        return render(request, "encyclopedia/search.html", {
            "search": search_value
        })


def createNewPage(request):
    # return render(request, "encyclopedia/newpage.html")
    if request.method == "POST":
        # get the title
        title = request.POST['title']
        # get the text
        markdown = request.POST['markdown']

        name_list = util.list_entries()

        if title in name_list:
            # When the page is saved, if an encyclopedia entry already  exists with the provided title, the user should be presented with an error message.
            return render(request, "encyclopedia/errormessage.html", {
                "title": title
            })
            # Save the new entry
        util.save_entry(title, markdown)

        return render(request, "encyclopedia/content.html", {
            "title": title,
            "entry": markdown2.markdown(markdown)})

    return render(request, "encyclopedia/newpage.html")


def edit(request):
    # entry = util.get_entry(entry)
    if request.method == "POST":
        title_when_post = request.POST['title']
        # get the text
        markdown = request.POST['markdown']
        name_list = util.list_entries()
        new_list = []

        for item in name_list:
            if item != title_when_post:
                new_list.append(item)

        if title_when_post in new_list:
            # When the page is saved, if an encyclopedia entry already  exists with the provided title, the user should be presented with an error message.
            return render(request, "encyclopedia/errormessage.html", {
                "title": title_when_post
            })
        # Save the new entry
        util.save_entry(title_when_post, markdown)

        return render(request, "encyclopedia/content.html", {
            "title": title_when_post,
            "entry": markdown2.markdown(markdown)
        })

    title = request.GET.get('title')
    entry = util.get_entry(title)

    return render(request, "encyclopedia/editContent.html", {
        "title": title,
        "entry": entry
    })

def randomPage(request):
    random_title = util.list_entries()

    random_encyclopedia = random.choice(random_title)
    # content(request, random_encyclopedia)
    entry = util.get_entry(random_encyclopedia)
    if entry:
        entry = markdown2.markdown(entry)

    return render(request, "encyclopedia/random.html", {
        "title": random_encyclopedia,
        "entry": entry,
    })
