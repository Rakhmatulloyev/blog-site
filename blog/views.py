from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import ContactForm
from .models import Article, Contact
from .bot import send_message  # Assuming send_message is defined in bot.py

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            description = form.cleaned_data["description"]

            send_message(name, email, phone_number, description)

            # Save the form data to Contact model
            form.save()

            # Reset form after successful submission
            form = ContactForm()

            # Show success message and redirect to home page
            messages.success(request, 'Your message has been sent successfully.')
            return HttpResponseRedirect(reverse('home-view'))  # Adjust 'home-view' with your actual URL name
        else:
            # Show error message if form is invalid
            messages.error(request, 'Please correct the errors below.')
    else:
        # For GET request, create a new form instance
        form = ContactForm()

    # Render the form in the context
    context = {"form": form}
    return render(request, "theme-particle.html", context)

def home_view(request):
    # Retrieve all articles sorted by id descending
    articles = Article.objects.all().order_by("-id")
    context = {"articles": articles}
    return render(request, "theme-particle.html", context)
