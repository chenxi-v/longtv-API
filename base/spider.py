# -*- coding: utf-8 -*-
"""
兼容层：适配TVBox风格的爬虫
"""
from abc import abstractmethod
from typing import Dict, List, Optional, Any
import httpx
import logging

logger = logging.getLogger(__name__)


class Spider:
    """
    TVBox风格的Spider基类
    使用驼峰命名的方法
    """

    def __init__(self):
        """初始化爬虫"""
        self._cache: Dict[str, Any] = {}
        self._client = httpx.Client(timeout=30.0)
        self._proxy_url: Optional[str] = None

    def init(self, extend: str = "") -> None:
        """初始化爬虫"""
        pass

    def homeContent(self, filter: bool = False) -> Dict[str, Any]:
        """获取首页内容"""
        return {}

    def homeVideoContent(self) -> Dict[str, Any]:
        """获取首页视频"""
        return {}

    def categoryContent(self, tid: str, pg: str = "1", filter: bool = False, extend: Dict = {}) -> Dict[str, Any]:
        """获取分类内容"""
        return {}

    def detailContent(self, ids: List[str]) -> Dict[str, Any]:
        """获取视频详情"""
        return {}

    def searchContent(self, key: str, quick: bool = False, pg: str = "1") -> Dict[str, Any]:
        """搜索内容"""
        return {}

    def playerContent(self, flag: str, id: str, vipFlags: List[str] = None) -> Dict[str, Any]:
        """获取播放地址"""
        return {}

    def isVideoFormat(self, url: str) -> bool:
        """判断是否为视频格式"""
        return False

    def manualVideoCheck(self) -> bool:
        """手动视频检查"""
        return False

    def destroy(self) -> None:
        """销毁爬虫"""
        pass

    def localProxy(self, param: Dict) -> Optional[List[Any]]:
        """本地代理"""
        return None

    def proxy(self, param: Dict) -> Optional[List[Any]]:
        """
        代理调用 - 调用 localProxy

        Args:
            param: 代理参数

        Returns:
            代理结果
        """
        return self.localProxy(param)

    def getCache(self, key: str) -> Optional[Any]:
        """获取缓存"""
        return self._cache.get(key)

    def setCache(self, key: str, value: Any) -> None:
        """设置缓存"""
        self._cache[key] = value

    def fetch(self, url: str, **kwargs) -> httpx.Response:
        """
        发送HTTP请求

        Args:
            url: 请求URL
            **kwargs: httpx请求参数

        Returns:
            httpx.Response对象
        """
        return self._client.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        """
        发送POST请求

        Args:
            url: 请求URL
            **kwargs: httpx请求参数

        Returns:
            httpx.Response对象
        """
        return self._client.request("POST", url, **kwargs)

    def getProxyUrl(self) -> str:
        """
        获取代理URL

        Returns:
            代理URL字符串
        """
        return ""

    def setProxyUrl(self, proxy_url: str) -> None:
        """
        设置代理URL

        Args:
            proxy_url: 代理URL
        """
        self._proxy_url = proxy_url
        if proxy_url:
            self._client = httpx.Client(timeout=30.0, proxies={"http://": proxy_url, "https://": proxy_url})
        else:
            self._client = httpx.Client(timeout=30.0)
