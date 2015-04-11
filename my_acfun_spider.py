#coding:utf-8

import urllib2
import gzip
import re
import StringIO

doc = '''
Attention:
It is not a perfect spider,be careful.

Author : Flint_x and you
   Ver : 0.1415926
contact: 940852578@qq.com

'''

print (doc)

arc_get_list = []

# def deal_gzip(data):
# 	data = StringIO.StringIO(data)
# 	gz_page = gzip.GzipFile(data)
# 	html = gz_page.read()
# 	return html


def get_acfun(type_name,page_num,min_click_num):
	i = 0
	while i < page_num:
		
		i += 1
		print r'the ' + str(i) + ' page , Total ' + str(page_num) + ' page'
		this_url = 'http://www.acfun.tv/v/' + type_name +'/index_' + str(i) + '.htm'
		# print this_url
		try:
			data = urllib2.urlopen(this_url).read()
			# print data
		# gzip包处理
			# data = StringIO.StringIO(data)
			# gz_page = gzip.GzipFile(fileobj = data)
			# data = gz_page.read()
		# 正则表达式提取关键字
			re_str = '''<a title="(.*?)"article-info">'''
			re_pat = re.compile(re_str)
			arc_list = re_pat.findall(data)
			# print arc_list[0]
			print '-------------cut-off rule-----------------'
	
			for item in arc_list:
				# 统计点击量
				click_str = '''条评论，(.*?)人围观'''
				click_pat = re.compile(click_str)
				click_list = click_pat.findall(item)
				# print click_list[0]
	
				if str(click_list[0]).find('-') < 0:
					click_num = int(click_list[0])
					if click_num > min_click_num:
						# 标题提取
						name_str = '''class="title">(.*?)</a>'''
						name_pat = re.compile(name_str)
						name_list = name_pat.findall(item)
						# print name_list
						# ac号提取
						ac_str = '''</span><a href="/a/(.*?)" target="_blank'''
						ac_pat = re.compile(ac_str)
						ac_list = ac_pat.findall(item)
						# 评论数提取
						com_str = '''共有(.*?)条评论'''
						com_pat = re.compile(com_str)
						com_list = com_pat.findall(item)
						# print com_list[0]
						com_num = int(com_list[0])
						#得分计算公式
						point = click_num + 50 * com_num
	
						print '---->',ac_list[0]
						print '---->',name_list[0]
						print '---->click number :',click_list[0]
						print '---->comment number :',com_list[0]
						print '---->points :',point
						print '---------------------------------------------------------'
						# 添加文章信息
						arc_get_list.append({'ac' : ac_list[0] , 'name' : name_list[0] , 'click' : click_list[0] , 'comment' : com_list[0] , 'point' : point})
		except urllib2.HTTPError, e:
			print 'urllib2.HTTPError'
		except urllib2.URLError, e:
			print 'urllib2.URLError'

def sort_and_write(new_path,list):
	arc_get_list.sort(key = lambda obj: int(obj.get('point')) , reverse = True)
	print 'Total Arcticle : ', len(arc_get_list)
	print '---------->Writing~'

	f = open(new_path,'w+')
	x = 0 
	for arc in list :
		x += 1
		insert_str1 = 'No.' + str(x) + '\n' + str(arc['ac']) + '\n' + str(arc['name']) + '\n'
		insert_str2 = '共有 ' + str(arc['click']) + ' 人围观，' + str(arc['comment']) + '条评论' + '\n'
		f.write(insert_str1)
		f.write(insert_str2)
	f.close()

get_acfun('list110',7520,100000)
sort_and_write("D:\Arc_list.txt",arc_get_list)




	





