import chardet
from scrapy.selector.unified import Selector
from ..items import NewsItem
import scrapy
from scrapy.http.response.html import HtmlResponse
import datetime
from lxml.html import clean
import re
import datetime
from ..settings import USER_AGENTS_LIST, PROXY_IP_LIST
import random 

def get_time_now():

    return datetime.datetime.now()

def get_current_time():
    current_time = get_time_now()
    news_time = current_time.strftime("%Y-%m-%d %H:%M")
    return news_time
def get_standard_time():
    return strtime_to_datetime(datetime.datetime.strftime(get_time_now(), '%Y-%m-%d 0:00'))

def strtime_to_datetime(strtime: str, format="%Y-%m-%d %H:%M"):

    return datetime.datetime.strptime(strtime, format)

def compare_date(date: str):
    date_limit = 2
    tem_num = date.count(":")
    if tem_num == 1:
        current_time = strtime_to_datetime(date)
    elif tem_num == 2:
        current_time = strtime_to_datetime(date, "%Y-%m-%d %H:%M:%S")
    else:
        current_time = get_time_now()

    standard_time = get_standard_time() - datetime.timedelta(days=(date_limit - 1))
    return True if current_time >= standard_time else False

def create_next_url(response, time_list, page_list:list):
    page_limit = 2
    if time_list:
        last_time = time_list[-1]
        if compare_date(last_time):
            page_str = "|".join(page_list)


            url = response.url

            # page_info = re.search(r'(page=|up=|pNo=)([\d]*)', url)
            page_info = re.search(r'({})([\d]*)'.format(page_str), url)

            page = page_info.group(1)
            page_num = int(page_info.group(2))

            if page_num <= page_limit:
                next_url = url.replace(page_info.group(), page + str(page_num + 1))
                # print(next_url)
                return next_url
  
                # self.server.lpush(self.redis_key, next_url)

def parse_time_default(response: HtmlResponse, xpath="//span"):

    res = parse_txt_details_default(response, xpath)
    news_time = None
    # times = re.search(r'([\d]{4})\D([\d]{1,2})[\D]{1,3}([\d]{1,2})[\D]{1,3}([\d]{1,2}[:|：][\d]{2})', res)
    times = re.search(r'([\d]{4})\D([\d]{2})[\D]{1,3}([\d]{1,2})[\D]{1,3}([\d]{1,2}[:|：][\d]{2})', res)

    if times:
        news_time = '{}-{}-{} {}'.format(times.group(1), times.group(2), times.group(3), times.group(4))

    elif re.search(r'([\d]{1,2})\D([\d]{1,2})[\D]{1,3}([\d]{1,2}[:|：][\d]{2})', res):
        t = re.search(r'([\d]{1,2})\D([\d]{1,2})[\D]{1,3}([\d]{1,2}[:|：][\d]{2})', res)
        news_time = "{}-{}-{} {}".format(get_time_now().year, t.group(1), t.group(2), t.group(3))

    elif re.search(r'([\d]{4})\D([\d]{1,2})\D([\d]{1,2})', res):
        t1 = re.search(r'([\d]{4})\D([\d]{1,2})\D([\d]{1,2})', res)
        news_time = "{}-{}-{} 0:00".format(t1.group(1), t1.group(2), t1.group(3))

    return news_time

def decode_byte_str(response):

    encoding_dict = chardet.detect(response.body)
    encoding = encoding_dict.get('encoding')
    confidence = encoding_dict.get('confidence')

    res = response.body.decode(encoding, 'ignore')

    return res

def parse_url_title_default(html_a: Selector):
        url = html_a.xpath("./@href").extract_first()
        title = html_a.xpath("./text()").extract_first()

        return url.strip() if url else url, title.strip() if title else title

def save_url_title(url, title):
        item = NewsItem()
        item['news_url'] = url
        item['news_title'] = title
        return item

def create_request(item: NewsItem, callback=None, method='GET', headers=None, body=None,
                       cookies=None, meta=None, encoding='utf-8', priority=0,
                       dont_filter=False, errback=None, flags=None):

    return scrapy.Request(
        item['news_url'],
        meta={'item':item},
        callback=callback,
        headers=headers,
        dont_filter=dont_filter,
    )

def parse_txt_details_default(response: HtmlResponse, s_xpath="//div/p", join_str=''):
    details_list = response.xpath(s_xpath)
    details_html_list = details_list.re(".*")
    details_html = join_str.join(details_html_list)
    return clear_label(details_html)


def get_time_now():

    return datetime.datetime.now()


def get_current_time():
        current_time = get_time_now()
        news_time = current_time.strftime("%Y-%m-%d %H:%M")
        return news_time

def save_time_txt(response, times, txt):
        item = response.meta['item']
        item['news_time'] = times
        item['news_txt'] = txt

        # print(item['news_url'])
        # print(times)
        # print(item['news_title'])
        # print(txt)
        return item

def clear_data(data):

    if not data:
        return data

    tags_list = set(re.findall(r"<([\w]+).*?>", data))
    default_tages_list = ['div', 'font', 'p', 'strong', 'b', 'a', 'span', 'img', 'i', 'table', 'tbody', 'tr', 'td', 'br',
                     'center', 'em', 'video', 'strike', 'track', 'dl', 'mark', 'ruby', 'h5', 'section', 'ul', 'li']

    cleaner = clean.Cleaner(
        remove_tags=(list(tags_list) + default_tages_list)
    )

    details = cleaner.clean_html(data)
    details = details.replace('div', '').replace('</div>', '').replace('<>', '').replace('</>', '')
    details = details.replace('\xa0', '')
    details = details.replace('\u3000', '')
    details = details.replace('\r', '')
    details = details.replace('<br>', '')

    return details.strip()

def clear_label( txt):

        if not txt:
            return txt
        txt = txt.replace("</p>", "</p>\n")
        txt = clear_data(txt)
        while "\n\n" in txt:
            txt = txt.replace("\n\n", "\n")
        return txt
def get_user_agent():
    ua_index = 8
    return USER_AGENTS_LIST[ua_index]


def get_random_user_agent():

    return random.choice(USER_AGENTS_LIST)

def get_proxy_ip():

    return random.choice(PROXY_IP_LIST)

import json
class common_spider(scrapy.Spider):
    def save_cookies(self, cookies, expires):
        keys_name = "{}_cookies".format(self.name)
        self.server.set(keys_name, json.dumps(cookies), expires)

    def get_cookies(self):
        keys_name = "{}_cookies".format(self.name)
        value = self.server.get(keys_name)
        if not value:
            return None
        return json.loads(value)

