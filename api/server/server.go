package server

import (
	"github.com/gin-gonic/gin"
	"os"
)

var hub *Hub
var r *gin.Engine

func Initialize() {
	hub = &Hub{
		broadcast:  make(chan []byte),
		register:   make(chan *Client),
		unregister: make(chan *Client),
		clients:    make(map[*Client]bool),
		jobs:       make([]Job, 100),
	}
	go hub.run()

	r = NewRouter()
	port := os.Getenv("PORT")
	r.Run(":" + port)
}

func (h *Hub) run() {
	for {
		select {
		case client := <-h.register:
			h.clients[client] = true
		case client := <-h.unregister:
			if _, ok := h.clients[client]; ok {
				delete(h.clients, client)
				close(client.send)
			}
		}
	}
}
