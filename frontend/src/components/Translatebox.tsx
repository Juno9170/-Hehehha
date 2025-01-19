import React from 'react'
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
import { Input } from './ui/input'
import { Button } from './ui/button'
import { SendHorizonal } from 'lucide-react'
import { motion, AnimatePresence } from "framer-motion";
import "../styles/global.css"

const Translatebox = () => {
    const [language, setLanguage] = React.useState("en");
    const [progress, setProgress] = React.useState(0);
    return (
    <div className="text-[#6e4555] px-20 flex flex-col text-lg items-center">
    <div className="flex gap-6 mb-2">
      <p className=''>Target:</p>
      <Select onValueChange={(lang) => {setLanguage(lang); if (lang === 'en' || lang === 'fr') setProgress(1); else setProgress(0);}}>
      <SelectTrigger className="w-[180px] rounded-[5px] bg-slate-200/30">
        <SelectValue placeholder="Select a fruit" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup className='bg-[#F5E3E0] ring-offset-black'>
          <SelectLabel>Languages</SelectLabel>
          <SelectItem value=" " className='cursor-pointer'>Select a Language...</SelectItem>
          <SelectItem value="en" className='cursor-pointer'>English 🦅</SelectItem>
          <SelectItem value="fr" className='cursor-pointer'>French 🥖</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
    
    </div>
    <AnimatePresence>
        {progress>=1 && (
          <motion.div
            key="box"
            initial={{ opacity: 0, y: 50 }} // Start: hidden and slightly left
            animate={{ opacity: 1, y: 0 }}   // Animate to: fully visible and centered
            exit={{ opacity: 0, y: 50, transition:{duration:0.5} }}     // Exit: hidden and slightly right
            transition={{ duration: 1   , ease: "easeInOut" }} // Smooth timing
            
          >
            
            <p className='pt-8 flex'>Enter your prompt in any language</p>
            <div className='flex gap-2 pt-2'>
            <Input placeholder='type here..' className='rounded-[5px] w-80 bg-slate-200/15'/>
            <Button size="icon" variant="outline" className='rounded-full bg-slate-200/15 hover:bg-slate-200/30 active:bg-slate-200/70'>
                <SendHorizonal size={24} />
            </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    
  </div>
  )
}

export default Translatebox