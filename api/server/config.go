package server

import (
	"github.com/davisepalmer/RideSafe/api/controllers"
	"github.com/gin-gonic/gin"
	"net/http"
)

var user controllers.UserController
var leaderboard controllers.LeaderboardController

func NewRouter() *gin.Engine {
	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	//Initialize controllers
	user = controllers.UserController{}
	leaderboard = controllers.LeaderboardController{}

	router.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello World!")
	})
	router.POST("/driving", user.Driving)

	return router
}
