#coding=utf-8
from optparse import OptionParser
import urllib2
from qiniu import conf
from qiniu import rs
import sys

conf.ACCESS_KEY = ''
conf.SECRET_KEY = ''


def printUsage():
    content = '''
    Usage: python qm3u8.py -u <Url> [-o <Output>] [-e <Expires>]
    '''
    print content
    return


def getPrivateM3U8(url, output=None, expires=3600):
    req = urllib2.Request(url)
    try:
        conn = urllib2.urlopen(req, timeout=15)
        data = conn.read()
    except Exception as e:
        raise e
    dataList = data.split('\n')
    dataList = map(lambda x: makePrivateUrl(x, expires), dataList)
    content = '\n'.join(dataList)
    if output:
        makeFile(output, content)
    return content


def makePrivateUrl(content, expires=3600):
    if not content.startswith('http://'):
        return content
    policy = rs.GetPolicy()
    policy.expires = expires
    return policy.make_request(content)


def makeFile(output, content):
    with open(output, 'w') as f:
        f.write(content)
    return


def optParser():
    optp = OptionParser()
    #settings
    optp.add_option('-u', '--url', help='url of the m3u8 file',
                    dest='url', default=None)
    optp.add_option('-o', '--output', help='output file path',
                    dest='output', default=None)
    optp.add_option('-e', '--expires', help='expire time',
                    dest='expires', default=3600)

    opts, args = optp.parse_args()
    return opts.url, opts.output, int(opts.expires)


def main():
    url, output, expires = optParser()
    if not url:
        printUsage()
        return
    print getPrivateM3U8(url, output, expires)


if __name__ == '__main__':
    main()