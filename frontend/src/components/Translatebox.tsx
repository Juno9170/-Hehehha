import React, { useState, useEffect } from "react";
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
import Bird from "../../public/bird.png";
import { io, Socket } from "socket.io-client";

const socket: Socket = io("http://localhost:5050");

const Translatebox = () => {
  const [language, setLanguage] = React.useState("en-us");
  const [progress, setProgress] = React.useState(0);
  const [prompt, setPrompt] = React.useState("");
  const [translation, setTranslation] = React.useState("");
  const [isEditing, setIsEditing] = useState(false); // State to toggle between view and edit mode

  const [genText, setGenText] = useState("");
  const [genPhonemes, setGenPhonemes] = useState("");

  useEffect(() => {
    // Connect to the Socket.IO server
    socket.on("connect", () => {
      console.log("Connected to WebSocket server");
    });

    // Listen for "audio_processed" event
    socket.on("audio_processed", (data) => {
      setGenText(data.gen_text);
      setGenPhonemes(data.gen_phonemes);
    });

    // Cleanup the socket connection on component unmount
    return () => {
      socket.off("connect");
      socket.off("audio_processed");
    };
  }, []);

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

      const socket: Socket = io("http://localhost:5050"); // Connect to the server
      socket.emit("translated_text", { text: data.translatedText });

      // Optionally, disconnect the socket after emitting the event
      socket.disconnect();
    } else {
      console.error("Failed to translate:", response.status);
    }
  };

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleTranslationChange = (e: any) => {
    setTranslation(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false); // Switch to view mode once user leaves the input field
  };

  const handleKeyPress = (e: any) => {
    if (e.key === "Enter") {
      setIsEditing(false); // Exit editing mode when Enter is pressed
    }
  };

  return (
    <div className="text-[#6e4555] px-20 flex flex-col text-lg items-center">
      <div
        className={`${progress >= 3 ? "hidden" : ""} absolute ${
          progress === 0
            ? "bottom-32 left-1/4"
            : progress === 1
            ? "bottom-1/4 left-16"
            : progress === 2
            ? "bottom-[15%] left-16"
            : ""
        } transition-all duration-500 ease-in-out`}
      >
        <div className="relative">
          <img src={Bird.src || ""} className="w-60" />
          <div
            className={` ${
              progress >= 3 ? "hidden" : ""
            } absolute top-0 transform translate-x-full font-semibold bg-neutral-600/10 px-6 py-3 rounded-xl`}
          >{`${
            progress === 0
              ? "please pick a language from the dropdown menu"
              : progress === 1
              ? "Which phrase would you like to learn in the new language? "
              : progress === 2
              ? "Press the microphone button to test your pronounciation."
              : ""
          }`}</div>
        </div>
      </div>
      <div>
        {progress >= 3 && (
          <motion.div
            key="box"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
            transition={{ duration: 1, ease: "easeInOut" }}
            className="text-3xl font-medium text-center"
          >
            {progress === 3 ? (
              <button onClick={() => setProgress(4)}>show analysis</button>
            ) : (
              <div className="p-6 bg-[#F5E3E0] border border-solid drop-shadow-lg rounded-[8px] w-[50vw] flex flex-col gap-12">
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 0.2 }}
                  className="text-3xl font-medium text-center justify-around flex"
                >
                  <div>
                    Your Samples:
                    <audio controls>
                      <source
                        src="../../../server/test_audio_files/quickbrownfox.wav"
                        type="audio/wav"
                      />
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                  <div>
                    Correct Samples:
                    <audio controls>
                      <source
                        src="../../../server/test_audio_files/testingNOW.wav"
                        type="audio/wav"
                      />
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                </motion.div>
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 0.4 }}
                  className="text-base justify-around flex"
                >
                  <div>The quick brown fox jumps over the lazy dog.</div>
                  <div>{translation}</div>
                </motion.div>
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 0.6 }}
                  className="text-base justify-around flex"
                >
                  <div></div>
                  <div>ək wɪk bɹawn fɑks d͡ʒʌmpt owvɹ̩ð ə lejzi dɔɡ</div>
                </motion.div>
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 0.8 }}
                  className="text-base justify-around flex"
                >
                  <div>Your Samples</div>
                  <div>Correct Samples</div>
                </motion.div>
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 1 }}
                  className="text-base justify-around flex"
                >
                  <div>Your Samples</div>
                  <div>Correct Samples</div>
                </motion.div>
                <motion.div
                  key="box"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
                  transition={{ duration: 1, ease: "easeInOut", delay: 1.2 }}
                  className="text-base justify-around flex"
                >
                  <div>Your Samples</div>
                  <div>Correct Samples</div>
                </motion.div>
              </div>
            )}
            {progress === 4 && (
              <Button
                className=" text-xl bg-[#F5E3E0] hover:bg-[#ffbc9f] active:bg-[#c76c95] rounded-xl mt-5"
                onClick={() => setProgress(0)}
              >
                Go Again
              </Button>
            )}
          </motion.div>
        )}

        <div className="flex gap-6 mb-2">
          {progress < 3 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{
                duration: 1,
                ease: "easeInOut",
                delay: progress === 3 ? 1 : 0,
              }}
            >
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
            </motion.div>
          )}
        </div>
        <AnimatePresence>
          {progress >= 1 && progress < 3 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{
                duration: 1,
                ease: "easeInOut",
                delay: progress === 3 ? 0.5 : 0,
              }}
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
          {progress >= 2 && progress < 3 && (
            <motion.div
              key="box"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50, transition: { duration: 0.5 } }}
              transition={{
                duration: 1,
                ease: "easeInOut",
                delay: progress === 3 ? 0.1 : 0,
              }}
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
                  <span className="text-2xl max-w-[300px] text-center">
                    {translation}
                  </span>
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
              <VoiceProvider
                onFinish={() => setProgress(3)}
                titleString={translation}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Translatebox;
