package entities

type TestCase struct {
	TestNum int    `json:"test_num"`
	Input   string `json:"input"`
	Output  string `json:"output"`
}

type TestCases []TestCase
