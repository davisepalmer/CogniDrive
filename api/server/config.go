package server

import (
	"github.com/davisepalmer/RideSafe/api/controllers"
	"github.com/davisepalmer/RideSafe/api/db"
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

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "home.html", nil)
	})
	/*router.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello World!")
	})*/
	router.POST("/driving", func(c *gin.Context) {
		id := user.Driving(c)
		//c.Request.Header["email"][0]
		//c.Request.Header["token"][0]
		if id != "" {
			for client := range hub.Clients {
				client.send <- []byte(id)
			}
			db.AddScore(33, "john@gmail.com", "1096a158-d3a5-11ee-a9d2-2977793f77f3")
		}
	})

	router.GET("/testjob", func(c *gin.Context) {
		for client := range hub.Clients {
			client.send <- []byte("test2.jpg")
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
		go client.write()
	})

	return router
}
