package usecases

import (
	"fmt"
	"os"
	"runner/internal/application/dto"
	"runner/internal/domain/entities"
	"runner/internal/infrastructure"
	"runner/internal/infrastructure/config"
)

// writeTemp creates and returns pointer to temporary file containing code for running
func writeTemp(lang string, code *string, dir string) (*os.File, error) {
	tmpFile, err := os.CreateTemp(dir, fmt.Sprintf(config.AppConfig.TmpNamePattern, lang))
	if err != nil {
		return nil, err
	}
	defer tmpFile.Close()
	_, err = tmpFile.WriteString(*code)
	if err != nil {
		os.Remove(tmpFile.Name())
		return nil, fmt.Errorf("unable to save code to tempfile: %w", err)
	}
	return tmpFile, nil
}

type TestSolutionUseCase struct {
	Runner *infrastructure.CodeRunner
}

func (uc TestSolutionUseCase) TestSolution(dto *dto.IncomingData, runTimeout int) (*entities.TestCases, error) {
	f, err := writeTemp(uc.Runner.Lang, dto.Code, uc.Runner.Tmpfs)
	if err != nil {
		return &entities.TestCases{}, fmt.Errorf("internal error: %w", err)
	}
	toExec := f.Name()
	defer func() {
		os.Remove(toExec)
	}()

	results, err := uc.Runner.Run(dto.RunData, &toExec, runTimeout)
	return &results, err
}
