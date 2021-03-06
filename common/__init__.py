from time import timezone

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

# 注册自己为一个自定义的Tag
from django import template

register_lib = template.Library()


@register.filter
def join_queryset_attr(queryset, attr, delimiter=', '):
    """
    把结果集的属性用分隔符进行连接
    :param queryset: 结果集
    :param attr: 属性名
    :param delimiter: 分隔符
    :return: 
    """
    return delimiter.join([getattr(obj, attr, '') for obj in queryset])


@register.filter()
def str_to_int(value):
    """
    转换value为数值类型
    :param value: 
    :return: 
    """
    if value is not None and value != "":
        return int(value)
    else:
        return value


@register.filter
def pagination_range(total_page, current_num=1, display=5):
    """返回分页基础信息

    :param total_page: Total numbers of paginator
    :param current_num: current display page num
    :param display: Display as many as [:display:] page

    In order to display many page num on web like:
    < 1 2 3 4 5 >
    """
    try:
        current_num = int(current_num)
    except ValueError:
        current_num = 1

    start = current_num - display / 2 if current_num > display / 2 else 1
    end = start + display if start + display <= total_page else total_page + 1
    start = int(start)
    end = int(end)
    if(start == 0):
        start += 1
        end += 1
    return range(int(start), int(end))


@register.filter()
def file_path_filter(value):
    if type(value) is str:
        return ''
    else:
        return value.name.split('/')[-1].split('.')[0]


@register.filter()
def bool_to_human(value):
    """
    转换布尔类型为中文
    :param value: 
    :return: 
    """
    if value is True:
        return '是'
    else:
        return '否'


@register.filter()
def replace_to_br(value, str):
    """
    将换行符转为html到换行符
    :param value: 
    :return: 
    """
    if value is not None:
        return mark_safe(value.replace('\\n', '<br/>'))
    else:
        return ''


@register.filter()
def replace_to_nr(value):
    """
    将换行符转为html到换行符
    :param value:
    :return:
    """
    if value is not None:
        return mark_safe(value.replace('\n', '\\n').replace('\r', '\\r'))
    else:
        return ''


@register.filter
def join_attr(seq, attr=None, sep=None):
    """
    将属性用分割符连接
    :param seq: 
    :param attr: 
    :param sep: 
    :return: 
    """
    if sep is None:
        sep = ', '
    if attr is not None:
        seq = [getattr(obj, attr) for obj in seq]
    return sep.join(seq)


@register.filter
def int_to_str(value):
    """
    转换数值为字符串
    :param value: 
    :return: 
    """
    return str(value)


@register.filter
def ts_to_date(ts):
    """
    时间戳转日期
    :param ts: 
    :return: 
    """
    try:
        ts = float(ts)
    except TypeError:
        ts = 0
    dt = timezone.datetime.fromtimestamp(ts). \
        replace(tzinfo=timezone.get_current_timezone())
    return dt.strftime('%Y-%m-%d %H:%M:%S')


@register.filter(name='split')
def split(value, arg):
    if value:
        return value.split(arg)
    else:
        return []

@register.filter(name='getListFirst')
def getListFirst(value, arg):
    if value:
        if len(value)-1 >= arg:
            return value[arg]
        else:
            return ""
    else:
        return ""

@register.filter(name='getListLast')
def getListLast(value):
    if value:
        return value[len(value)-1]
    else:
        return ""


@register.filter(name='emptyValueConversion')
def emptyValueConversion(value,arg="0"):
    if value:
        return value;
    else:
        return arg;

@register.filter(name='devopsToolsTypeTrans')
def devopsToolsTypeTrans(value):
    tools_type_dict = {1:'常用命令',2:'上传文件',3:'远程文件',4:'shell脚本',5:'自定义'}
    if value:
        return tools_type_dict[value]
    else:
        return ""

@register.filter(name='getPercent')
def getPercent(value, total):
    if value and total:
        return '%.2f%s' % (value / total * 100,'%')
    else:
        return '0'


@register.filter(name='hostOperationLogTypeTrans')
def hostOperationLogTypeTrans(value):
    if value:
        # 1:新增host  2:绑定树节点   3:解绑树节点  4:未分配  5:待上线  6:已上线  7:删除
        type_dict = {"1":"新增主机","2":"绑定主机组","3":"解绑主机组","4":"未分配","5":"待上线","6":"已上线","7":"删除"}
        return type_dict[str(value)]
    else:
        return ""