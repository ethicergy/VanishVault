import FileUpload from "./FileUpload";
import FileDownload from "./FileDownload";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <div className="bg-white shadow-lg rounded-2xl p-6 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">VanishVault</h1>
        <FileUpload />
        <FileDownload />
      </div>
    </div>
  );
}


export default App;
