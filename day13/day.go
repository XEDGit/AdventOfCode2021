package main

import (
	"fmt"
	"net/http"
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
	list := [][]int{}
	new_i := 0

	for _, el := range slice {
		entry := encodeCoords(el)
		_, present := keys[entry]
		if !present {
			keys[entry] = true
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

func getFold(line string) (int, int) {
	if line == "" {
		return 2, 0
	}
	axis := 0
	if line[11] == 'x' {
		axis = 1
	}
	fold, _ := strconv.Atoi(line[13:])
	return axis, fold
}

func fold(line string, list [][]int) {
	axis, fold := getFold(line)
	for _, el := range list {

		if el[axis] > fold {
			el[axis] = fold - (el[axis] - fold)
		}
	}
}

var target_i = 0

func messageHandler(w http.ResponseWriter, r *http.Request) {
	init := false
	coords := false
	lines := []string{}
	list := [][]int{}
	if !init {

		data, err := os.ReadFile("./input")
		if err != nil {
			panic(err)
		}
		lines = strings.Split(string(data), "\n")
		list = make([][]int, countLines(lines))
		for i := range list {
			list[i] = make([]int, 2)
		}
		coords = true
	}
	last_line := ""
	for i, line := range lines {
		if len(line) <= 1 {
			coords = false
			if target_i == 0 {
				target_i = i + 1
			}
			continue
		}
		if coords {

			xy := strings.Split(line, ",")
			list[i][1], _ = strconv.Atoi(xy[0])
			list[i][0], _ = strconv.Atoi(xy[1])
			continue
		}
		fold(line, list)
		list = removeDups(list)
		if i == target_i {
			target_i++
			last_line = lines[i+1]
			break
		}
	}
	if target_i == len(lines)-1 {
		target_i = 0
	}
	fmt.Fprint(w, "<h1>Paper folder</h1>\n\n<h4>"+last_line+"</h4>\n<tt style=\"white-space: pre-wrap;\">"+string(show(list, last_line))+"</tt>")
}

func show(list [][]int, line string) []byte {
	max := findMax(list)
	paper := make([][]bool, max[0]+1)
	for i := range paper {
		paper[i] = make([]bool, max[1]+1)
	}
	for _, el := range list {
		paper[el[0]][el[1]] = true
	}
	axis, fold := getFold(line)
	res := []byte{}
	for y, col := range paper {
		for x, cell := range col {
			if axis == 0 && y == fold-1 {
				res = append(res, '-')
				continue
			} else if axis == 1 && x == fold-1 {
				res = append(res, '|')
				continue
			}
			if cell {
				res = append(res, '#')
				continue
			}
			res = append(res, ' ')
		}
		res = append(res, '\n')
	}
	return res
}

func main() {
	mux := http.NewServeMux()
	// Convert the messageHandler function to a HandlerFunc type
	mh := http.HandlerFunc(messageHandler)
	mux.Handle("/", mh)
	http.ListenAndServe(":8080", mux)
}
