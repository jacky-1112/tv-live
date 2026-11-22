import urllib.request

SOURCES = [
    "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u",
    "https://iptv-org.github.io/iptv/countries/cn.m3u",
    "https://iptv-org.github.io/iptv/countries/hk.m3u",
    "https://iptv-org.github.io/iptv/countries/tw.m3u",
    "https://iptv-org.github.io/iptv/countries/jp.m3u",
    "https://iptv-org.github.io/iptv/countries/kr.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "https://iptv-org.github.io/iptv/countries/ca.m3u",
    "https://iptv-org.github.io/iptv/countries/au.m3u",
    "https://iptv-org.github.io/iptv/countries/de.m3u",
    "https://iptv-org.github.io/iptv/countries/fr.m3u",
]

def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore").splitlines()

seen = set()
out = []
for s in SOURCES:
    try:
        lines = fetch(s)
    except Exception as e:
        print("skip", s, e)
        continue
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("#EXTINF"):
            url = ""
            j = i + 1
            while j < len(lines):
                if lines[j].strip() and not lines[j].startswith("#"):
                    url = lines[j].strip()
                    break
                j += 1
            if url and url not in seen:
                seen.add(url)
                out.append((l, url))
            i = j + 1 if url else i + 1
        else:
            i += 1

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="http://epg.51zmt.top:8000/e.xml"\n')
    for inf, u in out:
        f.write(inf + "\n" + u + "\n")
print("channels:", len(out))
