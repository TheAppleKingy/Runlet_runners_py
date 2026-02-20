package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"runner/internal/application/dto"
	"runner/internal/domain"
	"runner/internal/domain/entities"
	"runner/internal/infrastructure/config"
)

func checkFileExists(path string) error {
	info, err := os.Stat(path)
	if err != nil {
		if os.IsNotExist(err) {
			return fmt.Errorf("file %s not exists", path)
		}
		return err
	}
	if info.IsDir() {
		return fmt.Errorf("%s is a dir, not file", path)
	}
	return nil
}

func getIncomingData(path string) *dto.IncomingData {
	defer os.Remove(path)
	if err := checkFileExists(path); err != nil {
		fmt.Printf("internal error: %v", err)
		os.Exit(1)
	}

	fileData, err := os.ReadFile(path)
	if err != nil {
		fmt.Printf("internal error: unable to read mounted %s: %v", path, err)
		os.Exit(1)
	}
	var data dto.IncomingData
	if err := json.Unmarshal(fileData, &data); err != nil {
		fmt.Printf("internal error: unable to decode mounted %s: %v", path, err)
		os.Exit(1)
	}
	return &data
}

func main() {
	emptyCases := entities.TestCases{}
	response := &dto.OutgoingData{
		TestCases: &emptyCases,
		ErrMsg:    "",
	}
	printRes := func(err error) {
		if err != nil {
			response.ErrMsg = err.Error()
		}
		output, _ := json.Marshal(response)
		fmt.Println(string(output))
	}

	if err := config.LoadConfigs(); err != nil {
		printRes(fmt.Errorf("internal error: %v", err))
		os.Exit(1)
	}
	runArgsJSON := flag.String("run_args", "", "")
	compileArgsJSON := flag.String("compile_args", "", "")
	srcPlaceholder := flag.String("src_placeholder", "", "")
	binPlaceholder := flag.String("bin_placeholder", "", "")
	inputPath := flag.String("input", "", "")
	timeout := flag.Int("run_timeout", 0, "")
	flag.Parse()
	if *inputPath == "" {
		printRes(fmt.Errorf("internal error: compile args was not provide"))
		os.Exit(1)
	}
	if *compileArgsJSON == "" {
		printRes(fmt.Errorf("internal error: compile args was not provide"))
		os.Exit(1)
	}
	if *runArgsJSON == "" {
		printRes(fmt.Errorf("internal error: run args was not provide"))
		os.Exit(1)
	}
	if *srcPlaceholder == "" {
		printRes(fmt.Errorf("internal error: src_placeholder was not provide"))
		os.Exit(1)
	}
	if *binPlaceholder == "" {
		printRes(fmt.Errorf("internal error: bin_placeholder was not provide"))
		os.Exit(1)
	}
	if *timeout == 0 {
		printRes(fmt.Errorf("internal error: timeout for running one test case cannot be 0"))
		os.Exit(1)
	}
	var runArgs domain.RunArgsType
	var compileArgs domain.CompileArgsType
	if err := json.Unmarshal([]byte(*runArgsJSON), &runArgs); err != nil {
		printRes(fmt.Errorf("internal error: invalid run_args JSON: %v", err))
		os.Exit(1)
	}
	if err := json.Unmarshal([]byte(*compileArgsJSON), &compileArgs); err != nil {
		fmt.Printf("internal error: invalid run_args JSON: %v", err)
		os.Exit(1)
	}
	data := getIncomingData(*inputPath)
	runner := NewCodeRunner(runArgs, compileArgs, *srcPlaceholder, *binPlaceholder, config.AppConfig.Language)
	runService := NewRunCodeUseCase(runner)
	results, err := runService.TestSolution(data, *timeout)
	response.TestCases = results
	printRes(err)
}
