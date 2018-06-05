from django.forms.models import model_to_dict
import os,shutil,random,hashlib

def version_calc(calc_version, carry_bit=20):
    """
    :param calc_version: 计算版本号
    :param carry_bit: 多少进位
    :return:
    """
    results = ""
    if calc_version:
        l = calc_version.split('.')
        l.reverse()
        t = 0
        for i in range(len(l)):
            j = int(l[i])
            if i == 0:
                j += 1
            j += t
            t = 0
            if j >= carry_bit:
                j = 1
                t = 1
            results = str(j)+'.'+results
    return results[0:-1]


def path_is_exists(path):
    """
    判断路径是否存在
    :param path: 路径
    :return: 存在 - True  不存在 - False
    """
    if path:
        return os.path.exists(path)
    else:
        return False

def is_file(path):
    """
    是否是文件
    :param path: 路径
    :return: 是 - True
    """
    return os.path.isfile(path)

def is_dir(path):
    """
    是否是文件夹是
    :param path: 路径
    :return: 是 - True
    """
    return os.path.isdir(path)

def mkdir(path):
    """
    创建文件夹
    :param path: 路径
    :return: 创建成功 - True
    """
    if path:
        path = path.strip()
        path = path.rstrip("\\")
        if not path_is_exists(path):
            os.makedirs(path)
        return True
    else:
        return False

def cp(src,dst):
    """
    拷贝文件夹或文件
    :param src: 源
    :param dst: 目标
    :return:
    """
    if is_file(src):
        shutil.copy(src, dst)
    elif is_dir(src):
        shutil.copytree(src,dst)


def models_compare(dict,objct):
    """
    字典和model属性比较
    :param dict:
    :param objct:
    :return: True:一样  False:不一样
    """
    if dict and object:
       m_dict = model_to_dict(objct)
       for k in dict:
           m_value = m_dict.get(k,None)
           if m_value and dict[k] != m_value:
               return False
    return True

def remove_file(filename):
    if path_is_exists(filename):
        os.remove(filename)



def randomCharStr(population='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890',k=5):
    """
    随机产生字符串
    :param population: 自定义字符串
    :param k: 随机抽取个数 默认抽取5个
    :return:
    """
    return ''.join(random.sample(population, k))


def file_md5(filename):
    if filename and is_file(filename):
        f = None
        try:
            f = open(filename, 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            return str(hash_code).lower()
        except Exception as e:
            raise e
        finally:
            if f:
                f.close()
    return ""


def md5(s):
    if s:
        return hashlib.md5(s.encode('utf-8')).hexdigest()
    return ""
