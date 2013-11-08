#coding=utf-8
from optparse import OptionParser


def livePlaylist(content, prefix=None, listSize=3, isLive=True, allowCache=False):
    if not content:
        return ''
    contentList = content.split('\n')
    cacheTagCt = 0
    cacheTag = '#EXT-X-ALLOW-CACHE:YES' \
        if (isLive is not True) or (allowCache is True) \
        else '#EXT-X-ALLOW-CACHE:NO'
    hasSegSec = False
    inSegSec = False
    segSecStart = -1
    segSecEnd = -1

    for n, c in enumerate(contentList):
        if c.startswith('#EXT-X-ALLOW-CACHE'):  # cache tag
            cacheTagCt += 1
            contentList[n] = cacheTag
        elif inSegSec is False and c.startswith('#EXTINF'):
            hasSegSec = True
            segSecStart = n
            inSegSec = True
        elif inSegSec is True and c.startswith('#') and c.startswith('#EXTINF') is not True:
            segSecEnd = n
            inSegSec = False
        else:
            pass

    if hasSegSec is True:
        headSec = contentList[:segSecStart]
        seqSec = contentList[segSecStart:][-3:] if inSegSec else contentList[segSecStart:segSecEnd][-3:]
        tailSec = [] if inSegSec else contentList[segSecEnd:]
        return '%s\n%s\n%s' % ('\n'.join(headSec), '\n'.join(seqSec), '\n'.join(tailSec))
    else:
        return '\n'.join(contentList)


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