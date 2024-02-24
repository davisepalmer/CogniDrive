package main

import (
	"flag"
	"fmt"
	"github.com/davisepalmer/RideSafe/api/server"
	"os"
)

func main() {
	environment := flag.String("e", "development", "")
	flag.Usage = func() {
		fmt.Println("Usage: server -e {mode}")
		os.Exit(1)
	}
	flag.Parse()
	fmt.Println(environment)
	server.Initialize()
}
