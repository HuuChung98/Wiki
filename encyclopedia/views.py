import markdown2
from django import forms
from django.shortcuts import render

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, entry):

    entry = util.get_entry(entry)
    if entry:
        entry = markdown2.markdown(entry)
    else: 
        return render(request, "encyclopedia/notfound.html", {
            "error": entry
        })

    return render(request, "encyclopedia/content.html", {
        "entry": entry
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
    entryNew = ''
    if request.method == "POST":
        # get the title
        title = request.POST['title']
        # get the text 
        markdown = request.POST['markdown']
        print("Title" + title)
        print("Markdown content" + markdown)

        name_list = util.list_entries()

        if title in name_list:
        # When the page is saved, if an encyclopedia entry already  exists with the provided title, the user should be presented with an error message.
            return render(request, "encyclopedia/errormessage.html", {
                    "title": title
                })
                # Save the new entry
        util.save_entry(title, markdown)

        return render(request, "encyclopedia/content.html", {"entry": markdown2.markdown(markdown)})

    return render(request, "encyclopedia/newpage.html")
