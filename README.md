# crawler_related
## 一、proxy_pool--代理池
目的：利用网上公开的免费代理来解决爬取目标网站封IP的问题，但免费代理存在很多不可用的需要进行筛选剔除

pip安装：aiohttp、requests、redis-py、pyquery、Flask库

基础模块：存储模块、获取模块、检测模块、接口模块

1.存储模块

	把抓取下来的代理存储到Redis的有序集合，集合包括代理和分数两个字段，代理字段使用IP+端口号192.168.11.23:80的形式保存，分数字段代表可靠性程度最高100分最低0分。
	
获取模块会从网上获取新代理存到redis并设置为10分，检测模块检测新代理如可用直接设置成100分如不可用减1分，并且检测模块会定时对所有代理进行检测可用就设置100分不可用则减1分，0分时剔除代理。

2.获取模块

	抓取代理 66、Proxy360、Goubanjia 三个免费代理网站或者付费代理网站
	
3.检测模块

	代理可用设置成100分不可用减1分，0分时剔除。为了提高效率使用异步请求库aiohttp来进行检测
	
4.接口模块

	为了更安全方便的获取使用flask提供一个Web API接口，通过访问接口即可随机拿到可用分数最高的代理，可以部署到本地或者云服务器上

