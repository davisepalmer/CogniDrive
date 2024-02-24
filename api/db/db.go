package db

import (
	"context"
	"github.com/redis/go-redis/v9"
	"os"
)

type Database struct {
	Client *redis.Client
	Ctx    context.Context
}

var ctx = context.Background()
var DB = new(Database)

func Initialize() {
	DB.Client = redis.NewClient(&redis.Options{
		Addr:     "redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820",
		Password: os.Getenv("REDIS"), // no password set
		DB:       0,                  // use default DB
	})
}
