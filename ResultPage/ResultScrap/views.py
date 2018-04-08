from __future__ import division
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.


def get_credit(length, marks, lab):
    if length == 6:
        marks = calculate_for_all(4, marks)
    else:
        if lab == "L":
            marks = calculate_for_all(2, marks)
        else:
            marks = calculate_for_all(3, marks)
    return marks


def calculate_for_all(mul, marks):
    if marks < 40:
        return mul*0
    elif marks < 45:
        return mul*4
    elif marks < 50:
        return mul*5
    elif marks < 60:
        return mul*6
    elif marks < 70:
        return mul*7
    elif marks < 80:
        return mul*8
    elif marks < 90:
        return mul*9
    else:
        return mul*10


def calculate_marks(list1):
    credit_list = []
    sub_index = 0
    marks_index = 4
    for i in range(8):
        sub_code = str(list1[sub_index])
        print(sub_code, int(list1[marks_index]))
        marks = get_credit(len(sub_code), int(list1[marks_index]), sub_code[4])
        credit_list.append(marks)
        sub_index = sub_index + 6
        marks_index = marks_index + 6
    return credit_list


def homepage(request):
    return render(request, "homepage.html",)


def result_page(request):
    data = request.POST.dict()
    usn = {"lns": data["input1"]}
    usn_send = data["input1"]
    result = requests.post(url="http://www.results.vtu.ac.in/vitaviresultcbcs/resultpage.php", data=usn)
    beautiful_result = BeautifulSoup(result.content, "html.parser")
    res = beautiful_result.find_all("div")
    name_res = beautiful_result.find_all("td")
    details = name_res[3].text
    list1 = []
    for val in res:
        if val.string:
            list1.append(val.string)
    sem = list1[0]
    del list1[0]
    length = len(list1)
    for i in range(5):
        del list1[length-i-1]
    column_head = []
    for i in range(6):
        column_head.append(list1[0])
        del list1[0]
    marks_list = calculate_marks(list1)
    marks_list.reverse()
    sum1 = 0
    for val in marks_list:
        sum1 = sum1 + int(val)
    print(sum1)
    aggregate = sum1 / 26
    print(aggregate)

    list1.reverse()
    column_head.append("Credits Earned")
    marks = []
    for i in range(8):
        m = {
            "code": list1.pop(),
            "name": list1.pop(),
            "marks1": list1.pop(),
            "marks2": list1.pop(),
            "total": list1.pop(),
            "result": list1.pop(),
            "credits": marks_list.pop(),
        }
        marks.append(m)
    return render(request, "result_page.html", {"aggregate": aggregate, "name": details, "sem": sem, "usn_student": usn_send, "lists": marks, "col": column_head})

