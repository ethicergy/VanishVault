import { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

const handleUpload = async (event) => {
  event.preventDefault();
  if (!file) {
    setMessage("Please select a file");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload/", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`);
    }

    const data = await response.json();
    setMessage(`Upload successful: ${data.filename}`);  // ✅ Display filename
  } catch (error) {
    setMessage("Upload failed.");
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
