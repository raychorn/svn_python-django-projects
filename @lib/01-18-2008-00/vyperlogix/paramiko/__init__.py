__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import threading
import time
import traceback

import paramiko

from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils

__pageant_warning__ = '(Are you sure you have Pageant Running with the host key installed ?)'

class ParamikoSFTP(Cooperative):
    def __init__(self,hostname,port,username,password,callback=None,logPath=os.path.abspath(os.path.dirname(sys.argv[0]))):
        self.__hostname__ = hostname
        self.__port__ = port
        self.__username__ = username
        self.__password__ = password
        self.__transport__ = None
        _utils._makeDirs(logPath)
        paramiko.util.log_to_file(os.path.join(logPath,'%s.log' % (ObjectTypeName.objectSignature(self))))
        if self.hostname.find(':') >= 0:
            self.__hostname__, portstr = hostname.split(':')
            self.__port__ = int(portstr)
        try:
            self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock__.connect((self.hostname, self.port))
        except Exception, _details:
            info_string = _utils.formattedException(details=_details)
            print '*** Connect failed: %s' % (info_string)
            sys.exit(1)

        try:
            self.__transport__ = paramiko.Transport(self.__sock__)
            try:
                self.transport.start_client()
            except paramiko.SSHException:
                print '*** SSH negotiation failed.'
                sys.exit(1)
        
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            except IOError:
                try:
                    keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
                except IOError:
                    print '*** Unable to open host keys file'
                    keys = {}
        
            # check server's host key -- this is important.
            key = self.transport.get_remote_server_key()
            if not keys.has_key(hostname):
                print '*** WARNING: Unknown host key!  %s' % (__pageant_warning__)
            elif not keys[hostname].has_key(key.get_name()):
                print '*** WARNING: Unknown host key! %s' % (__pageant_warning__)
            elif keys[hostname][key.get_name()] != key:
                print '*** WARNING: Host key has changed!!! %s' % (__pageant_warning__)
                sys.exit(1)
            else:
                print '*** Host key OK.'
        
            self.agent_auth()
            if not self.transport.is_authenticated():
                self.manual_auth()
            if not self.transport.is_authenticated():
                print '*** Authentication failed. :('
                t.close()
                sys.exit(1)
        
            self.__channel__ = self.transport.open_session()
            self.channel.get_pty()
            print '*** Here we go!'
            print
            if (callable(callback)):
                callback(self)
            self.channel.close()
            self.transport.close()
        
        except Exception, _details:
            info_string = _utils.formattedException(details=_details)
            print info_string
            try:
                self.transport.close()
            except:
                pass
            sys.exit(1)

            
    def hostname():
        doc = "hostname"
        def fget(self):
            return self.__hostname__
        return locals()
    hostname = property(**hostname())
    
    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        return locals()
    port = property(**port())
    
    def username():
        doc = "username"
        def fget(self):
            return self.__username__
        return locals()
    username = property(**username())
    
    def password():
        doc = "password"
        def fget(self):
            return self.__password__
        return locals()
    password = property(**password())
    
    def transport():
        doc = "transport"
        def fget(self):
            return self.__transport__
        return locals()
    transport = property(**transport())
    
    def channel():
        doc = "channel"
        def fget(self):
            return self.__channel__
        return locals()
    channel = property(**channel())
    
    def getSFTPClient():
        doc = "SFTPClient"
        def fget(self):
            return paramiko.SFTPClient.from_transport(self.transport)
        return locals()
    getSFTPClient = property(**getSFTPClient())
    
    def agent_auth(self):
        """
        Attempt to authenticate to the given transport using any of the private
        keys available from an SSH agent.
        """
        
        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        if len(agent_keys) == 0:
            return
            
        for key in agent_keys:
            print 'Trying ssh-agent key %s' % hexlify(key.get_fingerprint()),
            try:
                self.transport.auth_publickey(self.username, key)
                print '... success!'
                return
            except paramiko.SSHException:
                print '... nope.'
    
    def manual_auth(self):
        self.transport.auth_password(self.username, self.password)
        
    def read(self,sftp,fpath):
        return sftp.open(fpath, 'r').read()
    
    def write(self,sftp,fpath,data):
        sftp.open(fpath, 'w').write(data)
        
if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

