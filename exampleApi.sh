hr="${PWD}"
testLoc="${hr}/testFolder"
toCopy="${testLoc}/file.txt"
other="${testLoc}/other.txt"

function gitStatus() {
	git status
}

function copyFile() {
	echo 'Copying file.txt'
	cp "${toCopy}" "${@}"
}

function falseCommand() {
	ftdd
}