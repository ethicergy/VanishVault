import { useState } from "react";
import axios from "axios";

const FileDownload = () => {
  const [filename, setFilename] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleDownload = async () => {
    if (!filename) {
      setMessage("⚠️ Please enter a filename.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.get(`http://127.0.0.1:8000/download/${filename}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMessage(`✅ Download successful: ${filename}`);
    } catch (error) {
      console.error("Download failed", error);
      setMessage("❌ Download failed. File may not exist.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-lg font-bold text-gray-700">Download File</h2>
      <input
        type="text"
        placeholder="Enter filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        className="border p-2 rounded w-full"
      />
      <button
        onClick={handleDownload}
        className={`px-4 py-2 rounded text-white ${
          filename ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-400 cursor-not-allowed"
        }`}
        disabled={!filename || loading}
      >
        {loading ? "Downloading..." : "Download"}
      </button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div>
  );
};

export default FileDownload;
