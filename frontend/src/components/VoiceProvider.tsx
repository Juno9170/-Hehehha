import React from 'react'
import AudioRecorderWithVisualizer from './Voice'
import { TooltipProvider } from './ui/tooltip'
interface Props {
  onFinish: () => void; // This is a callback function that takes no arguments and returns nothing
}
const VoiceProvider: React.FC<Props> = ({ onFinish }) => {
  return (
    <TooltipProvider>
        <AudioRecorderWithVisualizer onFinish = {onFinish} />
    </TooltipProvider>
  )
}

export default VoiceProvider