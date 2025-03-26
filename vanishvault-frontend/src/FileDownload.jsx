import { useState } from "react";
import axios from "axios";

const FileDownload = () => {
  const [filename, setFilename] = useState("");

  const handleDownload = async () => {
    if (!filename) {
      alert("Please enter a filename");
      return;
    }
  
    try {
      const response = await axios.get(`http://127.0.0.1:8000/download/${filename}`, {
        responseType: "blob",
      });
  
      if (response.status !== 200) {
        throw new Error("File not found");
      }
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Download failed", error);
      alert("Download failed. File may not exist.");
    }
  };
  

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
      <input type="text" placeholder="Enter filename" value={filename} onChange={(e) => setFilename(e.target.value)} />
      <button onClick={handleDownload} className="bg-green-500 text-white px-4 py-2 rounded">
        Download
      </button>
    </div>
  );
};

export default FileDownload;
