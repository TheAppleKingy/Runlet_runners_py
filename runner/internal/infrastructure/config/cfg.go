package config

type config interface {
	parse() error
}

func LoadConfigs() error {
	configs := []config{
		&AppConfig,
	}
	for _, cfg := range configs {
		if err := cfg.parse(); err != nil {
			return err
		}
	}
	return nil
}
