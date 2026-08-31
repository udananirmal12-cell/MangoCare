import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  preview: {
    allowedHosts: [
      "insightful-elegance-production-02d5.up.railway.app"
    ]
  }
});