from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render


PRODUCTS = {
    "galaxy-s25-ultra": {
        "name": "Galaxy S25 Ultra", "category": "Phones", "price": "₹129,999",
        "tagline": "Galaxy AI. Built for the extraordinary.",
        "description": "A premium titanium-framed flagship with an advanced camera, the brilliant Dynamic AMOLED display, and powerful Galaxy AI experiences.",
        "accent": "#4b67c3", "icon": "S",
    },
    "galaxy-z-fold7": {
        "name": "Galaxy Z Fold7", "category": "Phones", "price": "₹174,999",
        "tagline": "Thin. Powerful. Transformative.",
        "description": "Unfold a cinematic screen and a laptop-like workspace in a remarkably slim foldable design made for multitasking.",
        "accent": "#b4a0db", "icon": "Z",
    },
    "galaxy-watch8": {
        "name": "Galaxy Watch8", "category": "Wearables", "price": "₹29,999",
        "tagline": "Know your health. Own your day.",
        "description": "Stay connected and informed with an elegant smartwatch, advanced wellness insights, fitness tracking, and all-day battery life.",
        "accent": "#83a5ba", "icon": "W",
    },
    "neo-qled-8k": {
        "name": "Neo QLED 8K", "category": "TV & AV", "price": "₹249,999",
        "tagline": "Every detail, elevated.",
        "description": "Quantum Mini LEDs deliver intense contrast and detail in an immersive 8K display with intelligent upscaling.",
        "accent": "#4d6e98", "icon": "8K",
    },
    "galaxy-book4": {
        "name": "Galaxy Book4", "category": "PC & Tablets", "price": "₹89,990",
        "tagline": "Power meets portability.",
        "description": "A refined Windows laptop built for smooth productivity, vivid visuals, and seamless connection to the Galaxy ecosystem.",
        "accent": "#aeb9c8", "icon": "B",
    },
    "bespoke-washing-machine": {
        "name": "Bespoke AI Washer", "category": "Appliances", "price": "₹54,990",
        "tagline": "Smarter laundry, beautifully done.",
        "description": "Personalise your laundry experience with intelligent fabric care, efficient cleaning, and a refined Bespoke finish.",
        "accent": "#d6ccbc", "icon": "A",
    },
}


def home(request):
    featured = [dict(slug=slug, **product) for slug, product in list(PRODUCTS.items())[:3]]
    return render(request, "home.html", {"featured": featured})


def products(request):
    category = request.GET.get("category", "All")
    items = [dict(slug=slug, **product) for slug, product in PRODUCTS.items()]
    if category != "All":
        items = [item for item in items if item["category"] == category]
    categories = ["All"] + sorted({product["category"] for product in PRODUCTS.values()})
    return render(request, "products.html", {"items": items, "categories": categories, "current_category": category})


def product_detail(request, slug):
    product = PRODUCTS.get(slug)
    if not product:
        return redirect("products")
    return render(request, "product_detail.html", {"product": product, "slug": slug})


def about(request):
    return render(request, "about.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            messages.error(request, "Please enter both your username and password.")
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect("home")
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")
        if not all([name, username, email, password, confirm]):
            messages.error(request, "Please complete every field.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "That email is already registered.")
        else:
            try:
                validate_password(password)
                user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
                login(request, user)
                messages.success(request, "Your account was created successfully.")
                return redirect("home")
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("home")