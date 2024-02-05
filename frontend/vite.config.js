import react from "@vitejs/plugin-react";
import dotenv from "dotenv";
import { defineConfig } from "vite";
import eslint from "vite-plugin-eslint";

dotenv.config();

export default defineConfig(({ command, mode, ssrBuild }) => {
  if (mode === "prod") {
    return {
      plugins: [react(), eslint()],
      build: {
        outDir: "dist",
        assetsDir: "static",
        publicPath: "/",
        sourcemap: true,
        minify: true,
        manifest: true,
        rollupOptions: {
          // input: '/src/main.jsx', // overwrite default .html entry
        },
      },
      define: {
        "process.env.ENVIRONMENT": JSON.stringify(process.env.ENVIRONMENT),
        "process.env.GOOGLE_ANALYTICS_ID": JSON.stringify(
          process.env.GOOGLE_ANALYTICS_ID
        ),
      },
    };
  } else {
    return {
      plugins: [react(), eslint()],
      build: {
        outDir: "dist",
        assetsDir: "static",
        publicPath: "/",
        sourcemap: true,
        minify: false,
        manifest: true,
        rollupOptions: {
          // input: '/src/main.jsx', // overwrite default .html entry
        },
        watch: {
          include: "src/**",
          exclude: "node_modules/**",
        },
      },
      define: {
        "process.env.ENVIRONMENT": JSON.stringify(process.env.ENVIRONMENT),
        "process.env.GOOGLE_ANALYTICS_ID": JSON.stringify(
          process.env.GOOGLE_ANALYTICS_ID
        ),
      },
    };
  }
});
