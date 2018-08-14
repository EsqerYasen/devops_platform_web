from ldap3 import Connection, SUBTREE, ServerPool
import logging

logger = logging.getLogger('devops_platform_log')

class AdAuthenticate:
    LDAP_SERVER_POOL = ["ldap://sghdc15:389"]
    ADMIN_DN = "Serv-IT-AMP"
    ADMIN_PASSWORD = "Yum78ik,"
    SEARCH_BASE = "ou=yumchina,dc=cn,DC=yumchina,DC=com"

    @staticmethod
    def authenricate(username,password):
        bool = False
        try:
            if username and password:
                userInfo = AdAuthenticate.getUserInfo(username)
                if userInfo and userInfo.get("dn",None):
                    ldap_server_pool = ServerPool(AdAuthenticate.LDAP_SERVER_POOL)
                    conn = Connection(ldap_server_pool, user=userInfo['dn'], password=password, check_names=True, lazy=False,raise_exceptions=False)
                    conn.bind()
                    if conn.result["description"] == "success":
                       bool = True
        except Exception as e:
            logging.error(e)
        finally:
            if conn:
                conn.unbind()
        return bool

    @staticmethod
    def getUserInfo(username):
        userInfo = None
        try:
            ldap_server_pool = ServerPool(AdAuthenticate.LDAP_SERVER_POOL)
            conn = Connection(ldap_server_pool, user=AdAuthenticate.ADMIN_DN, password=AdAuthenticate.ADMIN_PASSWORD, check_names=True, lazy=False,raise_exceptions=False)
            conn.open()
            conn.bind()
            res = conn.search(
                search_base=AdAuthenticate.SEARCH_BASE,
                search_filter='(samaccountname={})'.format(username),
                search_scope=SUBTREE,
                attributes=["displayName","cn","sn","mail","description"],
                paged_size=5
            )
            if res:
                entry = conn.response[0]
                attr_dict = entry['attributes']
                userInfo = {
                    'dn':entry['dn'],
                    'cn':attr_dict['cn'],
                    'sn':attr_dict['sn'],
                    'mail':attr_dict['mail'],
                    'displayName': attr_dict['displayName'],
                    'description': attr_dict['description'],
                }
        except Exception as e:
            logging.error(e)
        finally:
            if conn:
                conn.unbind()
        return userInfo



