package main

import (
	"bytes"
	"fmt"
	"os/exec"
)

var SHVAR_RUN_COMMAND struct {
	command        string
	expectedOutput string
}

func (cl *Callable) SH_RUN_COMMAND(vars map[string]string) {
	parsedVars := &SHVAR_RUN_COMMAND
	parseVars(parsedVars, vars)
	fmt.Println(parsedVars)

	cmd := exec.Command("sh", "-c", parsedVars.command)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()

	output := fmt.Sprintf("%s%s", stdout.String(), stderr.String())
	if err != nil || !bytes.Contains([]byte(output), []byte(parsedVars.expectedOutput)) {
		panic(fmt.Errorf("expected output: %q, actual output: %q", parsedVars.expectedOutput, output))
	}
	fmt.Println(output)
}
