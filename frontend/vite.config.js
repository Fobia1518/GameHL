import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/videos": "http://127.0.0.1:8000",
      "/feedback": "http://127.0.0.1:8000",
    },
  },
});
