import { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage("⚠️ Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const data = await response.json();
      setMessage(`✅ Upload successful: ${data.filename}`);
    } catch (error) {
      setMessage(`❌ Upload failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-lg font-bold text-gray-700">Upload File</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="border p-2 rounded w-full"
      />
      <button
        onClick={handleUpload}
        className={`px-4 py-2 rounded text-white ${
          file ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-400 cursor-not-allowed"
        }`}
        disabled={!file || loading}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div>
  );
};

export default FileUpload;
