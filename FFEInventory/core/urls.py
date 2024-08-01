from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="adminDashboard"),
    # * Items
    path("items", views.items, name="adminViewItems"),
    path("items/view", views.view_item_by_id, name="viewItem"),
    path("items/update", views.updateItem, name="updateItem"),
    path("items/delete", views.deleteItem, name="deleteItem"),
    # * Items
    path("branch", views.branch, name="adminViewBranch"),
    path("branch/view", views.view_branch_by_id, name="viewBranch"),
    path("branch/update", views.updateBranch, name="updateBranch"),
    path("branch/delete", views.deleteBranch, name="deleteBranch"),
    # * Transactions
    path("transaction", views.transaction, name="adminViewTransactions"),
    path('get-item-details/', views.get_item_details, name='getItemDetails')

]
