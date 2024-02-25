package server

import (
	"bytes"
	"fmt"
	"github.com/gorilla/websocket"
	"log"
	"strings"
	"time"
)

type Client struct {
	hub  *Hub
	conn *websocket.Conn
	send chan []byte
}

type Job struct {
	Id    string
	Token string
	Score int
}

type Hub struct {
	clients    map[*Client]bool
	broadcast  chan []byte
	register   chan *Client
	unregister chan *Client
	jobs       []Job
}

func (c *Client) readPump() {
	defer func() {
		c.hub.unregister <- c
		c.conn.Close()
	}()
	c.conn.SetPongHandler(func(string) error { c.conn.SetReadDeadline(time.Now().Add(60 * time.Second)); return nil })
	for {
		_, message, err := c.conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Printf("error: %v", err)
			}
			break
		}
		message = bytes.TrimSpace(bytes.Replace(message, []byte("\n"), []byte(" "), -1))
		fmt.Println(string(message))
		jobStatus := strings.Split(string(message), "=")
		fmt.Println("Job ", jobStatus[0], "score:", jobStatus[1])
		//c.hub.broadcast <- message
	}
}
