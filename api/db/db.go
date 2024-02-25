package db

import (
	"context"
	"errors"
	"fmt"
	"github.com/redis/go-redis/v9"
	"os"
	"strconv"
	"strings"
)

type Database struct {
	Client *redis.Client
	Ctx    context.Context
}

var DB = new(Database)

func Initialize() {
	DB.Client = redis.NewClient(&redis.Options{
		Addr:     "redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820",
		Password: os.Getenv("REDIS"), // no password set
		DB:       0,                  // use default DB
	})
	DB.Ctx = context.Background()
	_, err := DB.Client.Ping(DB.Ctx).Result()
	if err != nil {
		fmt.Println("Error occured connecting to database")
		return
	}
	fmt.Println("Connected to Database")
	//addScore(33, "john@gmail.com", "1096a158-d3a5-11ee-a9d2-2977793f77f3")
	return
}

func AddScore(score int, email string, token string) error {
	fmt.Println("Finding user")

	/*userId, err := DB.Client.Get(DB.Ctx, "email:"+email).Result()
	if err == redis.Nil {
		//If user doesn't exist
		fmt.Println("Can't find user")
		return errors.New("User doesn't exist")
	} else if err != nil {
		//If error occurs searching database
		fmt.Println(err)
		return err
	}*/

	userJson, err := DB.Client.HGetAll(DB.Ctx, "user:"+email).Result()
	if err == redis.Nil {
		//If user doesn't exist
		fmt.Println("Can't find user")
		return errors.New("User doesn't exist")
	} else if err != nil {
		//If error occurs searching database
		fmt.Println(err)
		return err
	}

	if token != userJson["access_token"] {
		fmt.Println(err)
		return errors.New("Invalid access token")
	}
	var scores string
	if userJson["scores"] == "" {
		scores = strconv.Itoa(score)
	} else {
		scores = userJson["scores"] + "," + strconv.Itoa(score)
	}
	err = DB.Client.HSet(DB.Ctx, "user:"+email, "scores", scores).Err()
	if err != nil {
		fmt.Println(err)
		return errors.New("Invalid access token")
	}
	s := strings.Split(scores, ",")
	total := 0
	for _, value := range s {
		b, err := strconv.Atoi(value)
		if err != nil {
			fmt.Println(err)
			return errors.New("Error calculating score")
		}
		total = total + b
	}

	avg := fmt.Sprintf("%.2f", float32(total)/float32(len(s)))
	err = DB.Client.HSet(DB.Ctx, "user:"+email, "score_avg", avg).Err()
	if err != nil {
		fmt.Println(err)
		return errors.New("Invalid access token")
	}

	return nil
}
