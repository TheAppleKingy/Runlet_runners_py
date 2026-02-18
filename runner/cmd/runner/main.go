package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"runner/internal/application/dto"
	"runner/internal/infrastructure/config"
)

func main() {
	if err := config.LoadConfigs(); err != nil {
		fmt.Println("internal error:", err)
		os.Exit(1)
	}
	code := flag.String("code", "", "")
	data := flag.String("data", "", "")
	flag.Parse()
	if *code == "" {
		fmt.Println("internal error: code was not provide")
		os.Exit(1)
	}
	if *data == "" {
		fmt.Println("internal error: run data was not provide")
		os.Exit(1)
	}

	runService := NewRunCodeUseCase()
	var testsData []dto.RunData
	if err := json.Unmarshal([]byte(*data), &testsData); err != nil {
		fmt.Println("internal error: unable to dencode given run data:", err)
		os.Exit(1)
	}
	results, err := runService.TestSolution(testsData, config.AppConfig.Language, code)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	// Выводим результаты в JSON
	output, err := json.Marshal(results)
	if err != nil {
		fmt.Println("internal error: unable to encode result data:", err)
		os.Exit(1)
	}

	fmt.Println(string(output))
}
