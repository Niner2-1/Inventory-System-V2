from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Item, Branch, Custody, Transaction
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("adminDashboard")
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(request, "You need to be logged in to perform this action")

    return redirect(reverse("loginView"))


@login_required
def dashboard(request):
    context = {
        "page_title": "Dashboard",
    }
    return render(request, "admin/home.html", context)

def transaction(request):
    transactions = Transaction.objects.all()
    branches = Branch.objects.all()
    branches_data = [{'id': branch.id, 'name': branch.name.title()} for branch in branches]

    context = {
        "page_title": "Transaction",
        "transactions": transactions,
        "branches": branches_data,
    }

    if request.method == "POST":
        try:
            FFE_number = request.POST.get("FFE_number", "").lower()
            status = request.POST.get("status", "").lower()
            date = request.POST.get("date", "").lower()
            custody = request.POST.get("custody", "").lower()
            current_branch = request.POST.get("current_branch", "").lower()
            remarks = request.POST.get("remarks", "").lower()

            try:
                item = Item.objects.get(FFE_number=FFE_number)
            except Item.DoesNotExist:
                messages.error(request, "Item not found.")
                return redirect("adminViewTransactions")

            remarks_message = remarks if remarks else "n/a"
            branch = Branch.objects.get(id=current_branch)
            instance_custody, _ = Custody.objects.get_or_create(title=custody)

            transaction = Transaction.objects.create(
                item=item,
                date=date,
                status=status,
                remark=remarks_message,
                current_branch=branch,
                custody=instance_custody,
            )

            # Update item details
            item.status = status
            item.current_branch = branch
            item.custody = instance_custody
            item.save()

            messages.success(request, "Transaction added successfully")
            return redirect("adminViewTransactions")

        except IntegrityError as e:
            messages.error(request, "Transaction creation failed. Please check the details and try again.")
            return redirect("adminViewTransactions")
        except:
            messages.error(request, "Form validation failed")
            return redirect("adminViewTransactions")

    return render(request, "admin/transaction.html", context)





@login_required
def items(request):
    items = Item.objects.all()
    branches = Branch.objects.all()
    branches_data = [{'id': branch.id, 'name': branch.name.title()} for branch in branches]
    
    context = {
        "items": items,
        "branches": branches_data,
        "page_title": "Items List",
    }
    if request.method == "POST":
        try:
            FFE_number = request.POST.get("FFE_number", "").lower()
            old_FFE = request.POST.get("old_FFE", "").lower()
            item_type = request.POST.get("item_type", "").lower()
            processor = request.POST.get("processor", "").lower()
            motherboard = request.POST.get("motherboard", "").lower()
            memory = request.POST.get("memory", "").lower()
            video_card = request.POST.get("video_card", "").lower()
            hard_disk = request.POST.get("hard_disk", "").lower()
            others = request.POST.get("others", "").lower()
            description = request.POST.get("description", "").lower()
            cost = request.POST.get("cost", "").lower()
            date = request.POST.get("date", "").lower()
            branch = request.POST.get("originating_branch", "")
            custody = request.POST.get("custody", "").lower()
            status = request.POST.get("status", "").lower()


            instance_custody, _ = Custody.objects.get_or_create(title=custody)
            instance_branch = Branch.objects.get(id=branch)

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
            messages.success(request, "New item created")
            return redirect("adminViewItems")
        
        except IntegrityError as e:
            if "UNIQUE constraint failed: core_item.old_FFE" in str(e):
                messages.error(request, "An item with this 'Old FFE' already exists. Please check and try again.")
            elif "UNIQUE constraint failed: core_item.FFE_number" in str(e):
                messages.error(request, "An item with this 'FFE Number' already exists. Please check and try again.")
            return redirect("adminViewItems")
        except:
            messages.error(request, "Form validation failed")
            return redirect("adminViewItems")

    return render(request, "admin/items.html", context)


"""
ADD A EDIT FUNCTION AFTER THE BRANCH

"""


def view_item_by_id(request):
    item_id = request.GET.get("id", None)
    item = Item.objects.filter(FFE_number=item_id)
    context = {}
    if not item.exists():
        context["code"] = 404
    else:
        context["code"] = 200
        item = item[0]
        context["FFE_number"] = item.FFE_number
        context["old_FFE"] = item.old_FFE
        context["item_type"] = item.item_type
        context["processor"] = item.processor
        context["motherboard"] = item.motherboard
        context["memory"] = item.memory
        context["hard_disk"] = item.hard_disk
        context["others"] = item.others
        context["cost"] = item.cost
        context["video_card"] = item.video_card
        context["date_purchased"] = item.date_purchased
        context["description"] = item.description
        context["originating_branch"] = item.originating_branch.id
        context["current_branch"] = item.current_branch.id
        context["status"] = item.status
        context["custody"] = item.custody.title

    return JsonResponse(context)


