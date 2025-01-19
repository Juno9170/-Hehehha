import { useEffect, useState, useRef } from "react";
import { useAudioRecorder, AudioRecorder } from "react-audio-voice-recorder";
import { io, Socket } from "socket.io-client";
import "./Voice.css";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Button } from "./ui/button";
import { Trash, Mic, Download, Wand } from "lucide-react";
type AudioRecorderWithVisualizerProps = {
  onFinish?: () => void;
  titleString:string;
};

const host = "http://localhost:5050/";
const socket: Socket = io(host);

export default function AudioRecorderWithVisualizer({ onFinish, titleString }: AudioRecorderWithVisualizerProps) {
  const recorderControls = useAudioRecorder();

  const [audioUrl, setAudioUrl] = useState<string>("");
  const [audioKey, setAudioKey] = useState<number>(Date.now());
  const cancelled = useRef<boolean>(false);
  const [isReady, setIsReady] = useState<boolean>(true);

  const handleStopRecording = () => {
    recorderControls.stopRecording();
  };

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to WebSocket server");
    });

    socket.on("transcription", (data: { text: string }) => {
      console.log("Transcription:", data.text);
      // Optionally update the UI to show the transcription
    });

    socket.on("response", (data: { text: string }) => {
      console.log("Response Text:", data.text);
      // Optionally update the UI to show the response text
    });

    socket.on("audio_url", (data: { url: string }) => {
      setAudioUrl(host + data.url);
      setAudioKey(Date.now()); // Update the key to force refresh
      console.log("Received audio URL:", host + data.url);
      // Handle playing the received audio URL here
    });

    return () => {
      socket.off("connect");
      socket.off("transcription");
      socket.off("response");
      socket.off("audio_url");
    };
  }, []);

  useEffect(() => {
    if (recorderControls.isRecording) {
      setAudioUrl("");
    }
  }, [recorderControls.isRecording]);

  useEffect(() => {
    if (recorderControls.recordingBlob && !cancelled.current) {
      console.log("Sending audio blob to the server", recorderControls.recordingBlob);
      const reader = new FileReader();
      reader.onload = function (event) {
        const arrayBuffer = event.target?.result as ArrayBuffer;
        socket.emit("audio_data", {arrayBuffer, additionalString:titleString} );
      };

      reader.readAsArrayBuffer(recorderControls.recordingBlob);

      // Trigger onFinish callback after recording is processed
      if (onFinish) {
        onFinish();
      }
    }
  }, [recorderControls.recordingBlob, onFinish]);

  return (
    <div className=" flex flex-col items-center ">
      <AudioRecorder
        onRecordingComplete={(blob) => handleStopRecording()}
        recorderControls={recorderControls}
        showVisualizer={true}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
        }}
      />
      <div className="flex gap-5 justify-center">
        {/* ========== Delete recording button ========== */}
        {recorderControls.isRecording ? (
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                onClick={()=>{cancelled.current = true; setIsReady(true); handleStopRecording()}}
                size={"icon"}
                variant={"default"}
                className="mt-5 bg-[#D282A6] hover:bg-[#c76c95] rounded-xl"
              >
                <Trash size={15} />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="bottom" sideOffset={3}>
              <span> Reset recording</span>
            </TooltipContent>
          </Tooltip>
        ) : null}

        {/* ========== Start and send recording button ========== */}
        <Tooltip>
          <TooltipTrigger asChild>
            {!recorderControls.isRecording ? (
                <div className="flex flex-col items-center gap-4 font-semibold text-xl">
                    <div className={`${isReady ? "block" : "invisible"}`}>
                        Start Recording
                    </div>
                    <Button onClick={() => {recorderControls.startRecording(); setIsReady(false)}} size={"icon"} className="bg-[#F5E3E0] hover:bg-[#D282A6] active:bg-[#c76c95] rounded-xl">
                        <Mic size={15} /> 
                    </Button>
                </div>
            ) : (
              <Button onClick={() => {cancelled.current = false; handleStopRecording(); setIsReady(true) } } size={"icon"} className="mt-5 bg-[#F5E3E0] hover:bg-[#ffbc9f] rounded-xl">
                <Wand size={15} />
              </Button>
            )}
          </TooltipTrigger>
          <TooltipContent side="bottom" className="m-2" sideOffset={-3}>
            <span>
              {" "}
              {!recorderControls.isRecording ? "Start recording" : "Analyse"}{" "}
            </span>
          </TooltipContent>
        </Tooltip>
      </div>
    </div>
  );
}
