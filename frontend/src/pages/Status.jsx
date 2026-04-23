import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { CheckCircle, XCircle, Loader } from "lucide-react";

export default function Status() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const { data } = await axios.get(`/videos/status/${jobId}`);
        setJob(data);
        if (data.status === "done" || data.status === "error") {
          clearInterval(interval);
        }
      } catch {
        clearInterval(interval);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [jobId]);

  if (!job)
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Procesando video
      </h1>

      <div className="bg-white dark:bg-gray-900 rounded-2xl p-8 border border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-4 mb-6">
          {job.status === "done" && (
            <CheckCircle className="w-8 h-8 text-green-500" />
          )}
          {job.status === "error" && (
            <XCircle className="w-8 h-8 text-red-500" />
          )}
          {(job.status === "processing" || job.status === "queued") && (
            <Loader className="w-8 h-8 animate-spin text-orange-500" />
          )}
          <div>
            <p className="font-semibold text-gray-900 dark:text-white capitalize">
              {job.status}
            </p>
            <p className="text-sm text-gray-500">Job: {jobId}</p>
          </div>
        </div>

        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-6">
          <div
            className="bg-orange-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${job.progress}%` }}
          />
        </div>
        <p className="text-right text-sm text-gray-500 mb-6">{job.progress}%</p>

        {job.status === "error" && (
          <p className="text-red-500 text-sm mb-4">{job.error}</p>
        )}

        {job.status === "done" && (
          <div className="flex flex-col gap-3">
            <button
              onClick={() => navigate(`/compare/${jobId}`)}
              className="w-full py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition-colors"
            >
              Ver resultado
            </button>
            <button
              onClick={() => navigate(`/feedback/${jobId}`)}
              className="w-full py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white font-semibold rounded-xl transition-colors"
            >
              Dar feedback
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
