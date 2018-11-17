# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from TtaoSpider.items import TtaospiderItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com', 'tmall.com']

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                      "/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    def start_requests(self):
        url = "https://item.taobao.com/item.htm?id=574519986668"
        url2 = "https://detail.tmall.com/item.htm?id=550958953463&cm_id=140105335569ed55e27b"
        if "taobao" in url:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={
                    "cookiejar": 1,
                    # "proxy": proxy_ip_port,
                },
                callback=self.parse_tb_comment,
                dont_filter=True, )
        elif "tmall" in url:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={
                    "cookiejar": 1,
                    # "proxy": proxy_ip_port,
                },
                callback=self.parse_tm_comment,
                dont_filter=True, )

    def parse_tb_comment(self, response):
        user_num_id1 = response.headers.get("At_Autype").decode()
        if user_num_id1:
            user_num_id2 = re.findall(r"\d_(\d+)", user_num_id1)
            auction_num_id1 = re.findall(r"id=(\d+)", response.url)
            if user_num_id2 and auction_num_id1:
                user_num_id = user_num_id2[0]
                auction_num_id = auction_num_id1[0]
                comment_url1 = 'https://rate.taobao.com/feedRateList.htm?auctionNumId={}&userNumId={}&currentPageNum=1&pageSize=20'.format(auction_num_id, user_num_id)
                # 整个页面数
                response1 = requests.get(url=comment_url1, headers=self.headers)
                total_nums = re.findall(r"maxPage\":(\d+),", response1.text)
                if total_nums:
                    for total_num in range(total_nums[0]):
                        comment_url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId={}&userNumId={}' \
                                      '&currentPageNum={}&pageSize=10000'.format(auction_num_id, user_num_id, total_num)
                        impress_url = "https://rate.taobao.com/detailCommon.htm?auctionNumId={}&userNumId={}"
                        yield scrapy.Request(url=comment_url,
                                             headers=self.headers,
                                             meta={
                                                 "cookiejar": response.meta['cookiejar']
                                                 # "proxy": proxy_ip_port,
                                             },
                                             callback=self.comment_detail,
                                             dont_filter=True, )
                    yield scrapy.Request(url=impress_url.format(auction_num_id, user_num_id),
                                         headers=self.headers,
                                         meta={
                                             "cookiejar": response.meta['cookiejar']
                                             # "proxy": proxy_ip_port,
                                         },
                                         callback=self.comment_detail,
                                         dont_filter=True, )

    @staticmethod
    def comment_detail(response):
        item = TtaospiderItem()
        try:
            # 大家印象
            if "detailCommon" in response.url:
                impress_data = eval(response.text.replace("false", "\'false\'").replace(
                    "true", "\'true\'").replace("null", "\'null\'")).get("data", "")
                impress_list = impress_data.get("impress", "")
                if impress_list:
                    for impress in impress_list:
                        item["title"] = impress.get("title", "-1")
                        item["count"] = impress.get("count", "-1")

            else:
                comment_list = eval(response.text.replace("false", "\'false\'").replace(
                    "true", "\'true\'").replace("null", "\'null\'")).get("comments", "")

                if comment_list:
                    for comment in comment_list:
                        item["comment_content"] = comment.get("content", "-1")
                        item["comment_date"] = comment.get("date", "-1")
                        item["comment_user_nike"] = comment.get("user", {}).get("nick", "-1")
                        item["comment_user_vip"] = comment.get("user", {}).get("vip", "-1")
                        item["goods_color"] = comment.get("auction", {}).get("sku", "-1")
                        item["rate_id"] = comment.get("rateId", "-1")
                        print(item)
        except Exception as e:
            print("eval错误{}？".format(e))

    def parse_tm_comment(self, response):
        pass
