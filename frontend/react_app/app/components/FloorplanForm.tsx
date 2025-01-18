"use client"
import { useState } from "react";

export default function FloorplanForm() {
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState<String>("")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]); // Store the file in state
    }
  };

  const handleRemove = () => {
    setMsg("")
    setFile(null); // Clear the file state
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = ""; // Reset the input field
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file) {
      // Handle file upload
      setMsg(`File submitted: ${file.name}`)
    } else {
      setMsg(`Submit a file.`)
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col items-center gap-6 mt-6 w-full max-w-md mx-auto"
    >
      {/* File Input */}
      <input
        type="file"
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#383838] focus:border-[#383838]"
      />

      {/* Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 w-full">
        <button
          type="submit"
          className="w-full sm:w-auto rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-12 px-6"
        >
          Upload
        </button>
        <button
          type="button"
          onClick={handleRemove}
          className="w-full sm:w-auto rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-12 px-6"
        >
          Remove
        </button>
      </div>
      {msg && <div>{msg}</div>}
    </form>
  );
}
