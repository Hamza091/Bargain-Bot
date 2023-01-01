import { configureStore } from "@reduxjs/toolkit";
import TextMessageReducer from "./reducer";
import store from "../redux/store";

export default configureStore({
  reducer: {
    TextMessage: TextMessageReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
