import React, { useState } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { SendHorizonal, PenLine } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import "../styles/global.css";
import VoiceProvider from "./VoiceProvider";

const Translatebox = () => {
  const [language, setLanguage] = React.useState("en-us");
  const [progress, setProgress] = React.useState(0);
  const [prompt, setPrompt] = React.useState("");
  const [translation, setTranslation] = React.useState("");
  const [isEditing, setIsEditing] = useState(false); // State to toggle between view and edit mode

  const handleSubmit = async () => {
    const response = await fetch("http://localhost:5050/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ body: { prompt, language } }),
    });

    if (response.ok) {
      const data = await response.json();
      setProgress(2);
      setTranslation(data.translatedText); // Log the translated text or response data
    } else {
      console.error("Failed to translate:", response.status);
    }
  };

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleTranslationChange = (e : any) => {
    setTranslation(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false); // Switch to view mode once user leaves the input field
  };

  const handleKeyPress = (e : any) => {
    if (e.key === "Enter") {
      setIsEditing(false); // Exit editing mode when Enter is pressed
    }
  };

  return (
    <div className="text-[#6e4555] px-20 flex flex-col text-lg items-center">
      <div>
        <div className="flex gap-6 mb-2">
          <p>Target:</p>
          <Select
            onValueChange={(lang) => {
              setLanguage(lang);
              if (lang === "en-us" || lang === "fr") setProgress(1);
              else setProgress(0);
            }}
          >
            <SelectTrigger className="w-[180px] rounded-[5px] bg-slate-200/30">
              <SelectValue placeholder="Select a language" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup className="bg-[#F5E3E0] ring-offset-black">
                <SelectLabel>Languages</SelectLabel>
                <SelectItem value=" " className="cursor-pointer">
                  Select a Language...
                </SelectItem>
                <SelectItem value="en-us" className="cursor-pointer">
                  English 🦅
                </SelectItem>
                <SelectItem value="fr" className="cursor-pointer">
                  French 🥖
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <AnimatePresence>
          {progress >= 1 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{ duration: 1, ease: "easeInOut" }}
            >
              <p className="pt-8 flex">Enter your prompt in any language</p>
              <div className="flex gap-2 pt-2">
                <Input
                  placeholder="type here.."
                  onChange={(e) => setPrompt(e.target.value)}
                  className="rounded-[5px] w-80 bg-slate-200/15"
                />
                <Button
                  size="icon"
                  variant="outline"
                  className="rounded-full bg-slate-200/15 hover:bg-slate-200/30 active:bg-slate-200/70"
                  onClick={handleSubmit}
                >
                  <SendHorizonal size={24} />
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {progress >= 2 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{ duration: 1, ease: "easeInOut" }}
            >
              <p className="pt-8 flex">Try Saying:</p>
              <div className="flex relative gap-2 pt-2 font-medium justify-center text-2xl">
                {isEditing ? (
                  <Input
                    value={translation}
                    onChange={handleTranslationChange}
                    onBlur={handleBlur}
                    onKeyUp={handleKeyPress}
                    className="w-full text-center bg-transparent border-none text-2xl focus:outline-none" // Centered, full width, no borders
                    autoFocus
                  />
                ) : (
                  <span className="text-2xl">{translation}</span>
                )}
                <div className="absolute right-0">
                  <Button
                    size="icon"
                    variant="outline"
                    className="rounded-full bg-slate-200/15 hover:bg-slate-200/30 active:bg-slate-200/70"
                    onClick={handleEditClick}
                  >
                    <PenLine size={24} />
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {progress === 2 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0, transition: { delay: 0.5 } }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{ duration: 1, ease: "easeInOut" }}
            >
              <VoiceProvider onFinish={() => setProgress(3)} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Translatebox;
