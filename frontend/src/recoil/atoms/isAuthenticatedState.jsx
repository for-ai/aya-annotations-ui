import { atom } from "recoil";

export const isAuthenticatedState = atom({
  key: "isAuthenticatedState",
  default: false,
});
