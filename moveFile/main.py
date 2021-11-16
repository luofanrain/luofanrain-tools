## 批次移动文件
import os, shutil  
  
if __name__ == "__main__":
	# 绝对路径  
	currentDir = os.getcwd()
	sourceDir = os.path.abspath(f"{currentDir}/source")  
	targetDir = os.path.abspath(f"{currentDir}/target")  
	
	if not os.path.exists(targetDir):  
	    os.makedirs(targetDir)  
	index = 0 # 数字分类
	maxNum = 500 # 按文件数量分类
	if os.path.exists(sourceDir):  
		for root,dirs,files in os.walk(sourceDir):  
			for file in files:
				dirname = f"{targetDir}/{str(int(index/maxNum + 1))}"
				index+=1
				targetDir = os.path.abspath(dirname)  
				if not os.path.exists(targetDir):
					os.makedirs(targetDir)
				src_file = os.path.join(root, file)  
				shutil.copy(src_file, targetDir)  
				os.remove(src_file)
				if index%maxNum == 0:
					print(index)