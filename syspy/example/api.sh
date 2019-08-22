hr="${PWD}"
testLoc="${hr}/example/testFolder"
other="${testLoc}/other.txt"

function gitStatus() {
	git status
}

function copyFile() {
	echo 'Copying file.txt'
	cp "${1}" "${2}"
}

function delayedOutput() {
	sleep 1
	echo 'did a thing'
	sleep 1
	ftdd # this is designed to fail
	sleep 1
	echo 'did a final thing'
}