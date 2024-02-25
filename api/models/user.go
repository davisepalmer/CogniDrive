package models

type User struct {
	ID          string  `json:"id,omitempty"`
	Email       string  `json:"email"`
	FirstName   string  `json:"first_name"`
	Scores      []int   `json:"scores"`
	AccessToken string  `json:"access_token"`
	ScoreAvg    float32 `json:"score_avg"`
}
