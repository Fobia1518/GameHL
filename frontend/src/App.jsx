import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import Navbar from "./components/Navbar";
import Upload from "./pages/Upload";
import Status from "./pages/Status";
import Compare from "./pages/Compare";
import Feedback from "./pages/Feedback";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors">
          <Navbar />
          <main className="max-w-6xl mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Upload />} />
              <Route path="/status/:jobId" element={<Status />} />
              <Route path="/compare/:jobId" element={<Compare />} />
              <Route path="/feedback/:jobId" element={<Feedback />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}
