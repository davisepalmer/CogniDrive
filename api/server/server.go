package server

import "os"

func Initialize() {
	r := NewRouter()
	port := os.Getenv("PORT")
	r.Run(":" + port)
}
