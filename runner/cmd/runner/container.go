package main

import (
	"runner/internal/application/interfaces"
	usecases "runner/internal/application/use_cases"
	implementations "runner/internal/infrastructure"
)

func newCodeRunner() interfaces.Runner {
	return &implementations.CodeRunner{}
}

func NewRunCodeUseCase() *usecases.TestSolutionUseCase {
	return &usecases.TestSolutionUseCase{
		Runner: newCodeRunner(),
	}
}
