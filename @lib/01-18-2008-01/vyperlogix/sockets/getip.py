import sys
import socket
import struct

def get_ip_address(ifname):
    try:
        import fcntl
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])
    except:
        import platform
        from vyperlogix import misc
        print >> sys.stderr, '%s.WARNING: Cannot use this function in %s.' % (misc.funcName(),platform.uname()[0])
    return None

if (__name__ == '__main__'):
    import platform
    from vyperlogix.misc import _utils
    if (_utils.isUsingWindows):
        print >> sys.stderr, '%s.WARNING: Cannot use this function in %s.' % (misc.funcName(),platform.uname()[0])
    else:
        print get_ip_address('eth0')
    