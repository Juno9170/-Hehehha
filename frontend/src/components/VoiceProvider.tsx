import React from 'react'
import AudioRecorderWithVisualizer from './Voice'
import { TooltipProvider } from './ui/tooltip'
interface Props {
  onFinish: () => void; // This is a callback function that takes no arguments and returns nothing
  titleString:string;
}
const VoiceProvider: React.FC<Props> = ({ onFinish,titleString }) => {
  return (
    <TooltipProvider>
        <AudioRecorderWithVisualizer onFinish = {onFinish} titleString={titleString} />
    </TooltipProvider>
  )
}

export default VoiceProvider