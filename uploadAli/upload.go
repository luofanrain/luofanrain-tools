package main
import (
    "fmt"
		"encoding/json"
		"encoding/base64"
		"github.com/aliyun/alibaba-cloud-sdk-go/sdk"
    	"github.com/aliyun/alibaba-cloud-sdk-go/services/vod"
    	"github.com/aliyun/alibaba-cloud-sdk-go/sdk/auth/credentials"  
		"os"
    	"github.com/aliyun/aliyun-oss-go-sdk/oss"
		"github.com/aliyun/alibaba-cloud-sdk-go/sdk/requests"
)


type UploadAuthDTO struct {
	AccessKeyId string
	AccessKeySecret string
	SecurityToken string
}
type UploadAddressDTO struct {
	Endpoint string
	Bucket string
	FileName string
}
type UploadData struct {
	Title string `json:"title"`
	FilePath string `json:"filePath"`
	Categary string `json:"categary"`
}
type FileList struct {
	List []UploadData `json:"list"`
}
// categary  文件分类
// filePath 本地文件路径
// title  上传标题
var VideoList string = `{
	"list":
		[
			{
				"categary": "分类",
				"filePath": "c:/users/uploadali/media3/预览视频.mp4"
				"title": "预览视频" 
			}
		]
}`
func InitVodClient(accessKeyId string, accessKeySecret string) (client *vod.Client, err error) {
	// 点播服务接入区域
	regionId := "cn-shanghai"
	// 创建授权对象
	credential := &credentials.AccessKeyCredential{
			accessKeyId,
			accessKeySecret,
	}
	// 自定义config
	config := sdk.NewConfig()
	config.AutoRetry = true      // 失败是否自动重试
	config.MaxRetryTime = 3      // 最大重试次数
	config.Timeout = 3000000000  // 连接超时，单位：纳秒；默认为3秒
	// 创建vodClient实例
	return vod.NewClientWithOptions(regionId, config, credential)
}
func MyCreateUploadVideo(client *vod.Client,data UploadData)  (response *vod.CreateUploadVideoResponse, err error) {
	request := vod.CreateCreateUploadVideoRequest()
	CateId :=  getCategary(data.Categary)
	request.Title = data.Title
	request.FileName = data.FilePath
	request.CateId = CateId
	return client.CreateUploadVideo(request)
}
func InitOssClient(uploadAuthDTO UploadAuthDTO, uploadAddressDTO UploadAddressDTO) (*oss.Client, error) {
	client, err := oss.New(uploadAddressDTO.Endpoint,
			uploadAuthDTO.AccessKeyId,
			uploadAuthDTO.AccessKeySecret,
			oss.SecurityToken(uploadAuthDTO.SecurityToken),
			oss.Timeout(86400*7, 86400*7))
	return client, err
}
func UploadLocalFile(client *oss.Client, uploadAddressDTO UploadAddressDTO, fileItem UploadData) {
	// 获取存储空间。
	bucket, err := client.Bucket(uploadAddressDTO.Bucket)
	if err != nil {
			fmt.Println("Error:", err)
			os.Exit(-1)
	}
	// 上传本地文件。
	err = bucket.PutObjectFromFile(uploadAddressDTO.FileName, fileItem.FilePath)
	if err != nil {
			fmt.Println("Error:", err)
			os.Exit(-1)
	}
}
func MyRefreshUploadVideo(client *vod.Client) (response *vod.RefreshUploadVideoResponse, err error) {
	request := vod.CreateRefreshUploadVideoRequest()
	request.VideoId = ""
	request.AcceptFormat = "JSON"
	return client.RefreshUploadVideo(request)
}

func MyGetPlayInfo(client *vod.Client, videoId string) (response *vod.GetPlayInfoResponse, err error) {
	// 创建API请求并设置参数，调用vod.Create${apiName}Request
	request := vod.CreateGetPlayInfoRequest()
	request.VideoId = videoId
	request.AcceptFormat = "JSON"

	// 发起请求并处理异常，调用client.${apiName}(request)
	return client.GetPlayInfo(request)
}

func getCategary(key string) (CateId requests.Integer){
	switch key {	
		case "book": // 类型
			return  "类型id" //需要去阿里云后台拿
	}
}

func UploadTheFile(fileItem UploadData){
		// 初始化VOD客户端并获取上传地址和凭证
	var accessKeyId string = "*";                    // 您的AccessKeyId
	var accessKeySecret string = "*";            // 您的AccessKeySecret

	var vodClient, initVodClientErr = InitVodClient(accessKeyId, accessKeySecret)
	if initVodClientErr != nil {
			fmt.Println("Error:", initVodClientErr)
			return
	}
	
	// 获取上传地址和凭证
	var response, createUploadVideoErr = MyCreateUploadVideo(vodClient,fileItem)
	if createUploadVideoErr != nil {
			fmt.Println("Error:", createUploadVideoErr)
			return
	}
	// 执行成功会返回VideoId、UploadAddress和UploadAuth
	var videoId = response.VideoId
	var uploadAuthDTO UploadAuthDTO
	var uploadAddressDTO UploadAddressDTO
	var uploadAuthDecode, _ = base64.StdEncoding.DecodeString(response.UploadAuth)
	var uploadAddressDecode, _ = base64.StdEncoding.DecodeString(response.UploadAddress)
	json.Unmarshal(uploadAuthDecode, &uploadAuthDTO)
	json.Unmarshal(uploadAddressDecode, &uploadAddressDTO)
	// 使用UploadAuth和UploadAddress初始化OSS客户端
	var ossClient, _ = InitOssClient(uploadAuthDTO, uploadAddressDTO)
	// 上传文件，注意是同步上传会阻塞等待，耗时与文件大小和网络上行带宽有关
	UploadLocalFile(ossClient, uploadAddressDTO, fileItem)
	//MultipartUploadFile(ossClient, uploadAddressDTO, localFile)
	// fmt.Println(result)
	var res,resErr = MyGetPlayInfo(vodClient,videoId)
	fmt.Println(res,resErr)
	fmt.Println("Succeed, VideoId:", videoId)
}
func main() {
	var item FileList
	if err := json.Unmarshal([]byte(VideoList), &item);err != nil{
		fmt.Println(err)
	}else {
		curLen := len(item.List)
		for i:=0;i<curLen;i++ {
			fmt.Println(item.List[i])
			fmt.Println(i)
			UploadTheFile(item.List[i])
		}
	}
}

