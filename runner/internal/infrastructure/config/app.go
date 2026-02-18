package config

import (
	"errors"
	"os"
)

type appConfig struct {
	Language       string
	TmpNamePattern string
}

func (conf *appConfig) parse() error {
	lang := os.Getenv("LANG")
	if lang == "" {
		return errors.New("run error: undefined programming language")
	}
	conf.Language = lang
	return nil
}

var AppConfig = appConfig{
	TmpNamePattern: "runlet-*.%s",
}
