import FileUpload from "./FileUpload";
import FileDownload from "./FileDownload";
import FileLister from "./FileLister"; // Import the new component

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <div className="bg-white shadow-lg rounded-2xl p-6 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">VanishVault</h1>
        <FileUpload />
        <FileDownload />
        <FileLister />  {/* Add file listing component here */}
      </div>
    </div>
  );
}

export default App;
