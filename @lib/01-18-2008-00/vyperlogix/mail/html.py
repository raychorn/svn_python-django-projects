
def asHTMLEmail(html, text, subject):
    """Create a mime-message that will render HTML in popular
	   MUAs, text in better ones"""
    import MimeWriter
    import mimetools
    import cStringIO

    out = cStringIO.StringIO() # output buffer for our message 
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    #
    # set up some basic headers... we put subject here
    # because smtplib.sendmail expects it to be in the
    # message body
    #
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    #
    # start the multipart section of the message
    # multipart/alternative seems to work better
    # on some MUAs than multipart/mixed
    #
    writer.startmultipartbody("alternative")
    writer.flushheaders()
    #
    # the plain text section
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    #
    # start the html subpart of the message
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    #
    # returns us a file-ish object we can write to
    #
    pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    #
    # Now that we're done, close our writer and
    # return the message body
    #
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg

if __name__=="__main__":
    import smtplib
    from vyperlogix.mail import mailServer
    from vyperlogix.html.strip import strip_tags
    try:
        f = open("Z:\\@myMagma\\python-local-new-trunk\\test\\win32\\pop\\mailboxes\\hiral.kotak@einfochips.com\\2008-09-10T113433.html", 'r')
        html = f.read()
        f.close()
        text = strip_tags(html)
        subject = "Today's Newsletter!"
        message = asHTMLEmail(html, text, subject)
	_host = "tide2.magma-da.com"
	_port = 8025
        server = smtplib.SMTP(host="mailhost.magma-da.com",port=25)
        server.sendmail('molten-support@magma-da.com', 'raychorn@hotmail.com', message)
        server.quit()
        server = smtplib.SMTP(host=_host,port=_port)
        server.sendmail('molten-support@magma-da.com', 'raychorn@hotmail.com', html)
        server.quit()
	mailserver = mailServer.GMailServer('','',server=_host,port=_port)
	mailserver._sendEmail('molten-support@magma-da.com', 'raychorn@hotmail.com', html)
    except Exception, details:
        print 'ERROR: %s' % (str(details))
    finally:
        print 'Done !'
    