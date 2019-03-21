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

function delayedOutput() {
	sleep 1
	echo 'did a thing'
	sleep 1
	echo 'did another thing'
	sleep 1
	echo 'did a final thing'
}