import { configureStore } from "@reduxjs/toolkit";
import TextMessageReducer, { Buttons } from "./reducer";
import { Router } from "./reducer";
import store from "../redux/store";

export default configureStore({
  reducer: {
    TextMessage: TextMessageReducer,
    Router: Router,
    Buttons: Buttons,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
