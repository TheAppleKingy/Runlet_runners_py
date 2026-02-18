package implementations

import (
	"bytes"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"runner/internal/application/dto"
	"runner/internal/domain/entities"
	"runner/internal/infrastructure/config"
	"strings"
)

// CodeRunner is implementation of interfaces.Runner
type CodeRunner struct{}

// compile compiles binary based on src via lang compilator and returns name of binary file or provided src if language is interpreted
func (cr CodeRunner) compile(src *string, lang string) error {
	binaryName := strings.TrimSuffix(*src, "."+lang)
	langConf, ok := config.LaunguagesConfig.Languages[lang]
	if !ok {
		return errors.New("unable to load config data")
	}
	args := langConf.CompileCommandArgs
	if len(args) == 0 {
		return nil
	}

	compileArgs := make([]string, len(args))
	for i, arg := range args {
		srcPlaceholder := config.LaunguagesConfig.SrcPlaceholder
		binPlaceholder := config.LaunguagesConfig.BinPlaceholder
		switch {
		case strings.Contains(arg, srcPlaceholder):
			compileArgs[i] = strings.ReplaceAll(arg, srcPlaceholder, *src)
		case strings.Contains(arg, binPlaceholder):
			compileArgs[i] = strings.ReplaceAll(arg, binPlaceholder, binaryName)
		default:
			compileArgs[i] = arg
		}
	}

	cmd := exec.Command(compileArgs[0], compileArgs[1:]...)
	var stderr bytes.Buffer
	cmd.Stderr = &stderr
	if err := cmd.Run(); err != nil {
		errMsg := strings.TrimSuffix(stderr.String(), "\n")
		if errMsg != "" {
			return fmt.Errorf("unable to compile '%s' code: %s", lang, errMsg)
		}
		return fmt.Errorf("unable to compile '%s' code: %w", lang, err)
	}
	os.Remove(*src)
	*src = binaryName
	return nil
}

func (cr CodeRunner) Run(runData []dto.RunData, src *string, lang string) (entities.TestCases, error) {
	var results entities.TestCases
	if err := cr.compile(src, lang); err != nil {
		return entities.TestCases{}, fmt.Errorf("internal error: %w", err)
	}
	args := config.LaunguagesConfig.Languages[lang].RunCommandArgs
	runArgs := make([]string, len(args))
	for i, arg := range args {
		runArgs[i] = strings.ReplaceAll(arg, config.LaunguagesConfig.SrcPlaceholder, *src)
	}

	for _, testData := range runData {
		cmd := exec.Command(runArgs[0], runArgs[1:]...)
		var stdout, stderr bytes.Buffer
		cmd.Stdout = &stdout
		cmd.Stderr = &stderr
		cmd.Stdin = bytes.NewBufferString(testData.Input)
		err := cmd.Run()
		out := strings.TrimRight(stdout.String(), "\n")
		errMsg := strings.TrimRight(stderr.String(), "\n")
		if err != nil {
			if errMsg != "" {
				return entities.TestCases{{
					TestNum: testData.RunNum,
					Input:   testData.Input,
					Output:  errMsg,
				}}, nil
			} else {
				return entities.TestCases{}, fmt.Errorf("internal error: %w", err)
			}
		}
		results = append(results, entities.TestCase{
			TestNum: testData.RunNum,
			Input:   testData.Input,
			Output:  out,
		})
	}
	return results, nil
}