def updateItem(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
        return redirect("adminViewItems")
    try:
        item_id = request.POST.get("id", None)
        instance = Item.objects.get(FFE_number=item_id)

        instance.FFE_number = request.POST.get("FFE_number", "").lower()
        instance.old_FFE = None
        instance.item_type = request.POST.get("item_type", "").lower()
        instance.processor = request.POST.get("processor", "").lower()
        instance.motherboard = request.POST.get("motherboard", "").lower()
        instance.memory = request.POST.get("memory", "").lower()
        instance.video_card = request.POST.get("video_card", "").lower()
        instance.hard_disk = request.POST.get("hard_disk", "").lower()
        instance.others = request.POST.get("others", "").lower()
        instance.description = request.POST.get("description", "").lower()
        instance.cost = request.POST.get("cost", "").lower()
        instance.date_purchased = request.POST.get("date", "").lower()

        branch_id = request.POST.get("originating_branch", None)
        instance_branch = Branch.objects.get(id=branch_id)
        instance.originating_branch = instance_branch
        instance.current_branch = instance_branch

        custody_title = request.POST.get("custody").lower()
        instance_custody, _ = Custody.objects.get_or_create(title=custody_title)
        instance.custody = instance_custody

        instance.status = request.POST.get("status", "").lower()
        instance.save()

        instance.old_FFE = request.POST.get("old_FFE", "").lower()
        instance.save()

        messages.success(request, "Item updated successfully")
    except Exception as e:
        print(e)
        messages.error(request, "Invalid request for update")

    return redirect(reverse("adminViewItems"))


def deleteItem(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        item = Item.objects.get(FFE_number=request.POST.get("id"))
        messages.success(request, f'Item Has Been Deleted {item.FFE_number}')
        item.delete()
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse("adminViewItems"))


"""
Branch View
"""

@login_required
def branch(request):
    branches = Branch.objects.all()
    branches_data = [{'id': branch.id, 'name': branch.name.title()} for branch in branches]
    
    context = {
        "branches": branches_data,
        "page_title": "Branch List",
    }

    if request.method == "POST":
        try:
            branch_name = request.POST.get("branch_name")
            Branch.objects.create(
                name=branch_name.lower(),
            )
            messages.success(request, "New branch created")
            print("success")
            return redirect("adminViewBranch")
        except:
            messages.error(request, "Form validation failed")
            return redirect("adminViewBranch")

    return render(request, "admin/branch.html", context)


def view_branch_by_id(request):
    branch_id = request.GET.get("id", None)
    branch = Branch.objects.filter(id=branch_id)
    context = {}
    if not branch.exists():
        context["code"] = 404
    else:
        context["code"] = 200
        branch = branch[0]
        context["branch_name"] = branch.name.title()
        context["id"] = branch.id
    return JsonResponse(context)


def updateBranch(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
        return redirect("adminViewBranch")
    try:
        branch_id = request.POST.get("id")
        instance = Branch.objects.get(id=branch_id.lower())
        instance.name = request.POST.get("branch_name")
        instance.save()
        messages.success(request, "Branch updated successfully")
    except:
        messages.error(request, "Invalid request for update")

    return redirect(reverse("adminViewBranch"))


def deleteBranch(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        branch = Branch.objects.get(id=request.POST.get("id"))
        branch.delete()
        messages.success(request, "Branch Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse("adminViewBranch"))


def dashboard(request):
    items = Item.objects.all()
    branches = Branch.objects.all()  # Renamed variable to avoid conflict
    chart_data = {}

    context = {
        "Item_count": items.count(),
        "Branch_count": branches.count(),
        "Item": items,
        "Branch": branches,
        "chart_data": chart_data,
        "page_title": "Dashboard",
    }
    return render(request, "admin/home.html", context)



def get_item_details(request):
    ffe_number = request.GET.get('ffe_number', '').lower()
    try:
        item = Item.objects.get(FFE_number=ffe_number)
        item_details = {
            'status': item.status,
            'description': item.description,
            'remarks': item.remarks,
            'current_branch': item.current_branch.name if item.current_branch else 'N/A',
            'custody': item.custody.title if item.custody else 'N/A',
        }
        return JsonResponse({'item_details': item_details})
    except Item.DoesNotExist:
        return JsonResponse({'item_details': None})