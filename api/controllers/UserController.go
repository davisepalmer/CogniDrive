package controllers

import (
	"fmt"
	"github.com/buger/jsonparser"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"time"
)

var appId = "sJ144gmf7ZZQnBrsUGlF"
var appCode = "FLvpeHcGwrntfYPYq41qcA"

type status struct {
	Coord string
	Image string
}
type UserController struct{}

func (u UserController) Driving(c *gin.Context) string {
	//Input Validation
	jobId := uuid.New().String()

	var r *http.Request = c.Request
	err := r.ParseMultipartForm(10 << 20)
	if err != nil {
		fmt.Println(1)
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Image"})
		return ""
	}

	file, _, err := r.FormFile("myFile")
	if err != nil {
		fmt.Println(2)
		fmt.Println("Error Retrieving the File")
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Image"})
		return ""
	}

	defer file.Close()
	dst, err := os.Create("./python/temp/" + jobId + ".jpg")
	if err != nil {
		fmt.Println(3)
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Image"})
		return ""
	}
	go func() {
		time.Sleep(60 * time.Second)
		e := os.Remove("./python/temp/" + jobId + ".jpg")
		if e != nil {
			fmt.Println(e)
		}
	}()

	defer dst.Close()

	_, err = io.Copy(dst, file)
	if err != nil {
		fmt.Println(4)
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Image"})
		return ""
	}
	coord := url.QueryEscape(c.Request.Header["Coord"][0])
	if coord == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Coordinates"})
		return ""
	}

	speed, err := strconv.ParseFloat(c.Request.Header["Speed"][0], 32)
	if err != nil || speed < 10 {
		fmt.Println("womp womp")
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bad Speed"})
		return ""
	}

	//API Request
	url := "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?xnlp=CL_JSMv3.0.17.0&app_id=" + appId + "&app_code=" + appCode + "&prox=" + coord + "&mode=retrieveAddresses&maxResults=1&additionaldata=SuppressStreetType%2CUnnamed&locationattributes=linkInfo"
	req, _ := http.NewRequest("GET", url, nil)
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Couldn't get limit"})
		return ""
	}

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)
	limit, err := jsonparser.GetInt(body, "Response", "View", "[0]", "Result", "[0]", "Location", "LinkInfo", "SpeedLimit", "[0]", "Value")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Couldn't read body"})
		return ""
	}

	//limit := 10
	c.JSON(http.StatusOK, gin.H{"limit": limit})
	return jobId + "=" + strconv.Itoa(int(limit)) + "=" + strconv.Itoa(int(speed))
}
