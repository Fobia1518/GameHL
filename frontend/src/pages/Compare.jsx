import { useParams, useNavigate } from "react-router-dom";
import { Download, MessageSquare } from "lucide-react";

export default function Compare() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const originalUrl = null; // el original no lo guardamos aún
  const highlightUrl = `/videos/download/${jobId}`;

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Resultado
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-8">
        Compara el video original con los highlights generados
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl p-4 border border-gray-200 dark:border-gray-800">
          <h2 className="font-semibold text-gray-900 dark:text-white mb-3">
            Video original
          </h2>
          <div className="bg-gray-100 dark:bg-gray-800 rounded-xl aspect-video flex items-center justify-center">
            <p className="text-gray-400 text-sm">No disponible</p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-2xl p-4 border border-gray-200 dark:border-gray-800">
          <h2 className="font-semibold text-gray-900 dark:text-white mb-3">
            Highlights generados
          </h2>
          <video
            src={highlightUrl}
            controls
            className="w-full rounded-xl aspect-video bg-black"
          />
        </div>
      </div>

      {/* <div className="flex flex-wrap gap-4">
        <a
          href={highlightUrl}
          download
          className="flex items-center gap-2 px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition-colors"
        >
          <Download className="w-4 h-4" />
          Descargar Full HD
        </a>
        <a
          href={`/videos/download/${jobId}/vertical`}
          download
          className="flex items-center gap-2 px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-semibold rounded-xl transition-colors"
        >
          <Download className="w-4 h-4" />
          Descargar 9:16 (TikTok / Reels)
        </a>
        <button
          onClick={() => navigate(`/feedback/${jobId}`)}
          className="flex items-center gap-2 px-6 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white font-semibold rounded-xl transition-colors"
        >
          <MessageSquare className="w-4 h-4" />
          Dar feedback
        </button>
      </div> */}
      <div className="flex flex-wrap gap-4">
        <a
          href={highlightUrl}
          download
          className="flex items-center gap-2 px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition-colors"
        >
          <Download className="w-4 h-4" />
          Full HD 16:9
        </a>

        <a
          href={`/videos/download/${jobId}/vertical-gameplay`}
          download
          className="flex items-center gap-2 px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-semibold rounded-xl transition-colors"
        >
          <Download className="w-4 h-4" />
          9:16
        </a>

        <button
          onClick={() => navigate(`/feedback/${jobId}`)}
          className="flex items-center gap-2 px-6 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white font-semibold rounded-xl transition-colors"
        >
          <MessageSquare className="w-4 h-4" />
          Dar feedback
        </button>
      </div>
    </div>
  );
}
