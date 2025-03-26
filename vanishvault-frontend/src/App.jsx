import FileUpload from "./FileUpload";
import FileDownload from "./FileDownload";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 space-y-6">
      <h1 className="text-2xl font-bold">VanishVault</h1>
      <FileUpload />
      <FileDownload />
    </div>
  );
}

export default App;
