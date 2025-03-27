import { useState, useEffect } from "react";
import axios from "axios";

const FileLister = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchFileList();
  }, []);

  const fetchFileList = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/filelist/");
      setFiles(response.data.files);
    } catch (err) {
      setError("Failed to fetch files.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (filename) => {
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
      alert("Download failed. File may not exist.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md mt-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Uploaded Files</h2>

      {loading && <p className="text-gray-500">Loading files...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <ul className="space-y-2">
        {files.length > 0 ? (
          files.map((file, index) => (
            <li key={index} className="flex justify-between items-center bg-gray-100 px-4 py-2 rounded">
              <span className="text-gray-800">{file}</span>
              <button
                onClick={() => handleDownload(file)}
                className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
              >
                Download
              </button>
            </li>
          ))
        ) : (
          <p className="text-gray-500">No files uploaded yet.</p>
        )}
      </ul>
    </div>
  );
};

export default FileLister;
