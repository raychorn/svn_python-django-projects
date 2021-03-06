PyAMF provides Action Message Format (AMF) support for Python that is
compatible with the Flash Player.

The Adobe Integrated Runtime and Flash Player use AMF to communicate
between an application and a remote server. AMF encodes remote procedure
calls (RPC) into a compact binary representation that can be transferred
over HTTP/HTTPS or the RTMP/RTMPS protocol. Objects and data values are
serialized into this binary format, which increases performance,
allowing applications to load data up to 10 times faster than with
text-based formats such as XML or SOAP.

AMF 3, the default serialization for ActionScript 3.0, provides various
advantages over AMF0, which is used for ActionScript 1.0 and 2.0. AMF 3
sends data over the network more efficiently than AMF 0. AMF 3 supports
sending int and uint objects as integers and supports data types that are
available only in ActionScript 3.0, such as ByteArray, ArrayCollection,
and IExternalizable.