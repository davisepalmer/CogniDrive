package server

import (
	"github.com/davisepalmer/RideSafe/api/controllers"
	"github.com/gin-gonic/gin"
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

	router.POST("/login", user.Login)
	router.POST("/register", user.Register)

	v1 := router.Group("/v1")
	{
		userGroup := v1.Group("/user")
		{
			userGroup.GET("/:id", user.Get)
		}
	}

	return router
}
