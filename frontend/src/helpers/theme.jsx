import { extendTheme } from "@chakra-ui/react";

import { radioTheme } from "./radio.jsx";

const theme = extendTheme({
  components: {
    Radio: radioTheme,
  },
});

export default theme;
