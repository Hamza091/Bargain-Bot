import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export const TextMessageReducer = createSlice({
  name: "Message",
  initialState: {
    userId: null,
    text: "",
    result: [],
  },
  reducers: {
    SET_TEXTMESSGAGE: (state, action: PayloadAction<string>) => {
      state.text = action.payload;
    },
    SET_RESPONSE: (state, action: PayloadAction<object>) => {
      // @ts-ignore
      state.result.push(action.payload);
    },
    SET_USERID: (state, action: PayloadAction<string>) => {
      // @ts-ignore
      state.userId = action.payload;
    },
  },
});

export const { SET_TEXTMESSGAGE, SET_RESPONSE, SET_USERID } =
  TextMessageReducer.actions;
export default TextMessageReducer.reducer;

export const RouterReducer = createSlice({
  name: "Router",
  initialState: {
    route: "",
  },
  reducers: {
    SET_ROUTE: (state, action: PayloadAction<string>) => {
      state.route = action.payload;
    },
  },
});

export const { SET_ROUTE } = RouterReducer.actions;
export const Router = RouterReducer.reducer;

export const ButtonsReducer = createSlice({
  name: "Buttons",
  initialState: {
    botPopUp: false,
  },
  reducers: {
    SET_BOTPOPUP: (state, action: PayloadAction<boolean>) => {
      state.botPopUp = action.payload;
    },
  },
});

export const { SET_BOTPOPUP } = ButtonsReducer.actions;
export const Buttons = ButtonsReducer.reducer;
