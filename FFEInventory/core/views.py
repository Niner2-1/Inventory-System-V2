from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Item, Transaction, Branch, Custody
from django.contrib import messages
from django.db import IntegrityError


def dashboard(request):
    return render(request, "pages/dashboard.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "pages/login.html", {"error": "Invalid username or password"})
    else:
        return render(request, "pages/login.html")
    
def logout_view(request):
    logout(request)
    return redirect("login")


def item_view(request):
    items = Item.objects.all().order_by("-date_purchased")
    items_count = items.count()
    unique_item_types = items.values_list("item_type", flat=True).distinct()

    return render(
        request,
        "pages/items.html",
        {
            "count": items_count,
            "items": items,
            "unique_item_types": unique_item_types,
        },
    )
    
    
def add_Item(request):
    if request.method == "POST":
        FFE_number = request.POST.get("FFE_number")
        old_FFE = request.POST.get("old_FFE")
        item_type = request.POST.get("item_type")
        processor = request.POST.get("processor")
        motherboard = request.POST.get("motherboard")
        memory = request.POST.get("memory")
        video_card = request.POST.get("video_card")
        hard_disk = request.POST.get("hard_disk")
        others = request.POST.get("others")
        description = request.POST.get("description")
        cost = request.POST.get("cost")
        date = request.POST.get("date")
        branch = request.POST.get("branch")
        custody = request.POST.get("custody")
        status = request.POST.get("status")

        try:
            instance_custody, _ = Custody.objects.get_or_create(title=custody)
            instance_branch = Branch.objects.get(name=branch)

            Item.objects.create(
                FFE_number=FFE_number,
                old_FFE=old_FFE if old_FFE != "" else None,
                item_type=item_type,
                processor=processor,
                motherboard=motherboard,
                memory=memory,
                hard_disk=hard_disk,
                others=others,
                cost=cost,
                video_card=video_card,
                date_purchased=date,
                description=description,
                originating_branch=instance_branch,
                current_branch=instance_branch,
                status=status,
                custody=instance_custody,
            )
            messages.success(request, "Item added successfully.")
        except IntegrityError as e:
            messages.error(request, f"Item {FFE_number} already exist.\n {e}")

    branches = Branch.objects.all()
    context = {
        "branches": branches,
    }
    return render(request, "pages/item_form.html", context)