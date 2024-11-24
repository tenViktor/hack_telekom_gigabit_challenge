import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()], // Use Vue plugin
  server: {
    host: "0.0.0.0", // Listen on all network interfaces
    port: 5173, // Port for dev server
    proxy: {
      // Proxy configuration for API calls
      "/api": {
        target: "http://backend:8000", // Forward to backend container
        changeOrigin: true, // Change request origin
        rewrite: (path) => path.replace(/^\/api/, ""), // Remove /api prefix
      },
    },
  },
});
