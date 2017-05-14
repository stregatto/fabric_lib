
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

    def getNodesFromSRV(self, domain=None, dns_addresses=None):
        '''
        Returns an iterable object with the resoult... ore false for errors.
        '''
        resolver = dns.resolver.Resolver()
        if dns_addreses:
            resolver.nameservers = secchia.separatedStringToList(dns_addresses)
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

    def isEtcdHostedOnHost(self, host, domain=None, dns_addresses=None):
        '''
        Return True if the host is in the SRV _etcd-server dns entry false in the other cases
        '''
        answer = self.getNodesFromSRV(domain, dns_addresses)
        if host in str(answer.rrset):
            return True
        else:
            return False


# etcdTools = EtcdTools()
# domain='mydomain.com'
# dns_addresses = '10.10.10.10, 10.10.10.20'
# host = 'mynode001'
# print(etcdTools.isEtcdHostedOnHost(host, domain, dns_addresses))
