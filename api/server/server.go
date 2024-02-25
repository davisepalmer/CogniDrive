package server

import (
	"fmt"
	"github.com/davisepalmer/RideSafe/api/db"
	"github.com/gin-gonic/gin"
	"os"
)

var hub *Hub
var r *gin.Engine
var jobs map[string]Job

func Initialize() {
	hub = &Hub{
		broadcast:  make(chan []byte),
		register:   make(chan *Client),
		unregister: make(chan *Client),
		Clients:    make(map[*Client]bool),
		//jobs:       make([]Job, 100),
	}
	jobs = make(map[string]Job)
	go hub.run()
	fmt.Println("Starting Database...")
	db.Initialize()
	r = NewRouter()
	port := os.Getenv("PORT")
	r.Run(":" + port)
}

func (h *Hub) run() {
	for {
		select {
		case client := <-h.register:
			h.Clients[client] = true
		case client := <-h.unregister:
			if _, ok := h.Clients[client]; ok {
				delete(h.Clients, client)
				close(client.send)
			}
		case message := <-h.broadcast:
			for client := range h.Clients {
				select {
				case client.send <- message:
				default:
					close(client.send)
					delete(h.Clients, client)
				}
			}
		}
	}
}
