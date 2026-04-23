import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Upload as UploadIcon, Video } from "lucide-react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef();
  const navigate = useNavigate();

  const handleFile = (f) => {
    if (f && f.type.startsWith("video/")) {
      setFile(f);
      setError(null);
    } else {
      setError("Solo se aceptan archivos de video");
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const { data } = await axios.post("/videos/upload", form);
      navigate(`/status/${data.job_id}`);
    } catch {
      setError("Error al subir el video, intenta de nuevo");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Subir video
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-8">
        Sube tu gameplay y generamos los highlights automáticamente
      </p>

      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFile(e.dataTransfer.files[0]);
        }}
        className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors
          ${dragging ? "border-orange-500 bg-orange-50 dark:bg-orange-950" : "border-gray-300 dark:border-gray-700 hover:border-orange-400 dark:hover:border-orange-500"}
        `}
      >
        <input
          ref={inputRef}
          type="file"
          accept="video/*"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        {file ? (
          <div className="flex flex-col items-center gap-3">
            <Video className="w-12 h-12 text-orange-500" />
            <p className="font-medium text-gray-900 dark:text-white">
              {file.name}
            </p>
            <p className="text-sm text-gray-500">
              {(file.size / 1024 / 1024).toFixed(1)} MB
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <UploadIcon className="w-12 h-12 text-gray-400" />
            <p className="font-medium text-gray-700 dark:text-gray-300">
              Arrastra tu video aquí
            </p>
            <p className="text-sm text-gray-500">o haz clic para seleccionar</p>
            <p className="text-xs text-gray-400">MP4, AVI, MOV soportados</p>
          </div>
        )}
      </div>

      {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className="mt-6 w-full py-3 px-6 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 dark:disabled:bg-gray-700 text-white font-semibold rounded-xl transition-colors disabled:cursor-not-allowed"
      >
        {loading ? "Subiendo..." : "Generar highlights"}
      </button>
    </div>
  );
}
