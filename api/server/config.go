package server

import (
	"github.com/davisepalmer/RideSafe/api/controllers"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
)

var user controllers.UserController
var leaderboard controllers.LeaderboardController

var upgrader = websocket.Upgrader{}

func NewRouter() *gin.Engine {
	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())
	router.LoadHTMLGlob("*.html")
	//Initialize controllers
	user = controllers.UserController{}
	leaderboard = controllers.LeaderboardController{}

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "home.html", nil)
	})
	/*router.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello World!")
	})*/
	router.POST("/driving", user.Driving)

	router.GET("/testjob", func(c *gin.Context) {
		for client := range hub.clients {
			select {
			case client.send <- []byte("test2.jpg"):
			default:
				close(client.send)
				delete(hub.clients, client)
			}
		}
	})

	router.GET("/supersecretimageprocessor", func(c *gin.Context) {
		conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
		if err != nil {
			log.Println(err)
			return
		}
		client := &Client{hub: hub, conn: conn, send: make(chan []byte, 256)}
		client.hub.register <- client

		go client.read()
	})

	return router
}
