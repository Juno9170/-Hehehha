<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Tooltip, TooltipContent, TooltipTrigger } from "../../lib/components/ui/tooltip";
    import { Download, Mic, Trash } from "lucide-svelte";
    import { onMount, onDestroy } from "svelte";
    // import { useTheme } from "next-themes";
  
    type Record = {
      id: number;
      name: string;
      file: any;
    };
  
    let recorder: MediaRecorder;
    let recordingChunks: BlobPart[] = [];
    let timerTimeout: ReturnType<typeof setTimeout>;
  
    let isRecording = false;
    let isRecordingFinished = false;
    let timer = 0;
    let currentRecord: Record = {
      id: -1,
      name: "",
      file: null,
    };
  
    let canvasRef: HTMLCanvasElement;
    let animationRef: any;
  
    // Utility function to pad a number with leading zeros
    const padWithLeadingZeros = (num: number, length: number): string => {
      return String(num).padStart(length, "0");
    };
  
    // Utility function to download a blob
    const downloadBlob = (blob: Blob) => {
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = `Audio_${new Date().getMilliseconds()}.mp3`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    };
  
    const startRecording = async () => {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          isRecording = true;
  
          const AudioContext = window.AudioContext;
          const audioCtx = new AudioContext();
          const analyser = audioCtx.createAnalyser();
          const source = audioCtx.createMediaStreamSource(stream);
          source.connect(analyser);
  
          const mimeType = MediaRecorder.isTypeSupported("audio/mpeg")
            ? "audio/mpeg"
            : MediaRecorder.isTypeSupported("audio/webm")
            ? "audio/webm"
            : "audio/wav";
  
          const options = { mimeType };
          recorder = new MediaRecorder(stream, options);
          recorder.start();
          recordingChunks = [];
  
          recorder.ondataavailable = (e) => {
            recordingChunks.push(e.data);
          };
  
          recorder.onstop = () => {
            const recordBlob = new Blob(recordingChunks, { type: "audio/wav" });
            downloadBlob(recordBlob);
            currentRecord = { ...currentRecord, file: window.URL.createObjectURL(recordBlob) };
            recordingChunks = [];
          };
        } catch (error) {
          alert(error);
          console.log(error);
        }
      }
    };
  
    const stopRecording = () => {
      recorder.stop();
      isRecording = false;
      isRecordingFinished = true;
      timer = 0;
      clearTimeout(timerTimeout);
    };
  
    const resetRecording = () => {
      recorder.stop();
      isRecording = false;
      isRecordingFinished = true;
      timer = 0;
      clearTimeout(timerTimeout);
  
      // Clear the animation frame and canvas
      cancelAnimationFrame(animationRef);
      if (canvasRef) {
        const canvasCtx = canvasRef.getContext("2d");
        if (canvasCtx) {
          const WIDTH = canvasRef.width;
          const HEIGHT = canvasRef.height;
          canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);
        }
      }
    };
  
    const handleSubmit = () => {
      stopRecording();
    };
  
    // Effect to update the timer every second
    onMount(() => {
      if (isRecording) {
        timerTimeout = setTimeout(() => {
          timer += 1;
        }, 1000);
      }
    });
  
    onDestroy(() => {
      clearTimeout(timerTimeout);
    });
  
    // Visualizer
    const visualizeVolume = () => {
      if (!canvasRef) return;
  
      const canvasCtx = canvasRef.getContext("2d");
      const WIDTH = canvasRef.width;
      const HEIGHT = canvasRef.height;
  
      const drawWaveform = (dataArray: Uint8Array) => {
        if (!canvasCtx) return;
        canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);
        canvasCtx.fillStyle = "#939393";
  
        const barWidth = 1;
        const spacing = 1;
        const maxBarHeight = HEIGHT / 2.5;
        const numBars = Math.floor(WIDTH / (barWidth + spacing));
  
        for (let i = 0; i < numBars; i++) {
          const barHeight = Math.pow(dataArray[i] / 128.0, 8) * maxBarHeight;
          const x = (barWidth + spacing) * i;
          const y = HEIGHT / 2 - barHeight / 2;
          canvasCtx.fillRect(x, y, barWidth, barHeight);
        }
      };
  
      const draw = () => {
        if (!isRecording) {
          cancelAnimationFrame(animationRef);
          return;
        }
        animationRef = requestAnimationFrame(draw);
        // Replace with audio data fetching logic
        const dataArray = new Uint8Array(256);
        drawWaveform(dataArray);
      };
  
      draw();
    };
  
    // Timer formatting
    const hours = Math.floor(timer / 3600);
    const minutes = Math.floor((timer % 3600) / 60);
    const seconds = timer % 60;
  
    const [hourLeft, hourRight] = padWithLeadingZeros(hours, 2).split("");
    const [minuteLeft, minuteRight] = padWithLeadingZeros(minutes, 2).split("");
    const [secondLeft, secondRight] = padWithLeadingZeros(seconds, 2).split("");
  </script>
  
  <div class="bg-black flex h-16 rounded-md relative w-full items-center justify-center gap-2 max-w-5xl {isRecording ? 'border p-1' : 'border-none p-0'}">
    {#if isRecording}
      <div class="items-center -top-12 left-0 absolute justify-center gap-0.5 border p-1.5 rounded-md font-mono font-medium text-foreground flex">
        <span class="rounded-md bg-background p-0.5 text-foreground">{hourLeft}</span>
        <span class="rounded-md bg-background p-0.5 text-foreground">{hourRight}</span>
        <span>:</span>
        <span class="rounded-md bg-background p-0.5 text-foreground">{minuteLeft}</span>
        <span class="rounded-md bg-background p-0.5 text-foreground">{minuteRight}</span>
        <span>:</span>
        <span class="rounded-md bg-background p-0.5 text-foreground">{secondLeft}</span>
        <span class="rounded-md bg-background p-0.5 text-foreground">{secondRight}</span>
      </div>
    {/if}
    
    <canvas bind:this={canvasRef} class="h-full w-full bg-black {isRecording ? 'flex' : 'hidden'}" />
  
    <div class="flex gap-2">
      {#if isRecording}
        <Tooltip>
          <TooltipTrigger>
            <Button on:click={resetRecording} size="icon" variant="destructive">
              <Trash size={15} />
            </Button>
          </TooltipTrigger>
          <TooltipContent class="m-2">
            <span> Reset recording</span>
          </TooltipContent>
        </Tooltip>
      {/if}
  
      <Tooltip>
        <TooltipTrigger>
          {#if !isRecording}
            <Button on:click={startRecording} size="icon">
              <Mic size={15} />
            </Button>
          {:else}
            <Button on:click={handleSubmit} size="icon">
              <Download size={15} />
            </Button>
          {/if}
        </TooltipTrigger>
        <TooltipContent class="m-2">
          <span> {!isRecording ? "Start recording" : "Download recording"} </span>
        </TooltipContent>
      </Tooltip>
    </div>
  </div>
  