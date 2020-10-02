package main

import (
	"fmt"
	"github.com/fogleman/gg"
	"os"
	"sync"
)

var plotmutex = &sync.Mutex{}

type plotter_basics struct{

	dc *gg.Context

}

const w = 1024
const h = 800

var plotterBase plotter_basics

func inializePlotter(){
	plotterBase.dc = gg.NewContext(w,h);
	plotterBase.dc.SetRGB(0, 0, 0)
}

func print(systime string){

	plotmutex.Lock()

	plotterBase.dc = gg.NewContext(w,h);
	plotterBase.dc.SetRGB(0, 0, 0)

	plotterBase.dc.LoadFontFace("/Library/Fonts/Arial.ttf", 40)

	pixellength,_ := plotterBase.dc.MeasureString(systime)
	printx := w -  (w / 2) - pixellength/2 ;

	plotterBase.dc.DrawString(systime,float64(printx), h - h/2 )

	// rename old file, which then can be consumed as we write to the new file.
	oldfilepath := "./printer/plot.png"
	newfilepath := "./printer/plot1.png"
	fmt.Println(oldfilepath)

	var _, err = os.Stat(oldfilepath)

	// create file if not exists
	if os.IsNotExist(err) == false {
		//os.Remove(newfilepath) // might have to a check here
		os.Rename(oldfilepath,newfilepath)
		//os.Remove(oldfilepath) // likewise
	}
	err = plotterBase.dc.SavePNG(oldfilepath)

	if (err != nil) {
		panic(err)
		fmt.Println(err.Error())
	}

	plotmutex.Unlock()

}