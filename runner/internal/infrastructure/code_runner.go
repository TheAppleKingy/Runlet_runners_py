package infrastructure

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"os/exec"
	"runner/internal/application/dto"
	"runner/internal/domain"
	"runner/internal/domain/entities"
	"strings"
	"time"
)

// CodeRunner is implementation of interfaces.Runner
type CodeRunner struct {
	RunArgs        domain.RunArgsType
	CompileArgs    domain.CompileArgsType
	SrcPlaceHolder string
	BinPlaceholder string
	Lang           string
}

// compile compiles binary based on src via lang compilator and returns name of binary file or provided src if language is interpreted
func (cr CodeRunner) compile(src *string) error {
	if len(cr.CompileArgs) == 0 {
		return nil
	}
	binaryName := strings.TrimSuffix(*src, "."+cr.Lang)
	compileArgs := make([]string, len(cr.CompileArgs))
	for i, arg := range cr.CompileArgs {
		switch {
		case strings.Contains(arg, cr.SrcPlaceHolder):
			compileArgs[i] = strings.ReplaceAll(arg, cr.SrcPlaceHolder, *src)
		case strings.Contains(arg, cr.BinPlaceholder):
			compileArgs[i] = strings.ReplaceAll(arg, cr.BinPlaceholder, binaryName)
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
			return fmt.Errorf("unable to compile '%s' code: %s", cr.Lang, errMsg)
		}
		return fmt.Errorf("unable to compile '%s' code: %w", cr.Lang, err)
	}
	os.Remove(*src)
	*src = binaryName
	return nil
}

func (cr CodeRunner) Run(
	runData *[]dto.RunData,
	src *string,
	runTimeout int,
) (entities.TestCases, error) {
	var results entities.TestCases
	if err := cr.compile(src); err != nil {
		return entities.TestCases{}, fmt.Errorf("internal error: %w", err)
	}
	runArgs := make([]string, len(cr.RunArgs))
	for i, arg := range cr.RunArgs {
		runArgs[i] = strings.ReplaceAll(arg, cr.SrcPlaceHolder, *src)
	}
	timeout := time.Duration(runTimeout) * time.Second
	for _, testData := range *runData {
		ctx, cancel := context.WithTimeout(context.Background(), timeout)
		defer cancel()
		cmd := exec.CommandContext(ctx, runArgs[0], runArgs[1:]...)
		var stdout, stderr bytes.Buffer
		cmd.Stdout = &stdout
		cmd.Stderr = &stderr
		cmd.Stdin = bytes.NewBufferString(testData.Input)
		err := cmd.Run()
		out := strings.TrimRight(stdout.String(), "\n")
		errMsg := strings.TrimRight(stderr.String(), "\n")
		if ctx.Err() == context.DeadlineExceeded {
			return entities.TestCases{{
				TestNum: testData.RunNum,
				Input:   testData.Input,
				Output:  "timeout exceeded",
			}}, nil
		}
		if err != nil {
			out = "internal error"
			resultErr := err
			if errMsg != "" {
				out = errMsg
				resultErr = nil
			} else {
				resultErr = fmt.Errorf("internal error: %w", err)
			}
			return entities.TestCases{{
				TestNum: testData.RunNum,
				Input:   testData.Input,
				Output:  out,
			}}, resultErr
		}
		results = append(results, entities.TestCase{
			TestNum: testData.RunNum,
			Input:   testData.Input,
			Output:  out,
		})
	}
	return results, nil
}
