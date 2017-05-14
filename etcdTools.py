
from fabric.api import *
from fabric.utils import *
from fabric.contrib import *
import secchia
import dns.resolver

class ConfigurationError(Exception):
    pass

class EvaluationError(Exception):
    pass


class EtcdTools(object):
    '''
    This module is intende to semplify the manage of etcd, is not intended
    to substitute python etcd module.
    This module depends on dnspython.
    '''

    def __init__(self):
        return

    def get_nodes_from_SRV(self, domain=None, dns_addresses=None):
        '''
        Returns an iterable object with the resoult... ore false for errors.
        '''
        resolver = dns.resolver.Resolver()
        if dns_addresses:
            resolver.nameservers = secchia.separated_string_to_list(dns_addresses)
        else:
            print("Using default dns resolver srevers.")
        if not domain:
            raise ConfigurationError('You have to specify the domain name to query')
            return 4
        srv_prefix = '_etcd-server._tcp.' + domain
        try:
            answers = resolver.query(srv_prefix, 'SRV')
        except Exception as e:
            raise EvaluationError(e)
            return 1
        return answers

    def is_etcd_hosted_on_host(self, host, domain=None, dns_addresses=None):
        '''
        Return True if the host is in the SRV _etcd-server dns entry false in the other cases
        '''
        answer = self.get_nodes_from_SRV(domain, dns_addresses)
        if host in str(answer.rrset):
            return True
        else:
            return False


# etcdTools = EtcdTools()
# domain='mydomain.com'
# dns_addresses = '10.10.10.10, 10.10.10.20'
# host = 'mynode001'
# print(etcdTools.is_etcd_hosted_on_host(host, domain, dns_addresses))
