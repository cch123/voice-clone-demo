package main

import (
	"fmt"
	"os"
	"os/signal"
	"sync"

	"github.com/gordonklaus/portaudio"
	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
)

const sampleRate = 16000

func main() {
	portaudio.Initialize()
	defer portaudio.Terminate()

	in := make([]int16, 1024)
	audioBuffer := &audio.IntBuffer{
		Format: &audio.Format{
			NumChannels: 1,
			SampleRate:  sampleRate,
		},
		SourceBitDepth: 16,
	}

	callback := func(in, out []int16) {
		intData := make([]int, len(in))
		for i, v := range in {
			intData[i] = int(v)
		}
		audioBuffer.Data = append(audioBuffer.Data, intData...)
	}

	stream, err := portaudio.OpenDefaultStream(1, 0, sampleRate, len(in), callback)
	if err != nil {
		panic(fmt.Sprintf("Failed to open default stream: %v", err))
	}
	defer stream.Close()

	err = stream.Start()
	if err != nil {
		panic(fmt.Sprintf("Failed to start stream: %v", err))
	}

	wg := &sync.WaitGroup{}
	wg.Add(1)

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)

	go func() {
		defer wg.Done()
		<-c
	}()

	wg.Wait()
	err = stream.Stop()
	if err != nil {
		panic(fmt.Sprintf("Failed to stop stream: %v", err))
	}

	outputFile, err := os.Create("audio.wav")
	if err != nil {
		panic(fmt.Sprintf("Failed to create output file: %v", err))
	}
	defer outputFile.Close()

	wavEncoder := wav.NewEncoder(outputFile, sampleRate, 16, 1, 1)
	err = wavEncoder.Write(audioBuffer)
	if err != nil {
		panic(fmt.Sprintf("Failed to write output file: %v", err))
	}

	wavEncoder.Close()
	fmt.Println("Recording saved to output.wav.")
}

