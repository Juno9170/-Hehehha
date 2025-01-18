import React from 'react'
import { AudioRecorderWithVisualizer } from './Voice'
import { TooltipProvider } from './ui/tooltip'
const VoiceProvider = () => {
  return (
    <TooltipProvider>
        <AudioRecorderWithVisualizer />
    </TooltipProvider>
  )
}

export default VoiceProvider