import os
import subprocess
import errno
import time
import sys

PIPE = subprocess.PIPE

from vyperlogix import misc
from vyperlogix.classes.CooperativeClass import Cooperative

__copyright__ = """\
(c). Copyright 2008-2010, Vyper Logix Corp., 

              All Rights Reserved.

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

if subprocess.mswindows:
    from win32file import ReadFile, WriteFile
    from win32pipe import PeekNamedPipe
    import msvcrt
else:
    import select
    import fcntl

class Popen(subprocess.Popen):
    def recv(self, maxsize=None):
        return self._recv('stdout', maxsize)
    
    def recv_err(self, maxsize=None):
        return self._recv('stderr', maxsize)

    def send_recv(self, input='', maxsize=None):
        return self.send(input), self.recv(maxsize), self.recv_err(maxsize)

    def get_conn_maxsize(self, which, maxsize):
        if maxsize is None:
            maxsize = 1024
        elif maxsize < 1:
            maxsize = 1
        return getattr(self, which), maxsize
    
    def _close(self, which):
        getattr(self, which).close()
        setattr(self, which, None)
    
    if subprocess.mswindows:
        def send(self, input):
            if not self.stdin:
                return None

            try:
                x = msvcrt.get_osfhandle(self.stdin.fileno())
                (errCode, written) = WriteFile(x, input)
            except ValueError:
                return self._close('stdin')
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            try:
                x = msvcrt.get_osfhandle(conn.fileno())
                (read, nAvail, nMessage) = PeekNamedPipe(x, 0)
                if maxsize < nAvail:
                    nAvail = maxsize
                if nAvail > 0:
                    (errCode, read) = ReadFile(x, nAvail, None)
            except ValueError:
                return self._close(which)
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close(which)
                raise
            
            if self.universal_newlines:
                read = self._translate_newlines(read)
            return read

    else:
        def send(self, input):
            if not self.stdin:
                return None

            if not select.select([], [self.stdin], [], 0)[1]:
                return 0

            try:
                written = os.write(self.stdin.fileno(), input)
            except OSError, why:
                if why[0] == errno.EPIPE: #broken pipe
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            flags = fcntl.fcntl(conn, fcntl.F_GETFL)
            if not conn.closed:
                fcntl.fcntl(conn, fcntl.F_SETFL, flags| os.O_NONBLOCK)
            
            try:
                if not select.select([conn], [], [], 0)[0]:
                    return ''
                
                r = conn.read(maxsize)
                if not r:
                    return self._close(which)
    
                if self.universal_newlines:
                    r = self._translate_newlines(r)
                return r
            finally:
                if not conn.closed:
                    fcntl.fcntl(conn, fcntl.F_SETFL, flags)

message = "Other end disconnected!"

def recv_some(p, t=.1, e=1, tr=5, stderr=0):
    if tr < 1:
        tr = 1
    x = time.time()+t
    y = []
    r = ''
    pr = p.recv
    if stderr:
        pr = p.recv_err
    while time.time() < x or r:
        r = pr()
        if r is None:
            if e:
                raise Exception(message)
            else:
                break
        elif r:
            y.append(r)
        else:
            time.sleep(max((x-time.time())/tr, 1))
    return ''.join(y)
    
def send_all(p, data):
    while len(data):
        sent = p.send(data)
        if sent is None:
            raise Exception(message)
        data = buffer(data, sent)
        
class Shell(Cooperative):
    '''Shell processor.'''
    def __init__(self,commands,shell=None,env=None,isExit=False,isWait=False,isVerbose=False,fOut=sys.stderr):
        '''isVerbose=True and fOut=something work together otherwise there will be no putput from the commands that were issued.'''
        self.isVerbose = isVerbose
        self.fOut = fOut
        if (not misc.isList(commands)):
            commands = [commands]
        if sys.platform == 'win32':
            shell, commands, self.tail = ('cmd' if (shell is None) else shell, commands, '\r\n')
        else:
            shell, commands, self.tail = ('sh' if (shell is None) else shell, commands, '\n')

        e = os.environ if (env == None) else env
        self.proc = Popen(shell, env=e, stdin=PIPE, stdout=PIPE)
        if (self.isVerbose):
            print >>self.fOut, recv_some(self.proc),
        for cmd in commands:
            send_all(self.proc, str(cmd) + self.tail)
            if (self.isVerbose):
                print >>self.fOut, recv_some(self.proc),
        if (isExit):
            self.doExit()
        if (isWait):
            self.doWait()
    
    def doSend(self,data):
        send_all(self.proc, data)
        if (self.isVerbose):
            print >>self.fOut, recv_some(self.proc, e=0)
            
    def doSendWithTail(self,data):
        self.doSend(data + self.tail)
            
    def doExit(self):
        send_all(self.proc, 'exit' + self.tail)
        if (self.isVerbose):
            print >>self.fOut, recv_some(self.proc, e=0)

    def doWait(self):
        self.proc.wait()
            