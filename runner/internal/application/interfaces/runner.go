package interfaces

import (
	"runner/internal/application/dto"
	"runner/internal/domain/entities"
)

// Runner is interface for structs able to run code directly via Runner.Run and return result
type Runner interface {
	// Run runs program wrote in src
	Run(testsData []dto.RunData, src *string, lang string) (entities.TestCases, error)
}
