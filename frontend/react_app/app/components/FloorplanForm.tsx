"use client";
import { useState } from "react";

export default function FloorplanForm() {
  const [file, setFile] = useState<File | null>(null);
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [msg, setMsg] = useState<string>("");
  const [markers, setMarkers] = useState<{ x: number; y: number }[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setImageSrc(URL.createObjectURL(selectedFile)); // Create a temporary URL for the uploaded image
      setMsg(""); // Clear any previous messages
      setMarkers([]); // Reset markers
    }
  };

  const handleRemove = () => {
    setMsg("");
    setFile(null);
    setImageSrc(null);
    setMarkers([]); // Clear all markers
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = ""; // Reset the input field
    }
  };

  const handleImageClick = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    if (!imageSrc) return;

    const boundingRect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - boundingRect.left; // Calculate x-coordinate relative to the image
    const y = e.clientY - boundingRect.top;  // Calculate y-coordinate relative to the image

    if (markers.length == 2) {
      // Only allow two markers (for start and end only) to be shown
      setMarkers([{ x, y }])
    } else {
      setMarkers((prev) => [...prev, { x, y }]); // Add the new marker
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file) {
      setMsg(`File submitted: ${file.name}`);
    } else {
      setMsg(`Please upload a file.`);
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

      {/* Display Message */}
      {msg && <div className="text-sm text-gray-700 mt-2">{msg}</div>}

      {/* Display Image with Markers */}
      {imageSrc && (
        <div
          className="relative mt-6 w-full max-w-lg"
          onClick={handleImageClick}
        >
          <img
            src={imageSrc}
            alt="Uploaded Floorplan"
            className="w-full rounded-lg shadow-lg"
          />
          {/* Render Markers */}
          {markers.map((marker, index) => (
            <div
              key={index}
              className="absolute w-4 h-4 rounded-full shadow-lg transform -translate-x-1/2 -translate-y-1/2"
              style={{
                left: `${marker.x}px`, top: `${marker.y}px`,
                backgroundColor: index === 0 ? 'green' : 'red'
              }}
            />
          ))}

          <div className="flex flex-col gap-4 w-full" style={{ marginTop: 20 }}>
            <div className="flex gap-4 justify-center">
              {markers.map((marker, index) => (
                <div
                  key={index}
                >
                  {index == 0 ? `Start` : `End`} Coords: {marker.x}, {marker.y}
                </div>
              ))}
            </div>
            <button
              className="w-full sm:w-auto rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-green-500 text-white gap-2 hover:bg-green-600 dark:hover:bg-green-400 text-sm sm:text-base h-12 px-6"
            >
              Send it!
            </button>
          </div>
        </div>
      )}
    </form>
  );
}
