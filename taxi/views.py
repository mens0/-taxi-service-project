from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverCreationForm, LicenseUpdateForm, DriverSearchForm, \
    CarCreateForm, CarSearchForm, ManufacturerSearchForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)

        manufacturer = self.request.GET.get("manufacturer", "")

        context["search_form"] = ManufacturerSearchForm(initial={
            "manufacturer": manufacturer
        })

        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            return super().get_queryset().filter(
                name__icontains=form.cleaned_data["manufacturer"]
            )

        return super().get_queryset()


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 2
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)

        model = self.request.GET.get("model", "")

        context["search_form"] = CarSearchForm(initial={
            "model": model
        })

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return super().get_queryset().filter(
                model__icontains=form.cleaned_data["model"]
            )

        return super().get_queryset()


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = DriverSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = DriverSearchForm(self.request.GET)
        if form.is_valid():
            return super().get_queryset().filter(
                username__icontains=form.cleaned_data["username"],
            )

        return super().get_queryset()


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")



class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreateForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    fields = "__all__"
    template_name = "taxi/car_delete_form.html"
    success_url = reverse_lazy("taxi:car-list")


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_delete_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = "taxi/driver_delete_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class LicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = LicenseUpdateForm
    template_name = "taxi/license_update.html"
    success_url = reverse_lazy("taxi:driver-list")


def add_to_driver(request, pk, action):
    driver = Driver.objects.get(id=request.user.id)
    if action == "delete":
        driver.cars.remove(pk)
    elif action == "assign":
        driver.cars.add(pk)

    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
