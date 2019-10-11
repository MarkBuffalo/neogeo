
![Picture of the Earth, I guess](https://i.imgur.com/bjKHl7C.png)

# What is it?

It's neogeo. A very badly named, and very simple geolocation tool for python that integrates with ipstack. Other than the API token from ipstack, it works out of the box with python3. Or at least it's supposed to.

# Why would you use it?

Sometimes you have to do the thing with OSINT quickly. Or something. 

# Installation


1. Sign up for a free account at https://ipstack.com/
2. ```git clone https://github.com/MarkBuffalo/neogeo.git && cd neogeo```
3. ```python3 neogeo.py```


# Options 
```
$ python3 neogeo.py -h
usage: neogeo.py [-h] [-ip IP] [--ips IPS] [--token TOKEN] [-f FORMAT] [-hc]
                 [--full]

Geolocate a single ip, or a list of them. Requires an ipstack API key

optional arguments:
  -h, --help            show this help message and exit
  -ip IP, --ip IP       Input a single IP address to check
  --ips IPS             Point to a file, new-line separated, containing
                        multiple IP addresses.
  --token TOKEN         Your IP Stack API token
  -f FORMAT, --format FORMAT
                        The file output format. Options: json, csv, tsv
  -hc, --hide           Hide the columns and just output the results.
  --full                Decide whether or not to output a bunch of redundant
                        information.
```


# Example usage:

### 1. Single IP Address

When you just need a single hit.
```
$ python3 neogeo.py -i 172.217.12.36
ip	location	city	region_name	zip	country_name	continent_name	latitude	longitude
172.217.12.36	🇺🇸	Manhattan	New York	10020	United States	North America	40.7589111328125	-73.97901916503906
```
#### 2. Without columns

When you just need a single hit, and no column information.
```
$ python3 neogeo.py -i 172.217.12.36 --hide
172.217.12.36	🇺🇸	Manhattan	New York	10020	United States	North America	40.7589111328125	-73.97901916503906
```

#### 3. Multiple IP Addresses (TSV -- default)

When you need multiple IP addresses. With the `tsv` format (`--format tsv`; default), this is a great option for pasting into google sheets, or excel spreadsheets.
```
$ python3 neogeo.py --ips iptest.txt 
ip	location	city	region_name	zip	country_name	continent_name	latitude	longitude
172.217.12.36	🇺🇸	Manhattan	New York	10020	United States	North America	40.7589111328125	-73.97901916503906
98.137.246.8	🇺🇸	Quincy	Washington	98848	United States	North America	47.206031799316406	-119.7993392944336
98.138.219.231	🇺🇸	Manhattan	New York	10003	United States	North America	40.73139190673828	-73.9884033203125
98.138.219.232	🇺🇸	Manhattan	New York	10003	United States	North America	40.73139190673828	-73.9884033203125
216.58.194.68	🇺🇸	Mountain View	California	94043	United States	North America	37.419158935546875	-122.07540893554688
72.30.35.10	🇺🇸	Manhattan	New York	10003	United States	North America	40.73139190673828	-73.9884033203125
```

#### 4. Different formats (CSV)

Makes it easy to use csv tools to import it.
````
$ python3 neogeo.py --ips iptest.txt --format csv
ip,location,city,region_name,zip,country_name,continent_name,latitude,longitude
172.217.12.36,🇺🇸,Manhattan,New York,10020,United States,North America,40.7589111328125,-73.97901916503906
98.137.246.8,🇺🇸,Quincy,Washington,98848,United States,North America,47.206031799316406,-119.7993392944336
98.138.219.231,🇺🇸,Manhattan,New York,10003,United States,North America,40.73139190673828,-73.9884033203125
216.58.194.68,🇺🇸,Mountain View,California,94043,United States,North America,37.419158935546875,-122.07540893554688
72.30.35.10,🇺🇸,Manhattan,New York,10003,United States,North America,40.73139190673828,-73.9884033203125
98.138.219.232,🇺🇸,Manhattan,New York,10003,United States,North America,40.73139190673828,-73.9884033203125

````

#### 5. Different Formats (JSON)

When you just want to print json for some reason.
```
 python3 neogeo.py --ips iptest.txt --format json
{"ip":"98.138.219.232","type":"ipv4","continent_code":"NA","continent_name":"North America","country_code":"US","country_name":"United States","region_code":"NY","region_name":"New York","city":"Manhattan","zip":"10003","latitude":40.73139190673828,"longitude":-73.9884033203125,"location":{"geoname_id":5125771,"capital":"Washington D.C.","languages":[{"code":"en","name":"English","native":"English"}],"country_flag":"http:\/\/assets.ipstack.com\/flags\/us.svg","country_flag_emoji":"\ud83c\uddfa\ud83c\uddf8","country_flag_emoji_unicode":"U+1F1FA U+1F1F8","calling_code":"1","is_eu":false}}
{"ip":"98.137.246.8","type":"ipv4","continent_code":"NA","continent_name":"North America","country_code":"US","country_name":"United States","region_code":"WA","region_name":"Washington","city":"Quincy","zip":"98848","latitude":47.206031799316406,"longitude":-119.7993392944336,"location":{"geoname_id":null,"capital":"Washington D.C.","languages":[{"code":"en","name":"English","native":"English"}],"country_flag":"http:\/\/assets.ipstack.com\/flags\/us.svg","country_flag_emoji":"\ud83c\uddfa\ud83c\uddf8","country_flag_emoji_unicode":"U+1F1FA U+1F1F8","calling_code":"1","is_eu":false}}
[...]

```

#### 6. Pipe to `jq` with `--format json` option so you can do your own thing.

When you don't want to bother with the way neogeo parses stuff.

```
{
  "ip": "98.138.219.232",
  "type": "ipv4",
  "continent_code": "NA",
  "continent_name": "North America",
  "country_code": "US",
  "country_name": "United States",
  "region_code": "NY",
  "region_name": "New York",
  "city": "Manhattan",
  "zip": "10003",
  "latitude": 40.73139190673828,
  "longitude": -73.9884033203125,
  "location": {
    "geoname_id": 5125771,
    "capital": "Washington D.C.",
    "languages": [
      {
        "code": "en",
        "name": "English",
        "native": "English"
      }
    ],
    "country_flag": "http://assets.ipstack.com/flags/us.svg",
    "country_flag_emoji": "🇺🇸",
    "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
    "calling_code": "1",
    "is_eu": false
  }
}
```
#### 7. Coming soon: a better `--full`
```
NotImplementedException
```




# Problems running?

- Make sure there are no blank lines in your file with new-line separated IP addresses. I'll fix it some other time. 
- Anything else? Let me know. 
