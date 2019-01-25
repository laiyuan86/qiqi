# Create your views here.
from django.shortcuts import render
from .func import execkuber
from .exserver import connect_server


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


#显示单个nodes的信息
def get_node_info_by_nodename(request):
    exkube = execkuber()
    path = request.path
    path_list = path.split('/')
    while '' in path_list:
        path_list.remove('')
    node_name = path_list[2]
    print(node_name)
    node_info_list = exkube.get_node_info_by_nodename(node_name)

    return render(request, 'k8s/node_detail_info.html', {'node_name': node_name, 'node_info_list': node_info_list})


#备份etcd集群数据
def backup_etcd_data(request):
    IP_LIST = ['172.24.132.185', '172.24.132.186', '172.24.132.187']
    PORT = 22
    USER = 'root'
    PASSWORD = 'sgdbyjc@2018'
    COMMAND = 'bash /opt/script/etcd/backup.sh'
    back_ex = connect_server()
    ex_result_list = []
    for IP in IP_LIST:
        ex_result_dic = {}
        res = back_ex.ex_command(IP, PORT, USER, PASSWORD, COMMAND)
        ex_result_dic[IP] = res
        ex_result_list.append(ex_result_dic)

    return render(request, 'k8s/backup_etcd.html', {'ex_result_list': ex_result_list})


#xuexi js
def return_js(request):
    return render(request, 'k8s/styjs.html')


if __name__ == '__main__':
    index()

