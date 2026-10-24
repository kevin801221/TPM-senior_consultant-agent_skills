import { defineConfig } from "vite";
export default defineConfig({
  build: {
    rolldownOptions: {
      onwarn(warning, defaultHandler) {
        // This is a browser-only app; React Server Component directives do not apply.
        if (warning.code === "MODULE_LEVEL_DIRECTIVE") return;
        defaultHandler(warning);
      },
      output: {
        codeSplitting: {
          groups: [
            {
              name: "markdown",
              test: /node_modules\/(?:react-markdown|remark-|rehype-|micromark|mdast|hast|unist|vfile|unified)/,
            },
            { name: "assistant", test: /node_modules\/@assistant-ui/ },
            {
              name: "react",
              test: /node_modules\/(?:react|react-dom|scheduler)\//,
            },
          ],
        },
      },
    },
  },
});
