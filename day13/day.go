package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func encodeCoords(xy []int) string {
	res := string(rune(xy[0])) + "," + string(rune(xy[1]))
	return res
}

func removeDups(slice [][]int) [][]int {
	keys := make(map[string]bool)
	// list := make([][]int, len(slice))
	list := [][]int{}
	new_i := 0

	for _, el := range slice {
		entry := encodeCoords(el)
		_, present := keys[entry]
		if !present {
			keys[entry] = true
			// list[new_i] = []int{el[0], el[1]}
			list = append(list, el)
			new_i++
			continue
		}
	}
	return list
}

func countLines(lines []string) int {
	length := 0
	for _, line := range lines {
		if len(line) <= 1 {
			break
		}
		length++
	}
	return length
}

func findMax(list [][]int) []int {
	max := make([]int, 2)
	for _, el := range list {
		if el[0] > max[0] {
			max[0] = el[0] + 1
		}
		if el[1] > max[1] {
			max[1] = el[1] + 1
		}
	}
	return max
}

func fold(line string, list [][]int) {
	axis := 1
	if line[11] == 'x' {
		axis = 0
	}
	fold, _ := strconv.Atoi(line[13:])
	for _, el := range list {

		if el[axis] > fold {
			el[axis] = fold - (el[axis] - fold)
		}
	}
}

func main() {
	data, err := os.ReadFile("./input")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(data), "\n")
	list := make([][]int, countLines(lines))
	for i := range list {
		list[i] = make([]int, 2)
	}
	coords := true
	for i, line := range lines {
		if len(line) <= 1 {
			coords = false
			continue
		}
		if coords {

			xy := strings.Split(line, ",")
			list[i][0], _ = strconv.Atoi(xy[0])
			list[i][1], _ = strconv.Atoi(xy[1])
			continue
		}
		fold(line, list)
		list = removeDups(list)
		fmt.Println("fold ", len(list))
	}
	max := findMax(list)
	paper := make([][]bool, max[0])
	for i := range paper {
		paper[i] = make([]bool, max[1])
	}
	for _, el := range list {
		paper[el[0]][el[1]] = true
	}
	res := []byte{}
	for _, col := range paper {
		for _, cell := range col {
			if cell {
				res = append(res, '#')
				continue
			}
			res = append(res, ' ')
		}
		res = append(res, '\n')
	}
	os.Stdout.Write(res)
}
