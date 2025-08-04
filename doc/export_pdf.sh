curl -X POST http://127.0.0.1:8000/tools/call/export  \
-H "Accept: application/pdf" \
-F "file=@git.md"

# this will return a json with the URL to the PDF file
# {"status_url":"/jobs/f4f6c37728c8ad321f05de1d4d026867f59bc28eec52777f1f485df7c975208d"}