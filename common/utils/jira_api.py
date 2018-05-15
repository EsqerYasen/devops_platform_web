#coding:utf-8

from jira.client import JIRA
from rest_framework import serializers

class jira_api():

    def __init__(self, server, user, pwd):
        """
        :param server: jira域名
        :param user:jira用户
        :param pwd:jira账户密码
        """
        self.server = server;
        self.basic_auth = (user, pwd)
        self.jiraClient = None

    def login(self):
        self.jiraClient = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.jiraClient is not None:
            return True
        else:
            return False


    def get_issue_list(self,jql_str=None,page=0,limit=10,fields=None):
        """
        查询issue集合
        :param jql_str: 查询语句
        :param page: 分页参数 开始
        :param limit: 分页参数 结束
        :param fields: 查询字段
        :return:issue: 列表
        """
        if self.jiraClient is None:
            self.login()
        if jql_str is None and jql_str == "":
            return []
        return self.jiraClient.search_issues(jql_str=jql_str, startAt=page, maxResults=limit, fields=fields)

    def get_issue_info(self,id_or_key,fields=None):
        """
        根据id或key查询issue信息
        :param id_or_key: issue id或key
        :param fields: 查询字段
        :return: issue详细信息
        """
        if self.jiraClient is None:
            self.login()
        if id_or_key is None:
            return {}
        return self.jiraClient.issue(id_or_key, fields=fields)

    def get_comments_from_issue(self,issue):
        """
        获取issue中所有comment集合
        :param issue:
        :return:
        """
        if self.jiraClient is None:
            self.login()
        if issue is None:
            return []
        return self.jiraClient.comments(issue)

    def get_comment_from_issue(self,issue,comment_id):
        if self.jiraClient is None:
            self.login()
        if issue is None:
            return {}
        if comment_id is None:
            return {}
        return self.jiraClient.comment(issue, comment_id)

    def add_comment_to_issue(self,issue_id,comment_str):
        if self.jiraClient is None:
            self.login()
        if issue_id is None or issue_id == "":
            return False
        if comment_str is None or comment_str == "":
            return False
        return self.jiraClient.add_comment(issue_id, comment_str)

    def update_comment(self,issue_id_or_key,comment_id,comment_str):
        if self.jiraClient is None:
            self.login()
        if issue_id_or_key is None or issue_id_or_key == "":
            return False
        if comment_id is None or comment_id == "":
            return False
        comment = self.get_comment_from_issue(self.get_issue_info(issue_id_or_key),comment_id)
        if comment is None:
            return False
        return comment.update(body=comment_str)

    def get_transitions_from_issue(self,issue):
        if self.jiraClient is None:
            self.login()
        if issue is None:
            return {}
        return self.jiraClient.transitions(issue)

    def assign_issue_to_user(self,issue_id,assignee):
        if self.jiraClient is None:
            self.login()
        if issue_id is None:
            return False
        if assignee is None:
            return False
        return self.jiraClient.assign_issue(issue_id, assignee)

    def transition_issues(self,issue_id,transition_id,assignee=None,comment=""):
        if self.jiraClient is None:
            self.login()
        if(issue_id is None):
            return False
        if(transition_id is None):
            return False
        if(comment is None):
            return False
        fields = None
        if assignee is not None and assignee != "":
            fields = {'assignee': {'name': assignee}}
        return self.jiraClient.transition_issue(issue=issue_id,fields=fields,transition=transition_id,comment=comment)

    def group_members(self,group_name):
        if self.jiraClient is None:
            self.login()
        if group_name is None:
            return []
        return self.jiraClient.group_members(group_name)

    def get_project_by_key(self,key):
        if self.jiraClient is None:
            self.login()
        if key is None:
            return ""
        return self.jiraClient.project(key)

    def get_custom_field_option(self,id):
        if self.jiraClient is None:
            self.login()
        if id is None:
            return ""
        return self.jiraClient.custom_field_option(id)