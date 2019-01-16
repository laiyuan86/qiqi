from django.shortcuts import render
from harbor.func import execharbor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import configparser, os
config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(BASE_DIR, 'qiqi.conf'))
HOST = config.get('harbor', 'host')
USER = config.get('harbor', 'user')
PASSWORD = config.get('harbor', 'password')

# Create your views here.


def index(request):
    exharbor = execharbor(HOST, USER, PASSWORD)
    pms_info_dic = exharbor.get_pm_image_name()
    return render(request, 'harbor/index.html', {'pms_info_dic': pms_info_dic})


def about(request):
    return render(request, 'harbor/about.html')


def get_pm_detail(request):
    exharbor = execharbor(HOST, USER, PASSWORD)
    res = request.path
    if not res:
        return
    else:
        path_list = res.split('/')
    path_list.remove("")
    pm_name = path_list[2]
    pm_id = exharbor.get_pmid_by_pmname(pm_name)
    pm_image_list = exharbor.get_image_name(pm_id)
    pms_info_dic = exharbor.get_pm_image_name()
    tags_num_dic = {}
    Image_Name = "镜像名字"
    tag_number = "标签个数"
    for image_name in pm_image_list:
        tag_num = exharbor.get_image_tags(image_name)[1]
        tags_num_dic[image_name] = tag_num
    return render(request, 'harbor/index.html', {'tags_num_dic': tags_num_dic, 'pm_name': pm_name, \
                                                 'Image_Name': Image_Name, 'tag_number': tag_number, \
                  'pms_info_dic': pms_info_dic })


def get_image_tags(request):
    exharbor = execharbor(HOST, USER, PASSWORD)
    res = request.path
    if not res:
        return
    else:
        path_list = res.split('/')
    path_list.remove("")
    if len(path_list) == 4:
        image_name = path_list[2] + "/" + path_list[3]
    else:
        image_name = ['None']
#    print(image_name)
    tags_list = exharbor.get_image_tags(image_name)[0]
    return render(request, 'harbor/tags.html', {'tags_list': tags_list, 'image_name': image_name})


@csrf_exempt
def delete_image(request):
    exharbor = execharbor(HOST, USER, PASSWORD)
    res = request.POST.getlist('tags')
    if not res:
        print("没有选择")
    else:
        for image_tag in res:
            image_tag_list = image_tag.split(',')
            exharbor.delete_image(image_tag_list[0], image_tag_list[1])
    return render(request, 'harbor/about.html')
