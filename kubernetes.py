from fabric.api import *
from fabric.utils import *
from fabric.contrib import *
from time import sleep
import sys
from converter import TimeConverter

class FabricException (Exception):
    pass


class Pod(object):

    def __init__(self, name, ready, status, restarts, age):
        self.name = name
        self.ready = ready
        self.status = status
        self.restarts = restarts
        self.age = age


class KubeManage(object):

    def __init__(self, kubectl):
        '''
        Kubemanager(kubeletstring)
        something like:
        kubectl kubectl --context production
        kubectl kubectl --context qa
        kubectl kubectl --context sre
        '''
        self.kubectl = kubectl
        return

    def drain(self, host):
        '''
        The function drains a node with: --ignore-daemonsets --delete-local-data --force
        It returns True if the drain is terminated with success and False in the other cases
        '''
        drain_string = 'drain --ignore-daemonsets --delete-local-data --force'
        cmd = self.kubectl + ' ' + drain_string + ' ' + host
        print(cmd)
        try:
            local(cmd)
            return True
        except Exception as e:
            print('Something goes wrong during draining ERROR: %s' % e)
        return False

    def uncordon(self, host):
        '''
        The function uncordon the node, if the command exit with uncordoned (also for nodes
        are yet uncordoned) the function returns True, False for other cases
        '''
        uncordon_string = 'uncordon'
        cmd = self.kubectl + ' ' + uncordon_string + ' ' + host
        print(cmd)
        out = local(cmd, capture=True)
        if 'uncordoned' in out:
            return True
        else:
            print('Something goes wrong during uncordon ERROR: %s' % out)
            return False

    def is_node_drained(self, host):
        '''
        The function check if the node is in "SchedulingDisabled", it returns True
        if the node is in SchedulingDisabled, False in the other cases
        '''
        check_string = 'get node'
        cmd = self.kubectl + ' ' + check_string + ' ' + host + '|grep -v NAME'
        print(cmd)
        out = local(cmd, capture=True)
        # out = 'SchedulingDisabled'
        if 'SchedulingDisabled' in out:
            return True
        return False

    def get_namespaces(self):
        '''
        The function returns all namespaces
        '''
        check_string = 'get namespaces'
        cmd = self.kubectl + ' ' + check_string
        namespaces = []
        out = local(cmd, capture=True).rsplit("\n")
        for line in out:
            if 'NAME' not in line:
                namespaces.append(line.split(" ")[0])
        return namespaces

    def get_num_of_terminating_pod(self, namespace, sleeptime=0):
        '''
        The function returns the number of terminating pods.
        Print . for everytime it founds terminating pods.
        '''
        num = 0
        sleep(sleeptime)
        sys.stdout.write(' ')
        sys.stdout.flush()
        pods = self.get_pod_for_namespace(namespace)
        for pod in pods:
            if 'Terminating' in pod.status:
                sys.stdout.write('.')
                sys.stdout.flush()
                num += 1
        return num

    def get_num_of_creating_pod(self, namespace, sleeptime=0):
        '''
        The function returns the number of creating pods
        a pod in creating state is a pod with number of container not equal to
        the nuber of expected pods.
        Print ^ for everytime it founds creating pods.
        '''
        num = 0
        sleep(sleeptime)
        sys.stdout.write(' ')
        sys.stdout.flush()
        pods = self.get_pod_for_namespace(namespace)
        for pod in pods:
            dockers, desidered = pod.ready.split('/')
            if dockers != desidered and pod.status != 'Terminating':
                sys.stdout.write('^')
                sys.stdout.flush()
                num += 1
        return num

    def get_pod_for_namespace(self, namespace, eldest='0s'):
        '''
        The function returns a list of all pods for a single namespace
        '''
        check_string = 'get pod --namespace %s' % namespace
        cmd = self.kubectl + ' ' + check_string
        eldest_in_seconds = TimeConverter(eldest).seconds
        with hide('output', 'running', 'warnings'), settings(warn_only=True):
            out = local(cmd, capture=True).rsplit("\n")
        pods = []
        for line in out:
            if 'NAME' not in line:
                name = line.split()[0]
                ready = line.split()[1]
                status = line.split()[2]
                restarts = line.split()[3]
                age = line.split()[4]
                age = TimeConverter(age).seconds
                pod = Pod(name, ready, status, restarts, age)
                if int(eldest_in_seconds) <= int(pod.age):
                    pods.append(pod)
        return pods

    def delete_pod(self, pod, namespace):
        '''
        The function delete a pod in a namespace
        '''
        do_string = 'delete pod %s --namespace %s' % (pod, namespace)
        cmd = self.kubectl + ' ' + do_string
        out = local(cmd, capture=True).rsplit("\n")
        return out


# kubeManage = KubeManage('kubectl --context production')
# kubeManage.get_namespaces()
