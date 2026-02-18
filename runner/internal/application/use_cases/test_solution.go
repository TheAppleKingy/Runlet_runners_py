package usecases

import (
	"fmt"
	"os"
	"runner/internal/application/dto"
	"runner/internal/application/interfaces"
	"runner/internal/domain/entities"
	"runner/internal/infrastructure/config"
)

// writeTemp creates and returns pointer to temporary file containing code for running
func writeTemp(lang string, code *string) (*os.File, error) {
	tmpFile, err := os.CreateTemp("", fmt.Sprintf(config.AppConfig.TmpNamePattern, lang))
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
	Runner interfaces.Runner
}

func (rs TestSolutionUseCase) TestSolution(testsData []dto.RunData, lang string, code *string) (entities.TestCases, error) {
	f, err := writeTemp(lang, code)
	if err != nil {
		return entities.TestCases{}, fmt.Errorf("internal error: %w", err)
	}
	toExec := f.Name()
	defer func() {
		os.Remove(toExec)
	}()

	results, err := rs.Runner.Run(testsData, &toExec, lang)
	return results, err
}
