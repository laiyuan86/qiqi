# Create your views here.
from django.shortcuts import render
from .func import execkuber


def index(request):
    exkube = execkuber()
    namespaces_list = exkube.get_all_namespaces()
    cluster_info_list = exkube.get_nodes_info()
    nodes_info_dic = cluster_info_list[0]
    cpu_nums = cluster_info_list[1]
    memorys = cluster_info_list[2]
    return render(request, 'k8s/index.html', {'namespaces_list': namespaces_list, 'nodes_info_dic': nodes_info_dic,\
                                              'cpu_nums': cpu_nums, 'memorys': memorys})


#获取命名空间中的pod信息
def get_pods_by_ns(request):
    exkube = execkuber()
    namespaces_list = exkube.get_all_namespaces()
    path = request.path
    path_list = path.split('/')
    while '' in path_list:
        path_list.remove('')
    ns = path_list[2]
    pods_info_dic = exkube.get_pods_by_namespace(ns)
    for k, v in pods_info_dic.items():
        pods_info_list = v
        title_ns = k
    svcs_info_list = exkube.get_svc_by_ns(ns)
    return render(request, 'k8s/ns_detail_info.html', {'namespaces_list': namespaces_list, 'pods_info_list': pods_info_list,\
                                              'title_ns': title_ns, 'svcs_info_list': svcs_info_list})


if __name__ == '__main__':
    index()

