from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect

from . import util
import markdown2
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def results(request,title):

    content=util.get_entry(title)
    #if entry doesn't exist send an error message
    if content == None:
        message = "The page \"" + title.upper() + "\" does not exist."
        return render(request, "encyclopedia/error.html", {
            "message": message
        })
    #Convert entry in markdown
    content=markdown2.markdown(content)
    return render(request, "encyclopedia/results.html",{
            "title": title,
            "content": content,
        })

def newpage(request):
    if request.method=="POST": 
        title=request.POST["title"]
        content=request.POST["content"]        
        editPage=request.POST.get("editPage")
        message={
              "message":"Title or content cannot be emty",
              "editPage":editPage
        }

            #Check title and content  are provided
        if title=="" or content=="":
            return render (request,"encyclopedia/error.html",{
                    "message":message
                })
        if editPage == "True":
            util.save_entry(title,content)
            content=util.get_entry(title)
            return HttpResponseRedirect( "wiki/"+title) 
        #if title exists,display error message
        else:
            entries=util.list_entries()
            if title.lower() in (entry.lower() for entry in entries):
                return render(request,"encyclopedia/error.html",{                        "message":"This entry exists"
                            })
                    #save content and title in entries
            content="#"+" "+title+"\n"+"\n"+content
            util.save_entry(title,content)
            content=util.get_entry(title)
            return HttpResponseRedirect( "wiki/"+title)        
    else:
        return render(request,"encyclopedia/newpage.html")

def edit(request):
    #Render html page where  user can edit the content
    title=request.POST["title"]
    editPage=request.POST.get("editPage")
    content=util.get_entry(title)
    
    return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content,
            })
    
def error(request):
    return render(request,"encyclopedia/error.html")

def random(request):
    #Get random entry
    entries=util.list_entries()
    title=choice(entries)
    return HttpResponseRedirect("wiki/"+title)

def search(request):
    query=request.GET["q"]
    entries=util.list_entries()
    results=[]
    if query.lower() in (entry.lower() for entry in entries):
        return HttpResponseRedirect ("wiki/"+query)
    
    for title in entries:
        if query.lower() in title.lower() :
            results.append(title)
        
    return render(request,"encyclopedia/search.html",{
            "results":results,
        })
