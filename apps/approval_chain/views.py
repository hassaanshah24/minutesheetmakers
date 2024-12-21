from django.shortcuts import render, redirect
from .models import ApprovalChain, ApprovalStep
from .forms import ApprovalChainForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages


User = get_user_model()



@login_required
def create_approval_chain(request):
    approvers = User.objects.all()  # Fetch all approvers for dropdown
    if request.method == "POST":
        form = ApprovalChainForm(request.POST)
        if form.is_valid():
            approval_chain = form.save(commit=False)
            approval_chain.created_by = request.user
            approval_chain.save()

            approvers_list = request.POST.getlist("approvers[]")
            for index, approver_id in enumerate(approvers_list, start=1):
                approver = User.objects.get(id=approver_id)
                ApprovalStep.objects.create(
                    chain=approval_chain,
                    approver=approver,
                    step_order=index,
                )
            messages.success(request, "Approval chain created successfully!")
            return redirect("submit_minutes")  # Adjusted for URL name 'submit_minutes'
        else:
            messages.error(request, "Error creating approval chain. Please try again.")
    else:
        form = ApprovalChainForm()
    return render(request, "approval_chain/create_chain.html", {"form": form, "approvers": approvers})


@login_required
def list_approval_chains(request):
    chains = ApprovalChain.objects.prefetch_related("approval_steps").all()
    return render(request, "approval_chain/list_chains.html", {"chains": chains})
