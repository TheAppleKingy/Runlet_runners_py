package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type languageConfig struct {
	CompileCommandArgs []string `yaml:"compile"`
	RunCommandArgs     []string `yaml:"run"`
}

type languagesConfig struct {
	Languages      map[string]languageConfig `yaml:"languages"`
	SrcPlaceholder string                    `yaml:"src_placeholder"`
	BinPlaceholder string                    `yaml:"bin_placeholder"`
}

func (cfg *languagesConfig) parse() error {
	path := os.Getenv("LANGS_CONF_PATH")
	if path == "" {
		return fmt.Errorf("internal error: undefined config path")
	}

	confData, err := os.ReadFile(path)
	if err != nil {
		return fmt.Errorf("internal error: %w", err)
	}

	if err := yaml.Unmarshal(confData, cfg); err != nil {
		return fmt.Errorf("internal error: %w", err)
	}
	return nil
}

var LaunguagesConfig = languagesConfig{}
