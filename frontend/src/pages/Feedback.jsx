import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { ThumbsUp, ThumbsDown, Clock } from "lucide-react";

export default function Feedback() {
  const { jobId } = useParams();
  const [clips, setClips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`/feedback/clips/${jobId}`)
      .then(({ data }) => setClips(data))
      .finally(() => setLoading(false));
  }, [jobId]);

  const submitFeedback = async (clipId, label) => {
    await axios.post(`/feedback/${clipId}`, { label });
    setClips((prev) =>
      prev.map((c) => (c.clip_id === clipId ? { ...c, label } : c)),
    );
  };

  if (loading)
    return (
      <div className="text-center text-gray-500 py-16">Cargando clips...</div>
    );

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Feedback
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-8">
        Evalúa cada clip para mejorar la detección futura
      </p>

      <div className="grid grid-cols-1 gap-6">
        {clips.map((clip, i) => (
          <div
            key={clip.clip_id}
            className="bg-white dark:bg-gray-900 rounded-2xl p-6 border border-gray-200 dark:border-gray-800"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-gray-900 dark:text-white">
                Clip #{i + 1}
              </h2>
              <div className="flex items-center gap-1 text-sm text-gray-500">
                <Clock className="w-4 h-4" />
                {clip.timestamp.toFixed(1)}s
              </div>
            </div>

            <video
              src={`http://127.0.0.1:8000/videos/clip/${clip.clip_id}`}
              controls
              className="w-full rounded-xl bg-black mb-4"
              style={{ maxHeight: "300px" }}
            />

            <div className="flex gap-3">
              <button
                onClick={() => submitFeedback(clip.clip_id, "highlight")}
                className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-semibold transition-colors
                  ${
                    clip.label === "highlight"
                      ? "bg-green-500 text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-950"
                  }`}
              >
                <ThumbsUp className="w-4 h-4" />
                Highlight
              </button>
              <button
                onClick={() => submitFeedback(clip.clip_id, "no_highlight")}
                className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-semibold transition-colors
                  ${
                    clip.label === "no_highlight"
                      ? "bg-red-500 text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-red-50 dark:hover:bg-red-950"
                  }`}
              >
                <ThumbsDown className="w-4 h-4" />
                No es highlight
              </button>
            </div>

            {clip.label && (
              <p className="text-center text-sm text-gray-500 mt-3">
                Guardado como <span className="font-medium">{clip.label}</span>
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
