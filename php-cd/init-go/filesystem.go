package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/cheggaaa/pb"
)

var FSVAR_LISTDIR struct {
	path string
}

func (cl *Callable) FS_LISTDIR(vars map[string]string) {
	parsedVars := &FSVAR_LISTDIR
	parseVars(parsedVars, vars)
	fmt.Println(parsedVars)

	// List files in directory
	dir, err := os.Open(parsedVars.path)
	if err != nil {
		log.Fatal(err)
	}
	defer dir.Close()
	files, err := dir.Readdir(-1)
	if err != nil {
		log.Fatal(err)
	}
	for _, file := range files {
		fmt.Println(file.Name())
	}
}

var FSVAR_DOWNLOAD_FILE struct {
	Url  string
	Path string
}

func (cl *Callable) FS_DOWNLOAD_FILE(vars map[string]string) {
	parsedVars := &FSVAR_DOWNLOAD_FILE
	parseVars(parsedVars, vars)
	fmt.Println(parsedVars)

	// Create the file
	out, err := os.Create(parsedVars.Path)
	if err != nil {
		panic(err)
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(parsedVars.Url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("bad status: %s", resp.Status))
	}

	// Writer the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		panic(err)
	}
}

var FSVAR_COPY_DIR struct {
	source      string
	destination string
}

func (cl *Callable) FS_COPY_DIR(vars map[string]string) {
	parsedVars := &FSVAR_COPY_DIR
	parseVars(parsedVars, vars)
	fmt.Println(parsedVars)

	// Open source directory
	srcInfo, err := os.Stat(src)
	if err != nil {
		return err
	}
	if !srcInfo.IsDir() {
		return fmt.Errorf("%s is not a directory", src)
	}

	// Create destination directory
	err = os.MkdirAll(dst, srcInfo.Mode())
	if err != nil {
		return err
	}

	// Get list of files in source directory
	files, err := os.ReadDir(src)
	if err != nil {
		return err
	}

	// Set up progress bar
	bar := pb.StartNew(len(files))
	defer bar.Finish()

	// Copy each file to the destination directory
	for _, file := range files {
		srcFile := filepath.Join(src, file.Name())
		dstFile := filepath.Join(dst, file.Name())

		if file.IsDir() {
			// Recursively copy directory
			err = copyDir(srcFile, dstFile)
			if err != nil {
				return err
			}
		} else {
			// Copy file
			err = copyFile(srcFile, dstFile, bar)
			if err != nil {
				return err
			}
		}
	}

	return nil
}

func copyFile(src string, dst string, bar *pb.ProgressBar) error {
	// Open source file
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	// Create destination file
	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	// Copy file
	_, err = io.Copy(dstFile, srcFile)
	if err != nil {
		return err
	}

	// Update progress bar
	bar.Increment()

	return nil
}
