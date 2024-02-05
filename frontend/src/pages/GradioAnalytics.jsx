import React from "react";
import { Box } from "@chakra-ui/react";

const GradioAnalytics = () => {
  return (
    <Box width="100%" height="100%" overflow="auto">
      <iframe
        src="https://c4ai-356718.lm.r.appspot.com/"
        title="Gradio Analytics"
        width="100%"
        height="100%"
        style={{ border: "none" }}
      />
    </Box>
  );
};

export default GradioAnalytics;
