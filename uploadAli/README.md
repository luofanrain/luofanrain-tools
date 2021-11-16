## 阿里云批量上传点播 视频 图片

#### 1、下载以下包
-u 强制使用网络去更新包和它的依赖包
-v 显示执行的命令
```
"github.com/aliyun/alibaba-cloud-sdk-go/sdk"    
"github.com/aliyun/alibaba-cloud-sdk-go/services/vod"
"github.com/aliyun/alibaba-cloud-sdk-go/sdk/auth/credentials"  
"github.com/aliyun/aliyun-oss-go-sdk/oss"
"github.com/aliyun/alibaba-cloud-sdk-go/sdk/requests"


go get  -v -u github.com/aliyun/alibaba-cloud-sdk-go/sdk
```


### 执行outputFilePath.py,并把输出内容copy到【upload.go】38行
```
python outputFilePath.py
```

### 在阿里云拿到AccessKeyId，AccessKeySecret并写入【upload.go】118行

### 执行go上传操作
```
go run upload.go
```