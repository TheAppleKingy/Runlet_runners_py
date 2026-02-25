package main

import (
	usecases "runner/internal/application/use_cases"
	"runner/internal/domain"
	"runner/internal/infrastructure"
	implementations "runner/internal/infrastructure"
)

func NewCodeRunner(
	runArgs domain.RunArgsType,
	compileArgs domain.CompileArgsType,
	srcPlaceholder string,
	binPlaceholder string,
	lang string,
	tmpfs string,
) *infrastructure.CodeRunner {
	return &implementations.CodeRunner{
		RunArgs:        runArgs,
		CompileArgs:    compileArgs,
		SrcPlaceHolder: srcPlaceholder,
		BinPlaceholder: binPlaceholder,
		Lang:           lang,
		Tmpfs:          tmpfs,
	}
}

func NewRunCodeUseCase(runner *infrastructure.CodeRunner) *usecases.TestSolutionUseCase {
	return &usecases.TestSolutionUseCase{
		Runner: runner,
	}
}
