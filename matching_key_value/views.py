from django.shortcuts import render
from django.http import HttpResponse
from fuzzywuzzy import process


def index(request):
    """
    This view sends medicine key data to the html page

    :param request:
    :return: Html template
    """
    with open('./data/Dummy-medical-dataset.csv') as f:
        medicine_key = [medicine_name.rstrip("\n").split(",")[0] for medicine_name in f]

    return render(request, 'matching_key_value/select.html', context={"medicine_key": medicine_key[1:]})


def list_table(request):
    """
    This view return the similar values of medicine in a table. It uses fuzzywuzzy library to calculate the ratios.

    :param request:
    :return: Html template
    """
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
        print("values_list", value_list)
        options = [values.replace('"', '') for values in medicine_dict.values() for val in value_list if
                       val in values and val not in exclusive_words]
        str2match = " ".join(value_list)
        matching_ratios = process.extractBests(str2match, set(options), score_cutoff=50)
        resultant_dict = {"key": key, "record": matching_ratios}
        return render(request, 'matching_key_value/table.html', context=resultant_dict)
    else:
        return HttpResponse("Method not allowed")
