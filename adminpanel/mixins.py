from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Admin access only")
            return redirect('bookings:user-home')
        return super().dispatch(request, *args, **kwargs)
