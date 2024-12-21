from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from .models import Minute, ApprovalStep
from .forms import MinuteForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.users.models import CustomUser
from django.contrib.auth import get_user_model
from approval_chain.models import ApprovalChain

User = get_user_model()

# Dynamically fetch the custom user model
User = get_user_model()


@login_required
def submit_minutes(request):
    if request.method == "POST":
        form = MinuteForm(request.POST, request.FILES)
        if form.is_valid():
            minute = form.save(commit=False)
            minute.created_by = request.user
            minute.save()

            # Use the selected approval chain to create ApprovalSteps
            approval_chain = form.cleaned_data.get("approval_chain")
            if approval_chain:
                for step in approval_chain.approval_steps.all():
                    ApprovalStep.objects.create(
                        minute=minute,
                        approver=step.approver,
                        step_order=step.step_order,
                        status="pending" if step.step_order == 1 else "pending",
                    )

            messages.success(request, "Minute submitted successfully!")
            return redirect("track-minutes")
    else:
        form = MinuteForm()

    return render(request, "minutes/submit_minutes.html", {"form": form, "title": "Submit New Minute"})


@login_required
def track_minutes(request):
    """
    Displays the list of minutes created by the logged-in user.
    """
    minutes = Minute.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'minutes/track_minutes.html', {
        'minutes': minutes,
        'title': 'Track Submitted Minutes'
    })


@login_required
def pending_minutes(request):
    """
    Displays minutes pending approval for the logged-in user.
    """
    if request.user.is_superuser:
        minutes = Minute.objects.filter(is_approved=False)
    else:
        minutes = Minute.objects.filter(
            approval_steps__approver=request.user,
            approval_steps__status='pending'
        ).distinct()
    return render(request, 'minutes/pending_minutes.html', {
        'minutes': minutes,
        'title': 'Pending Approvals'
    })


@login_required
def approve_minute(request, minute_id):
    """
    Handles the approval, rejection, marking, or returning of a minute.
    """
    minute = get_object_or_404(Minute, id=minute_id)
    current_step = minute.approval_steps.filter(step_order=minute.current_step).first()

    # Check if the user is authorized
    if not current_step or current_step.approver != request.user:
        messages.error(request, "You are not authorized to review this minute.")
        return redirect('pending-minutes')

    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')

        if action == 'approve':
            current_step.status = 'approved'
            current_step.approved_at = now()
            current_step.save()

            # Move to the next step or mark the minute as approved
            next_step = minute.approval_steps.filter(step_order=current_step.step_order + 1).first()
            if next_step:
                next_step.status = 'pending'
                next_step.save()
                minute.current_step += 1
            else:
                minute.is_approved = True
            minute.comments = comments
            minute.save()
            messages.success(request, "Minute approved successfully.")

        elif action == 'reject':
            current_step.status = 'rejected'
            current_step.approved_at = now()
            current_step.save()
            minute.is_approved = False
            minute.comments = comments
            minute.save()

            # Notify all members in the chain
            # Placeholder for notification logic
            messages.error(request, "Minute has been rejected and archived.")

        elif action == 'mark_to':
            new_approver_id = request.POST.get('mark_to_user')
            new_approver = User.objects.filter(id=new_approver_id).first()

            if new_approver:
                next_order = current_step.step_order + 1
                ApprovalStep.objects.create(
                    minute=minute,
                    approver=new_approver,
                    step_order=next_order,
                    status='pending'
                )

                # Reorder steps
                steps = minute.approval_steps.order_by('step_order')
                for idx, step in enumerate(steps, start=1):
                    step.step_order = idx
                    step.save()

                messages.success(request, f"Minute marked to {new_approver.get_full_name()}.")
            else:
                messages.error(request, "Invalid approver selected.")

        elif action == 'return_to':
            return_to_step = int(request.POST.get('return_to_step'))
            previous_step = minute.approval_steps.filter(step_order=return_to_step).first()

            if previous_step:
                previous_step.status = 'pending'
                previous_step.approved_at = None
                previous_step.save()

                # Reset later steps
                later_steps = minute.approval_steps.filter(step_order__gt=return_to_step)
                later_steps.update(status='pending', approved_at=None)

                minute.current_step = return_to_step
                minute.is_approved = False
                minute.comments = comments
                minute.save()
                messages.success(request, "Minute returned to a previous approver.")
            else:
                messages.error(request, "Invalid return-to step selected.")

        return redirect('pending-minutes')

    approvers = User.objects.all()  # Ensure all users are shown
    return render(request, 'minutes/review.html', {
        'minute': minute,
        'current_step': current_step,
        'all_steps': minute.approval_steps.all(),
        'approvers': approvers,
    })



def search_users(request):
    """
    API endpoint to fetch approvers dynamically.
    """
    query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')

    try:
        users = User.objects.filter(is_active=True)
        if query:
            users = users.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        if role_filter:
            users = users.filter(role=role_filter)  # Adjust 'role' field as per your User model

        results = [
            {'id': user.id, 'text': f"{user.first_name} {user.last_name} ({user.username})"}
            for user in users
        ]
        return JsonResponse({'results': results})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)