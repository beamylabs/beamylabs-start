package utils


import (
	"net/http"
)

func ServePrinter() {
	http.Handle("/",http.FileServer(http.Dir("./printer")));
	http.ListenAndServe(":9000", nil)
}

