package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"reflect"
	"strconv"
	"syscall"

	"gopkg.in/yaml.v2"
)

// func main() {
// 	var cl Callable
// 	reflect.ValueOf(&cl).MethodByName("HELLOWORLD").Call([]reflect.Value{})
// 	// fnc := reflect.ValueOf(&met).MethodByName("helloworld")
// 	// rfl := reflect.ValueOf(fnc)
// 	// fnc.Call([]reflect.Value{})
// }

// package main

// import (
// 	"fmt"
// 	"log"
// 	"os"
// 	"os/exec"
// 	"reflect"
// 	"syscall"

// 	"gopkg.in/yaml.v2"
// )

type Callable struct{}

var cal Callable
var rCall = reflect.ValueOf(&cal)

type Function struct {
	Func        string            `yaml:"func"`
	FailOnError bool              `yaml:"failOnError"`
	Vars        map[string]string `yaml:"vars"`
}

type UserFunctions struct {
	UID       int        `yaml:"uid"`
	Functions []Function `yaml:"functions"`
}

type Configuration struct {
	Runbook []UserFunctions `yaml:"runbook"`
}

func parseVars(s interface{}, vars map[string]string) interface{} {
	v := reflect.ValueOf(s).Elem()

	for i := 0; i < v.NumField(); i++ {
		fieldName := v.Type().Field(i).Name
		fieldValue := v.Field(i)

		if value, ok := vars[fieldName]; ok {
			switch fieldValue.Kind() {
			case reflect.String:
				fieldValue.SetString(value)
			case reflect.Int:
				intValue, err := strconv.Atoi(value)
				if err == nil {
					fieldValue.SetInt(int64(intValue))
				}
			case reflect.Bool:
				boolValue, err := strconv.ParseBool(value)
				if err == nil {
					fieldValue.SetBool(boolValue)
				}
			}
		}
	}

	return s
}

func runFunc(fName string, fVars map[string]string) error {

	method := rCall.MethodByName(fName)
	args := []reflect.Value{
		reflect.ValueOf(fVars),
	}

	retn := method.Call(args)

	// Return error if any
	if len(retn) == 0 {
		return nil
	}

	return retn[0].Interface().(error)
}

func loadConfiguration() (*Configuration, error) {
	// Load the configuration from the CONFIG environment variable
	configLocation := os.Getenv("CONFIG_LOCATION")
	if configLocation == "" {
		configLocation = "/init-go/config.yaml"
	}

	// Read the configuration file
	configData, err := ioutil.ReadFile(configLocation)
	if err != nil {
		return nil, fmt.Errorf("failed to read configuration file: %w", err)
	}

	// Unmarshal the YAML data into the Configuration struct
	var config Configuration
	err = yaml.Unmarshal([]byte(configData), &config)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal YAML: %w", err)
	}

	return &config, nil
}

func restartAsUser(uid int) error {
	args := os.Args
	args[0], _ = exec.LookPath(args[0])

	cmd := &exec.Cmd{
		Path:   args[0],
		Args:   args,
		Env:    os.Environ(),
		Stdout: os.Stdout,
		Stderr: os.Stderr,
		SysProcAttr: &syscall.SysProcAttr{
			Credential: &syscall.Credential{Uid: uint32(uid)},
		},
	}

	err := cmd.Start()
	if err != nil {
		return fmt.Errorf("failed to start subprocess as user %d: %s", uid, err)
	}
	err = cmd.Wait()
	if err != nil {
		return fmt.Errorf("subprocess as user %d exited with error: %s", uid, err)
	}

	return nil
}

func main() {
	// Load the configuration file
	config, err := loadConfiguration()
	if err != nil {
		log.Fatalf("Failed to load configuration: %s", err)
	}

	// Determine the current user
	uid := os.Geteuid()

	for _, user := range config.Runbook {

		if user.UID != uid {
			if int(user.UID) != 0 {
				continue
			}
			err := restartAsUser(user.UID)
			if err != nil {
				log.Fatalf("Failed to restart as user %d: %s", user.UID, err)
			}
			continue
		}

		for _, function := range user.Functions {
			err := runFunc(function.Func, function.Vars)
			if err != nil && function.FailOnError {
				log.Fatalf("Error running function %s: %s", function.Func, err)
			} else if err != nil {
				log.Printf("Error running function %s: %s", function.Func, err)
			}
		}
	}
	// Find the correct section of the runbook for this user
	// functions := findFunctions(config.Runbook, uid)

	// // Run each function sequentially
	// for _, function := range functions {
	// 	err := runFunc(function.Func, function.Vars)
	// 	if err != nil && function.FailOnError {
	// 		log.Fatalf("Error running function %s: %s", function.Func, err)
	// 	} else if err != nil {
	// 		log.Printf("Error running function %s: %s", function.Func, err)
	// 	}
	// }

	// // If there are more users in the runbook, restart the program as the next user
	// if len(config.Runbook) > 0 {
	// 	nextUser := config.Runbook[0].UID
	// 	config.Runbook = config.Runbook[1:]
	// 	restartAsUser(nextUser, config)
	// }
}
