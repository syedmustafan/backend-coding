from django.shortcuts import render
from django.http import HttpResponse
from fuzzywuzzy import fuzz
from django.views import generic


class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        with open('./data/Dummy-medical-dataset.csv') as f:
            medicine_key = [medicine_name.rstrip("\n").split(",")[0] for medicine_name in f]

        return render(request, 'matching_key_value/select.html', context={"medicine_key": medicine_key[1:]})


class ListTable(generic.CreateView):
    def post(self, request, *args, **kwargs):
        medicine_dict = {}
        options = []
        if request.method == 'POST':
            key = request.POST.get('key')
            with open('./data/Dummy-medical-dataset.csv') as f:
                for medicine in f:
                    medicine_name = medicine.rstrip("\n").split(",")
                    medicine_dict[medicine_name[0]] = medicine_name[1]

            medicine_value = medicine_dict.get(key, "") if key in medicine_dict else ""
            for values in medicine_dict.values():
                ratio = fuzz.ratio(values, medicine_value)
                if ratio > 50 and ratio != 100:
                    options.append((values, ratio))
            options.sort(key=lambda i: i[1], reverse=True)
            resultant_dict = {"key": key, "record": options}
            return render(request, 'matching_key_value/table.html', context=resultant_dict)
        else:
            return HttpResponse("Method not allowed")
