package models

type User struct {
	ID        string `json:"id,omitempty"`
	Email     string `json:"email"`
	FirstName string `json:"firstName"`
	Score     int    `json:"score"`
}
