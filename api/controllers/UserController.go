package controllers

import (
	"bytes"
	"encoding/base64"
	"errors"
	"fmt"
	"github.com/gin-gonic/gin"
	"image"
	"io/ioutil"
	"net/http"
	"strings"
)

var appId = "sJ144gmf7ZZQnBrsUGlF"
var appCode = "FLvpeHcGwrntfYPYq41qcA"

type status struct {
	Coord string
	Image string
}
type UserController struct{}

func (u UserController) Driving(c *gin.Context) {
	//Input Validation
	bBody, _ := ioutil.ReadAll(c.Request.Body)
	imageData := strings.Split(string(bBody), "image=")[1]
	disk, err := saveImageToDisk("test-1.jpg", imageData)
	if err != nil {
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Error saving file"})
		return
	}
	fmt.Println(disk)
	/*if image == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Image"})
		return
	}
	coord := url.QueryEscape(c.PostForm("coord"))
	if coord == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Coordinates"})
		return
	}

	//API Request
	url := "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?xnlp=CL_JSMv3.0.17.0&app_id=" + appId + "&app_code=" + appCode + "&prox=" + coord + "&mode=retrieveAddresses&maxResults=1&additionaldata=SuppressStreetType%2CUnnamed&locationattributes=linkInfo"
	req, _ := http.NewRequest("GET", url, nil)
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Couldn't get limit"})
		return
	}

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)
	limit, err := jsonparser.GetInt(body, "Response", "View", "[0]", "Result", "[0]", "Location", "LinkInfo", "SpeedLimit", "[0]", "Value")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Couldn't read body"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"limit": limit})*/
	c.JSON(http.StatusOK, gin.H{"limit": 10})
}

func saveImageToDisk(fileNameBase, data string) (string, error) {
	idx := strings.Index(data, ";base64,")
	if idx < 0 {
		return "", errors.New("Invalid image")
	}
	reader := base64.NewDecoder(base64.StdEncoding, strings.NewReader(data[idx+8:]))
	buff := bytes.Buffer{}
	_, err := buff.ReadFrom(reader)
	if err != nil {
		return "", err
	}
	imgCfg, fm, err := image.DecodeConfig(bytes.NewReader(buff.Bytes()))
	if err != nil {
		return "", err
	}

	if imgCfg.Width != 750 || imgCfg.Height != 685 {
		return "", errors.New("Invalid size")
	}

	fileName := fileNameBase + "." + fm
	ioutil.WriteFile(fileName, buff.Bytes(), 0644)

	return fileName, err
}
