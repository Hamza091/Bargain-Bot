import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export const TextMessageReducer = createSlice({
  name: "Message",
  initialState: {
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
  },
});

export const { SET_TEXTMESSGAGE, SET_RESPONSE } = TextMessageReducer.actions;
export default TextMessageReducer.reducer;
