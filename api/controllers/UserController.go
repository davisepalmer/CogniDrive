package controllers

import (
	"github.com/buger/jsonparser"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"net/http"
	"net/url"
)

var appId = "sJ144gmf7ZZQnBrsUGlF"
var appCode = "FLvpeHcGwrntfYPYq41qcA"

type UserController struct{}

func (u UserController) Driving(c *gin.Context) {
	coord := url.QueryEscape(c.PostForm("coord"))

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
	/*unit, err := jsonparser.GetString(body, "Response", "View", "[0]", "Result", "[0]", "Location", "LinkInfo", "SpeedLimit", "[0]", "Unit")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Couldn't read body"})
	}*/
	c.JSON(http.StatusOK, gin.H{"limit": limit})
}
