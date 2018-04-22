from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import lxml
from kmucafe.models import Menu


# Create your views here.

def keyboard(request):
    return JsonResponse(

        {
            'type': 'buttons',
            'buttons': ['학생식당', '교직원식당', '한울식당', '청향', '생활관식당(일반식)', '생활관식당(정기식)']
        }
    )


def get_menu(name):
    if name == '학생식당':
        f = Menu.objects.all()[0]
        s = str(f.cafe1)
        return s
    elif name == '교직원식당':
        f = Menu.objects.all()[0]
        s = str(f.cafe2)
        return s
    elif name == "한울식당":
        f = Menu.objects.all()[0]
        s = str(f.cafe3)
        return s
    elif name == "청향":
        f = Menu.objects.all()[0]
        s = str(f.cafe4)
        return s
    elif name == '생활관식당(일반식)':
        f = Menu.objects.all()[0]
        s = str(f.cafe5)
        return s
    elif name == '생활관식당(정기식)':
        f = Menu.objects.all()[0]
        s = str(f.cafe6)
        return s


def crawl(request):
    menu_db = Menu.objects.all()
    menu_db.delete()

    d = datetime.date.today()

    if d.weekday() == 6:
        Menu.objects.create(cafe1='월요일에 업데이트 됩니다.', cafe2='월요일에 업데이트 됩니다.', cafe3='월요일에 업데이트 됩니다.',
                            cafe4='월요일에 업데이트 됩니다.', cafe5='월요일에 업데이트 됩니다.', cafe6='월요일에 업데이트 됩니다.')

        return HttpResponse('Update')

    # 학생식당

    html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=2')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "lxml")

    m = soup.find_all(bgcolor="#eaffd9")

    price = []
    lunch = ""
    dinner = ""

    for i in range(9):
        try:
            price.append((m[i].text.lstrip('\n').split('\n\n')[2]))
        except:
            price.append("")

    breakfast = m[0].text.lstrip('\n').split('\n\n')[0] + " " + price[0] + '\n\n'

    for i in range(1, 6):
        lunch += m[i].text.lstrip('\n').split('\n\n')[0] + " " + price[i] + '\n\n'

    for i in range(6, 9):
        dinner += m[i].text.lstrip('\n').split('\n\n')[0] + " " + price[i] + '\n\n'

    cafe1 = "착한아침\n\n" + breakfast + "--------\n중식\n\n" + lunch + "--------\n석식\n\n" + dinner

    # elif name == '교직원식당':

    html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=3')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "lxml")

    m = soup.find_all(bgcolor="#eaffd9")

    price = []
    lunch = ""

    for i in range(4):
        try:
            price.append((m[i].text.lstrip('\n').split('\n\n')[2]))
        except:
            price.append("")

    for i in range(0, 2):
        lunch += m[i].text.lstrip('\n').split('\n\n')[0] + " " + price[i] + '\n\n'

    dinner = m[3].text.lstrip('\n').split('\n\n')[0] + " " + price[3] + '\n\n'

    cafe2 = "중식\n\n" + lunch + "--------\n석식\n\n" + dinner

    # elif name == "청향":

    html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=4')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "lxml")

    m = soup.find_all(bgcolor="#eaffd9")

    price = []
    lunch = ""

    for i in range(7):
        try:
            price.append((m[i].text.lstrip('\n').split('\n\n')[1]))
        except:
            price.append("")

    for i in range(7):
        lunch += m[i].text.lstrip('\n').split('\n\n')[0] + " " + price[i] + '\n\n'

    cafe4 = lunch

    # elif name == "한울식당":

    if d.weekday() == 5 or d.weekday() == 6:
        cafe3 = "주말은 쉽니다."
    else:
        html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=1')
        source = html.read()
        html.close()

        soup = BeautifulSoup(source, "lxml")

        cafe = soup.find_all("td", {"class": "mn_corn"})
        m = soup.find_all(bgcolor="#eaffd9")
        try:
            baro1 = m[0].text.split()
            baro1_1 = [baro1[0], baro1[1] + baro1[2][0:5], baro1[2][5:], baro1[3] + baro1[4]]
        except:
            baro1_1 = []

        result = ''
        try:
            result += cafe[0].text
            for i in range(len(baro1_1)): result += '\n\n' + baro1_1[i]
        except:
            result = ''

        result += '\n\n\n'
        for i in range(1, 4):
            result += cafe[i].text + '\n' + m[i].text

        replacing = m[4].text.replace("\r", " ")
        star_index = replacing.find('*석')
        result += cafe[4].text + '\n' + replacing[0:star_index] + '\n' + replacing[star_index:]

        replacing = m[5].text.replace("\r", " ")
        star_index = replacing.find('*석')
        result += cafe[5].text + '\n' + replacing[0:star_index] + '\n' + replacing[star_index:]

        result += cafe[6].text + '\n' + m[6].text

        cafe3 = result

    # elif name == '생활관식당(일반식)':

    html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=5')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "lxml")

    m = soup.find_all(bgcolor="#eaffd9")

    lunch = m[0].text.lstrip('\n').split('\n\n')[0] + '\n\n'

    cafe5 = lunch

    # elif name == '생활관식당(정기식)':

    html = urlopen('http://kmucoop.kookmin.ac.kr/restaurant/restaurant.php?w=6')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "lxml")

    m = soup.find_all(bgcolor="#eaffd9")

    price = []
    lunch = ""

    for i in range(3):
        try:
            price.append((m[i].text.lstrip('\n').split('\n\n')[2]))
        except:
            price.append("")

    for i in range(3):
        lunch += m[i].text.lstrip('\n').split('\n\n')[0] + " " + price[i] + '\n\n'

    cafe6 = lunch

    Menu.objects.create(cafe1=cafe1, cafe2=cafe2, cafe3=cafe3, cafe4=cafe4, cafe5=cafe5, cafe6=cafe6)

    return HttpResponse('Update')


@csrf_exempt
def answer(request):
    today = datetime.date.today().strftime("%m월 %d일")
    str = ((request.body).decode('utf-8'))
    received = json.loads(str)
    name = received['content']

    return JsonResponse(
        {
            'message': {
                'text': '매일 오전 5시, 10시에 업데이트됩니다.\n\n' + today + '의 ' + name + ' 메뉴입니다.\n\n' + get_menu(name)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학생식당', '교직원식당', '한울식당', '청향', '생활관식당(일반식)', '생활관식당(정기식)']
            }
        }
    )
