package dto

import (
	"runner/internal/domain/entities"
)

type RunData struct {
	RunNum int    `json:"test_num"`
	Input  string `json:"input"`
}

type IncomingData struct {
	Code    *string    `json:"code"`
	RunData *[]RunData `json:"run_data"`
}

type OutgoingData struct {
	TestCases *entities.TestCases `json:"test_cases"`
	ErrMsg    string              `json:"err_msg"`
}
