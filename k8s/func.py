#kubernetes 功能函数
from kubernetes import client, config


class execkuber(object):

    def __init__(self):
        config.load_kube_config()

    #获取所有namespace
    def get_all_namespaces(self):
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace().items
        namespaces_list = []
        for ns in namespaces:
            namespace = ns.metadata.name
            namespaces_list.append(namespace)
        print(namespaces_list)
        return namespaces_list

    #获取所有的pod
    def get_all_pods(self):
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces().items
        print(len(pods))

    #获取相关namespace下的pods
    def get_pods_by_namespace(self, ns):
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(ns).items
        pods_info_list = []
        pods_info_dic = {}
        for pod in pods:
            pod_info_dic = {}
            pod_name = pod.metadata.name
            pod_image = pod.spec.containers[0].image
            host_ip = pod.status.host_ip
            pod_ip = pod.status.pod_ip
            phase = pod.status.phase
            pod_info_dic["pod_name"] = pod_name
            pod_info_dic["pod_image"] = pod_image
            pod_info_dic["host_ip"] = host_ip
            pod_info_dic["pod_ip"] = pod_ip
            pod_info_dic["phase"] = phase
            pods_info_list.append(pod_info_dic)
        pods_info_dic[ns] = pods_info_list
        return pods_info_dic

    #获取node相关信息
    def get_nodes_info(self):
        v1 = client.CoreV1Api()
        res = v1.list_node().items
        nodes_info_dic = {}
        for i in res:
            node_info_dic = {}
            node_name = i.metadata.name
            node_info_dic["node_name"] = node_name
            ex_ip = i.spec.external_id
            node_info_dic["ex_ip"] = ex_ip
            allocatable_cpu_nums = i.status.allocatable['cpu']
            node_info_dic["allocatable_cpu_nums"] = allocatable_cpu_nums
            allocatable_memory = i.status.allocatable['memory']
            node_info_dic["allocatable_memory"] = allocatable_memory
            capacity_cpu_nums = i.status.capacity['cpu']
            node_info_dic["capacity_cpu_nums"] = capacity_cpu_nums
            capacity_memory = i.status.capacity['memory']
            node_info_dic["capacity_memory"] = capacity_memory
            images_list = i.status.images
            node_info_dic["images_list_num"] = len(images_list)
            architecture = i.status.node_info.architecture
            node_info_dic["architecture"] = architecture
            node_kernel_version = i.status.node_info.kernel_version
            node_info_dic["node_kernel_version"] = node_kernel_version
            systemtype = i.status.node_info.os_image
            node_info_dic["systemtype"] = systemtype
            docker_version = i.status.node_info.container_runtime_version
            node_info_dic["docker_version"] = docker_version
            kubernetes_version = i.status.node_info.kubelet_version
            node_info_dic["kubernetes_version"] = kubernetes_version
            nodes_info_dic[node_name] = node_info_dic


        node_num = 0
        for k, v in nodes_info_dic.items():
            node_num += 1
            print(k, v)
        print(node_num)

    #获取node状态
    def get_node_status(self, node_name):
        v1 = client.CoreV1Api()
        res = v1.read_node(node_name)
        print(res)


if __name__ == '__main__':
    exkube = execkuber()
    ns = "acc-pay"
    node_name = "172.24.132.187"
    exkube.get_node_status(node_name)