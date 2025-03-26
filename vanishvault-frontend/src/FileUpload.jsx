import { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async (event) => {
    event.preventDefault();

    const fileInput = document.querySelector('input[type="file"]');
    if (!fileInput.files.length) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);  // <-- Make sure the key matches FastAPI

    try {
        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Upload failed: ${response.status} ${response.statusText} - ${errorData.detail}`);
        }

        const data = await response.json();
        console.log("Upload Success:", data);
    } catch (error) {
        console.error("Error:", error);
        alert("Upload failed. Check console for details.");
    }
};


  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">
        Upload
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;
