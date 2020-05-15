#!usr/bin/python
# -*- coding: utf-8 -*-
import os
import conf as cf
import orderdirs as od
from checkpath import *
import shutil

if __name__ == '__main__':
	try:
		# 加载配置文件
		conf = cf.JsonConf()
		conf.LoadJson()
		
		# 加载升级文件夹顺序文件
		order = od.OrderDirs(conf.dict["orderfile"])
		order.LoadOrder()

		# 校验输出路径是否存在，不存在则创建
		if not CheckifExists(conf.dict["result"]):
			print('输出文件夹[',conf.dict["result"], ']不存在，已创建！')
			os.makedirs(conf.dict["result"])

		for kv in conf.dict["dirs_cover"].keys():
			outdir = os.path.join(conf.dict["result"],kv)
			if not CheckifExists(outdir):
				print('输出文件夹[',outdir, ']不存在，已创建！')
				os.makedirs(outdir)
		for kv in conf.dict["dirs_order"].keys():
			outdir = os.path.join(conf.dict["result"],kv)
			if not CheckifExists(outdir):
				print('输出文件夹[',outdir, ']不存在，已创建！')
				os.makedirs(outdir)

		# 按顺序表顺序升级
		i = 0
		for dir in order.filelist:
			i = i + 1
			_dir = os.path.join(conf.dict["path"],dir)
			# 顺序表里的路径不存在时，直接跳过
			if not CheckifExists(_dir):
				print('[不存在]',_dir)
				continue
			dirs = os.listdir(_dir)
			for name in dirs:
				for kv in zip(conf.dict["dirs_cover"].keys(),conf.dict["dirs_cover"].values()):
					if kv[1].find(name)>=0:
						#shutil.copytree(os.path.join(_dir,name), os.path.join(conf.dict["result"],kv[0]))
						os.system("xcopy /s /Y %s %s" % (os.path.join(_dir,name), os.path.join(conf.dict["result"],kv[0]))
				for kv in zip(conf.dict["dirs_corder"].keys(),conf.dict["dirs_corder"].values()):
					if kv[1].find(name)>=0:
						#shutil.copytree(os.path.join(_dir,name), os.path.join(conf.dict["result"],kv[0]))
						os.system("xcopy /s /Y %s %s" % (os.path.join(_dir,name), os.path.join(conf.dict["result"],kv[0])))
			print('[完  成]',_dir)

	except Exception as e:
		print(e.args)