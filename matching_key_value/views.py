from django.shortcuts import render
from django.http import HttpResponse
from fuzzywuzzy import process
from django.views import generic


class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        with open('./data/Dummy-medical-dataset.csv') as f:
            medicine_key = [medicine_name.rstrip("\n").split(",")[0] for medicine_name in f]

        return render(request, 'matching_key_value/select.html', context={"medicine_key": medicine_key[1:]})


class ListTable(generic.CreateView):
    def post(self, request, *args, **kwargs):
        medicine_dict = {}
        exclusive_words = ["TABLET", "500MG", "300MG", "250MG"]
        if request.method == 'POST':
            key = request.POST.get('key')
            with open('./data/Dummy-medical-dataset.csv') as f:
                for medicine in f:
                    medicine_name = medicine.rstrip("\n").split(",")
                    medicine_dict[medicine_name[0]] = medicine_name[1]

            medicine_value = medicine_dict.get(key, "") if key in medicine_dict else ""
            value_list = medicine_value.split(" ") if medicine_value else []
            options = [values.replace('"', '') for values in medicine_dict.values() for val in value_list if
                       val in values and val not in exclusive_words]
            str2match = " ".join(value_list)
            matching_ratios = process.extract(str2match, set(options))
            resultant_dict = {"key": key, "record": matching_ratios}
            return render(request, 'matching_key_value/table.html', context=resultant_dict)
        else:
            return HttpResponse("Method not allowed")
