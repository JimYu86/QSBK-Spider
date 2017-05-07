# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

# 糗事百科爬虫类
class QSBK:
	# 初始化方法，定义变量
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
		# 初始化headers
		self.headers = {'User-Agent':self.user_agent}
		# 存放段子的变量，每一个元素是每一页的段子
		self.stories = []
		# 存放程序是否继续运行的变量
		self.enable = False
		# 爬取的糗事百科热门消息，因为首页与第二页的URL地址不同，因此做判断
		self.url = ""

	# 传入某一页的索引获得页面代码
	def getPage(self,pageIndex):
		try:
			# 若第一次打开，则第一页为首页，否则为第二页
			if self.url:
				self.url = 'http://www.qiushibaike.com/8hr/page/' + str(pageIndex)
			else:
				self.url = 'http://www.qiushibaike.com'
			# 构建请求的request
			request = urllib2.Request(self.url,headers = self.headers)
			# 利用urlopen获取页面代码
			response = urllib2.urlopen(request)
			# 将页面转为UTF-8编码
			pageCode = response.read().decode('utf-8')
			return pageCode

		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print u"连接糗事百科失败，原因：",e.reason
				return None

	# 传入某一页代码
	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败"
			return None
		pattern = re.compile('<h2>(.*?)</h2>.*?class="content">.*?<span>(.*?)</.*?class="number">(.*?)</i>.*?</',re.S)
		items = re.findall(pattern,pageCode)
		# 用来储存每页的段子
		pageStories = []
		# 遍历正则表达式匹配的信息
		for item in items:
			repalceBR = re.compile('<br/>')
			# 这里的sub方法表示将item[1]也就是正文内容里所有的br/换行标签全部替换为\n，表示换行
			text = re.sub(repalceBR,"\n",item[1])
			# strip()方法用于移除字符串头尾指定的字符（默认为空格），这里即为移除首尾空格，append将每个元素追加到集合中去
			pageStories.append([item[0].strip(),text.strip(),item[2].strip()])
		return pageStories

	# 加载并提取页面的内容，加入到列表中
	def loadPage(self):
		# 如果当前未看的段子数量少于两个，则加载新一页
			if self.enable == True:
				if len(self.stories) < 2:
					# 获取新一页
					pageStories = self.getPageItems(self.pageIndex)
					# 将该页的段子存放到全局list中
					if pageStories:
						self.stories.append(pageStories)
						# 获取完之后页码索引加一，表示下次读取下一页
						self.pageIndex += 1

	# 调用该方法，每次敲回车打印输出一个段子
	def getOneStory(self,pageStories,page):
		# 遍历传入过来的一个段子的所有属性，这里具体包含发布人，正文，点赞数
		for story in pageStories:
			# 等待用户输入
			input = raw_input()
			# 每当输入回车一次，判断一下是否要加载新页面
			self.loadPage()
			# 如果输入Q则程序结束
			if input == "Q":
				self.enable = False
				return
			# 它们用于格式化字符串。%s作为字符串的占位符%d作为数字的占位符。它们的关联值通过使用%运算符的元组传入。
			print u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1])

	# 开始方法
	def start(self):
		print u"正在读取糗事百科，按回车查看新段子，按Q键退出..."
		# 使变量变为True，程序可以正常运行
		self.enable = True
		# 先加载一页内容
		self.loadPage()
		# 局部变量，控制当前读到了第几页
		nowPage = 0
		while self.enable:
		    if len(self.stories) > 0:
		    	# 从全局list中获取一页的段子
		    	pageStories = self.stories[0]
		    	# 当前读到的页数加一
		    	nowPage += 1
		    	# 将全局list中第一个元素删除，因为已经取出
		    	del self.stories[0]
		    	# 输出该页的段子
		    	self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

