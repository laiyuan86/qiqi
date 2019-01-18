#kubernetes 功能函数
from kubernetes import client, config
import json


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
            kubeletstatus = i.status.conditions
            for i in kubeletstatus:
                if i.reason == "KubeletReady":
                    node_status = i.type
                    node_info_dic['node_status'] = node_status

        node_num = 0
        cpu_nums = 0
        memorys = 0
        for node_name, node_info in nodes_info_dic.items():
            node_num += 1
            for k, v in node_info.items():
                if k == "allocatable_cpu_nums":
                    cpu_nums += int(v)
                elif k == "allocatable_memory":
                    mem = int(v[:-2])
                    memorys += int(mem / (1024*1024))
        cluster_info_list = []
        cluster_info_list.append(nodes_info_dic)
        cluster_info_list.append(cpu_nums)
        cluster_info_list.append(memorys)
        return cluster_info_list

    #根据namespace获取service
    def get_svc_by_ns(self, ns):
        v1 = client.CoreV1Api()
        res = v1.list_namespaced_service(ns).items
        svcs_info_list = []
        for i in res:
            svc_info_dic = {}
            svc_name = i.metadata.name
            svc_info_dic['name'] = svc_name
            selector = i.spec.selector
            svc_info_dic['selector'] = selector
            cluster_ip = i.spec.cluster_ip
            svc_info_dic['cluster_ip'] = cluster_ip
            svc_type = i.spec.type
            svc_info_dic['svc_type'] = svc_type
            port = eval(str(i.spec.ports[0]))
            node_port = port.get('node_port')
            svc_info_dic['node_port'] = node_port
            svc_port = port.get('port')
            svc_info_dic['svc_port'] = svc_port
            target_port = port.get('target_port')
            svc_info_dic['target_port'] = target_port
            svcs_info_list.append(svc_info_dic)
            print(type(selector))
        return svcs_info_list




if __name__ == '__main__':
    exkube = execkuber()
    ns = "acc-pay"
    node_name = "172.24.132.187"
    exkube.get_svc_by_ns(ns)
