import aiohttp
import asyncio
import os
import re
import shutil
import UnityPy
import json
import timeit
from PIL import Image

http_proxy = 'http://127.0.0.1:10809'
str_stamp_f = 'images/icon/stamp/l/framed/'
str_stamp_n = 'images/icon/stamp/l/'

ROOT = os.path.dirname(os.path.realpath(__file__))
IMG = os.path.join(ROOT, 'stamps\\img')
ASSETS = os.path.join(ROOT, 'assets')
os.makedirs(IMG, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)


def loadStampsUrl(sid, resVer):
    assetbundle = {
        'jp': f'../DLScripts/prs_manifests_archive/{resVer}/assetbundle.manifest',
        'zh_cn': f'../DLScripts/prs_manifests_archive/{resVer}/assetbundle.zh_cn.manifest',
        'zh_tw': f'../DLScripts/prs_manifests_archive/{resVer}/assetbundle.zh_tw.manifest',
        'en_us': f'../DLScripts/prs_manifests_archive/{resVer}/assetbundle.en_us.manifest'}
    stamp = {}
    for lang in assetbundle:
        with open(assetbundle[lang], 'r', encoding='utf-8') as m:
            for l in m:
                sp = l.split(',')
                if sp[0] == '%s%s' % (str_stamp_n, sid):
                    stamp['%s-%s-%s' % (sid, lang, 'normal')] = sp[1].strip()
                if sp[0] == '%s%s' % (str_stamp_f, sid):
                    stamp['%s-%s-%s' % (sid, lang, 'framed')] = sp[1].strip()
            m.close()
    return stamp


async def download(session, url, filename):
    async with session.get(url, proxy=http_proxy) as resp:
        if resp.status != 200:
            print(filename, ': download failed.')
        else:
            with open(os.path.join(ASSETS, filename), 'wb') as f:
                f.write(await resp.read())


async def downloadStamps(stamp):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            download(session, stamp[s], s)
            for s in stamp
        ])


def dumpStamps():
    for f in os.listdir(ASSETS):
        sid = f.split('-')[0]
        lang = f.split('-')[1]
        isFramed = True if f.split('-')[2] == 'framed' else False
        dumpStampFromAsset(os.path.join(ASSETS, f), sid, lang, isFramed)
    print('parse complete.')


def dumpStampFromAsset(filepath, sid, lang, isFramed):
    imageData = {}
    env = UnityPy.load(filepath)
    for obj in env.objects:
        data = obj.read()
        if str(data.type) == 'Texture2D':
            if 'alpha' in str(data.name):
                imageData['a8'] = data.image
            else:
                imageData['img'] = data.image
    frame = 'framed' if isFramed else 'normal'
    filepath = os.path.join(IMG, '%s\\%s\\%s.png' % (lang, frame, sid))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    combineA8(imageData).save(filepath)


def combineA8(imageData):
    (w, h) = imageData['img'].size
    (z, z, z, a) = imageData['a8'].resize((w, h), Image.ANTIALIAS).split()
    (r, g, b) = imageData['img'].split()
    return Image.merge("RGBA", (r, g, b, a))


def main(sid, resVer):
    start = timeit.default_timer()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(downloadStamps(loadStampsUrl(sid, resVer)))
    print("download complete.")

    dumpStamps()

    end = timeit.default_timer()
    print('time spent: ' + str(end-start))


if __name__ == '__main__':
    for sid in ['13101', '13102', '13103', '13201', '13202']:
        main(sid, '20211231_NHan3Y7Fnkeja8Ss')
