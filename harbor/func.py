#操作harbor的各种消息

import configparser
import os

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(BASE_DIR, 'qiqi.conf'))
HOST = config.get('harbor', 'host')
USER = config.get('harbor', 'user')
PASSWORD = config.get('harbor', 'password')


class execharbor(object):
    #初始化
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    #获取项目名称
    def get_pm_name(self):
        CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/projects?' \
        |grep '\"name\"'|awk -F '\"' '{print $4}' > tt.txt" \
              % (self.user, self.password, self.host)
        os.system(CLI)
        with open('tt.txt', 'r') as f:
            res = f.read()
        pms_name = res.split("\n")
        pms_name.remove("")
        return pms_name

    #获取项目名和ID的对应关系
    def get_pm_name_id(self):
        pms_name = self.get_pm_name()
        pms_info_list = []
        for pm_name in pms_name:
            pm_info = {}
            CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/projects?' \
         |grep -w '%s' -C 2|grep 'project_id'|awk '{print $2}'| awk -F ',' '{print $1}' > project_id.txt" \
        % (self.user, self.password, self.host, pm_name)
            os.system(CLI)
            with open('project_id.txt', 'r') as f:
                id = f.read()
                id = id.replace('\n', '')
                pm_info[pm_name] = id
                pms_info_list.append(pm_info)
        return pms_info_list

    #获取每个项目中对应的镜像名称
    def get_pm_image_name(self):
        pms_info_list = self.get_pm_name_id()
        pms_info_dic = {}
        for pm_info in pms_info_list:
            for k, v in pm_info.items():
                CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/repositories?project_id=%d'\
         |grep '\"name\"' |awk -F '\"' '{print $4}' |sed 's/sc\///g' > image_name.txt "\
        % (self.user, self.password, self.host, int(v))
            os.system(CLI)
            with open('image_name.txt', 'r') as f:
                image_name = f.read()
                image_name_list = image_name.split("\n")
                image_name_list.remove("")
                if image_name_list == []:
                    image_name_list.append("该项目为空")
                    pms_info_dic[k] = image_name_list
                else:
                    pms_info_dic[k] = image_name_list
#        print(pms_info_dic)
        return pms_info_dic

    #获取每个镜像的tags
    def get_pm_image_tags(self):
        pms_info_dic = self.get_pm_image_name()
        for pm_name, pm_image_list in pms_info_dic.items():
            for pm_image in pm_image_list:
#                print(pm_image + "================")
                CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/repositories/%s/tags/' \
                |grep '\"name\"' |awk -F '\"' '{print $4}'|sort -n|uniq > pm_image_tags.txt"\
                % (self.user, self.password, self.host, pm_image)
                os.system(CLI)
                with open('pm_image_tags.txt', 'r') as f:
                    tags = f.read()
                    tags_list = tags.split("\n")
                    tags_list.remove("")
                    print(len(tags_list), tags_list)

    #查询单个项目名称对应的ID
    def get_pmid_by_pmname(self, pm_name):
        CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/projects?' \
                 |grep -w '%s' -C 2|grep 'project_id'|awk '{print $2}'| awk -F ',' '{print $1}' > project_id.txt" \
              % (self.user, self.password, self.host, pm_name)
        os.system(CLI)
        with open('project_id.txt', 'r') as f:
            id = f.read()
            id = id.replace('\n', '')

        return id

    #获取单个项目下所有的镜像
    def get_image_name(self, pm_id):
        CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/repositories?project_id=%d'\
                |grep '\"name\"' |awk -F '\"' '{print $4}' |sed 's/sc\///g' > image_name.txt " \
              % (self.user, self.password, self.host, int(pm_id))
        os.system(CLI)
        with open('image_name.txt', 'r') as f:
            image_name = f.read()
            image_name_list = image_name.split("\n")
            image_name_list.remove("")
            if image_name_list == []:
                image_name_list.append("该项目为空")
        return image_name_list

    #获取单个镜像的所有tags
    def get_image_tags(self, image_name):
        CLI = "curl -s -u '%s:%s' -X GET -H 'Content-Type: application/json' '%s/api/repositories/%s/tags/' \
                        |grep '\"name\"' |awk -F '\"' '{print $4}'|sort -n|uniq > image_tags.txt" \
              % (self.user, self.password, self.host, image_name)
        os.system(CLI)
        if image_name == None:
            return
        with open('image_tags.txt', 'r') as f:
            tags = f.read()
            tags_list = tags.split("\n")
            tags_list.remove("")
            tagsinfo_list = [tags_list, len(tags_list)]
        return tagsinfo_list

    #删除镜像
    def delete_image(self, image_name, tag):
        CLI = "curl -s -u '%s:%s' -X DELETE -H 'Content-Type: application/json' '%s/api/repositories/%s/tags/%s'"\
        % (self.user, self.password, self.host, image_name, tag)
        os.system(CLI)


if __name__ == '__main__':
    exharbor = execharbor(HOST, USER, PASSWORD)
#    exharbor.get_pm_image_name()
    exharbor.get_image_tags("zhaipi_test/bss-match-sys-service")
#    exharbor.delete_image("zhaipi_test/bss-match-sys-service", "test_20181119.1")

