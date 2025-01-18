<script lang="ts">
    import { Button } from "@/ui/button";
    import { Textarea } from "@/ui/textarea";
  
    let recording: boolean = false;
    let recorder: MediaRecorder | null = null;
    let audioBlob: Blob | null = null;
    let apiResponse: string = '';
    let mediaStream: MediaStream | null = null;
  
    const startRecording = async (): Promise<void> => {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(mediaStream);
  
        const chunks: Blob[] = [];
        recorder.ondataavailable = (event: BlobEvent) => chunks.push(event.data);
        recorder.onstop = async () => {
          audioBlob = new Blob(chunks, { type: 'audio/wav' });
          await sendToAPI(audioBlob);
        };
  
        recorder.start();
        recording = true;
      } catch (err) {
        console.error('Error accessing microphone:', err);
        alert('Could not access microphone. Please allow microphone access.');
      }
    };
  
    const stopRecording = (): void => {
      if (recorder && mediaStream) {
        recorder.stop();
        mediaStream.getTracks().forEach((track) => track.stop());
        recording = false;
      }
    };
  
    const toggleRecording = (): void => {
      if (recording) {
        stopRecording();
      } else {
        startRecording();
      }
    };
  
    const sendToAPI = async (blob: Blob): Promise<void> => {
      const formData = new FormData();
      formData.append('audio', blob);
  
      try {
        console.log("before fetch");
        const response = await fetch('http://127.0.0.1:5000/', {
          method: 'POST',
          body: formData,
        });

        console.log(response);
  
        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }
  
        const data = await response.json();
        apiResponse = data.result || 'No result returned';
      } catch (err) {
        console.error('Error sending audio to API:', err);
        apiResponse = 'Error sending audio to API';
      }
    };
  </script>
  
  <div class="flex flex-col items-center justify-center h-screen text-center">
    <Button class="rounded-full shadow-lg px-6 py-2" on:click={toggleRecording}>
      {recording ? 'Stop Recording' : 'Start Recording'}
    </Button>
    <Textarea 
      class="w-4/5 h-24 resize-none shadow-lg rounded-lg mt-4" 
      readonly 
      bind:value={apiResponse} 
      placeholder="API response will appear here">
    </Textarea>
  </div>
  